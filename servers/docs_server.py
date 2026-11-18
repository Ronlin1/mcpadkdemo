from mcp.server import MCPServer

mcp = MCPServer("SpeakerOps Docs Demo")

DOCS = {
    "doc1": {
        "document_id": "doc1",
        "title": "Speaker Briefing",
        "content": (
            "MCP Dev Summit Nairobi speaker briefing. "
            "Keep the live demo deterministic, have a fallback recording, "
            "and emphasize production coordination failure modes."
        ),
    }
}


@mcp.tool()
def read_doc(document_id: str) -> dict:
    """Read a synthetic Google Doc."""
    if document_id not in DOCS:
        raise ValueError(f"Document not found: {document_id}")
    return DOCS[document_id]


@mcp.tool()
def update_doc(document_id: str, content: str) -> dict:
    """Update a synthetic Google Doc in memory."""
    if document_id not in DOCS:
        raise ValueError(f"Document not found: {document_id}")
    DOCS[document_id]["content"] = content
    return {
        "document_id": document_id,
        "status": "updated",
    }


if __name__ == "__main__":
    mcp.run()
