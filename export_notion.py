from notion_client import Client

# Initialize the Notion client with your integration token
notion = Client(auth="YOUR_NOTION_TOKEN")

# Define the parent page or database where you want to create the new page
parent_page_id = "1b3a34ce-a773-8060-91b8-dc3569cd049f"

# Define the properties of the new page
new_page = {
    "parent": {"type": "page_id", "page_id": parent_page_id},
    "properties": {
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "My New Notion Page"
                }
            }
        ]
    },
    "children": [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Introduction"
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "This is a sample page created using the Notion API in Python."
                        }
                    }
                ]
            }
        }
    ]
}

# Create the new page in Notion
response = notion.pages.create(**new_page)

print("New page created:", response["url"])
