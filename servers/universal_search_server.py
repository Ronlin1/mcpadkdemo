from mcp.server import MCPServer

mcp = MCPServer("SpeakerOps Universal Search Demo")

CORPUS = [
    {
        "source": "gmail",
        "id": "t1",
        "title": "MCP Dev Summit Nairobi: Speaker Next Steps",
        "text": "Speaker logistics from events@aaif.io.",
    },
    {
        "source": "drive",
        "id": "f1",
        "title": "mcp-dev-summit-talk-v7.md",
        "text": (
            "MCP standardizes the connection layer; coordination remains "
            "an application concern."
        ),
    },
    {
        "source": "calendar",
        "id": "e2",
        "title": "Beyond the Demo",
        "text": (
            "MCP Dev Summit Nairobi speaking session Friday Nov 20, "
            "16:15-16:40 EAT, Muthithu 6th Floor."
        ),
    },
    {
        "source": "drive",
        "id": "f3",
        "title": "mcp-auth-notes.md",
        "text": (
            "Internal notes mentioning MCP authentication, OAuth, "
            "authorization boundaries, and token handling."
        ),
    },
    {
        "source": "gmail",
        "id": "t3",
        "title": "Re: MCP authentication discussion",
        "text": "An email thread discussing auth choices for MCP clients.",
    },
]


@mcp.tool()
def search_corpus(query: str) -> list[dict]:
    """Cross-product synthetic search spanning Gmail, Drive, and Calendar."""
    q = query.lower().strip()
    return [
        item
        for item in CORPUS
        if q in f"{item['title']} {item['text']} {item['source']}".lower()
    ]


if __name__ == "__main__":
    mcp.run()
