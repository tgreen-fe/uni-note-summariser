from openai import OpenAI
import os
import textwrap
from notion_client import Client

client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

# Initialize the Notion client with your integration token
notion = Client(auth="YOUR_NOTION_TOKEN")

# Define the parent page or database where you want to create the new page
parent_page_id = "1b3a34ce-a773-8060-91b8-dc3569cd049f"


def parse_reply_to_blocks(reply):
    blocks = []
    parent_bullet = None  # Keep track of the last parent bullet point

    lines = reply.split("\n")  # Split the reply into lines

    for line in lines:
        if line.startswith("  - "):  # Indented bullet point
            if parent_bullet is not None:
                # Add this as a nested bullet point under the last bullet point
                parent_bullet.setdefault("bulleted_list_item", {}).setdefault("children", []).append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": line[3:]  # Remove the '\t- ' from the line
                                }
                            }
                        ]
                    }
                })
        elif line.startswith("- "):  # Regular bullet point
            bullet = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": line[2:]  # Remove the '- ' from the line
                            }
                        }
                    ]
                }
            }
            blocks.append(bullet)
            parent_bullet = bullet  # Update the parent bullet point
        else:
            # It's a normal paragraph
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": line
                            }
                        }
                    ]
                }
            })
            parent_bullet = None  # Reset parent bullet point after a paragraph

    return blocks

f = open("summary_subjects.txt").read()

with open("summary_subjects.txt") as file:
    for line in file:
        if line.strip() != "":
            subject = line.strip()

            messages = [{"role": "system",
                         "content": f"""I am a final year medical student studying in the UK. Summarise the requested subject
                         with the subtitles background, risk factors, causes, pathophysiology, signs and symptoms, investigations, 
                         diagnosis, management. Please only use bullet points for everything other than the subtitles. 
                         For background, use only 1 bullet point with maximum 25 words. Do not use full stops after each 
                         bullet point. For diagnosis and management, base this on the NICE guidelines. if available. 
                         Write a maximum of 5 bullet points for risk factors, 5 for causes, 5 for investigations, 
                         and 5 for diagnosis. Write a maximum of 5 bullet points for management, with a maximum of 2 
                         sub-bullet points for each. Do not use bold writing. Do not use colons in the bullet points. 
                         Do not use italics other than for species names. Use British English."""},
                        {"role": "user", "content": f"Summarise {subject}."}
                        ]

            print(messages[1])

            chat = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
            reply = chat.choices[0].message.content

            # Call the function to parse the reply into Notion blocks
            children_blocks = parse_reply_to_blocks(reply)

            # Define the properties of the new page
            new_page = {
                "parent": {"type": "page_id", "page_id": parent_page_id},
                "properties": {
                    "title": {
                        "title": [
                            {
                                "type": "text",
                                "text": {
                                    "content": subject
                                }
                            }
                        ]
                    }
                },
                "children": children_blocks
            }

            # Create the new page in Notion
            response = notion.pages.create(**new_page)

            print("New page created:", response["url"])





