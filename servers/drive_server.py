from mcp.server import MCPServer

mcp = MCPServer("SpeakerOps Drive Demo")

FILES = [
    {
        "file_id": "f1",
        "name": "mcp-dev-summit-talk-v7.md",
        "mime_type": "text/markdown",
        "content": (
            "# Beyond the Demo\n\n"
            "Thesis: MCP standardizes the connection layer; coordination "
            "remains an application concern.\n\n"
            "Closing: MCP gives tools a common interface. Engineering makes "
            "multi-server agents reliable."
        ),
    },
    {
        "file_id": "f2",
        "name": "speaker-checklist.txt",
        "mime_type": "text/plain",
        "content": (
            "Laptop\nHDMI adapter\nSlides PDF\nDemo fallback recording\n"
        ),
    },
]


@mcp.tool()
def search_files(query: str) -> list[dict]:
    """Search synthetic Drive files by name or content."""
    q = query.lower().strip()
    results = []
    for item in FILES:
        haystack = f"{item['name']} {item['content']}".lower()
        if q in haystack:
            results.append(
                {
                    "file_id": item["file_id"],
                    "name": item["name"],
                    "mime_type": item["mime_type"],
                }
            )
    return results


@mcp.tool()
def read_file_content(file_id: str) -> dict:
    """Read one synthetic Drive file."""
    for item in FILES:
        if item["file_id"] == file_id:
            return item
    raise ValueError(f"File not found: {file_id}")


if __name__ == "__main__":
    mcp.run()
