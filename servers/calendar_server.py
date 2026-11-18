import os
import time

from mcp.server import MCPServer

mcp = MCPServer("SpeakerOps Calendar Demo")

EVENTS = [
    {
        "event_id": "e1",
        "title": "MCP Dev Summit Nairobi",
        "start": "2026-11-20T08:00:00+03:00",
        "end": "2026-11-20T18:00:00+03:00",
        "location": "Hyatt Regency Nairobi Westlands",
        "description": "Conference-level event.",
    },
    {
        "event_id": "e2",
        "title": "Beyond the Demo: What Breaks When One AI Agent Talks to Multiple MCPs",
        "start": "2026-11-20T16:15:00+03:00",
        "end": "2026-11-20T16:40:00+03:00",
        "location": "Muthithu, 6th Floor",
        "description": "MCP Dev Summit Nairobi speaking session for Ronnie Atuhaire.",
    },
]


def maybe_delay():
    delay_ms = int(os.getenv("CALENDAR_LATENCY_MS", "0") or "0")
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)


@mcp.tool()
def list_events() -> list[dict]:
    """List synthetic calendar events."""
    maybe_delay()
    return EVENTS


@mcp.tool()
def search_events(query: str) -> list[dict]:
    """Search synthetic calendar events by title, location, or description."""
    maybe_delay()
    q = query.lower().strip()
    return [
        event
        for event in EVENTS
        if q in (
            f"{event['title']} {event['location']} {event['description']}"
        ).lower()
    ]


@mcp.tool()
def get_event(event_id: str) -> dict:
    """Get one synthetic calendar event."""
    maybe_delay()
    for event in EVENTS:
        if event["event_id"] == event_id:
            return event
    raise ValueError(f"Event not found: {event_id}")


@mcp.tool()
def create_event(
    title: str,
    start: str,
    end: str,
    location: str = "",
    description: str = "",
) -> dict:
    """
    Create a synthetic event.

    When CHAOS_CALENDAR=1, the event is committed first and then a simulated
    connection failure is raised. This demonstrates an UNKNOWN write outcome.
    """
    event = {
        "event_id": f"e{len(EVENTS) + 1}",
        "title": title,
        "start": start,
        "end": end,
        "location": location,
        "description": description,
    }

    EVENTS.append(event)

    if os.getenv("CHAOS_CALENDAR", "0") == "1":
        raise RuntimeError(
            "SIMULATED CONNECTION LOSS AFTER COMMIT: outcome is UNKNOWN to the caller."
        )

    return event


@mcp.tool()
def delete_event(event_id: str) -> dict:
    """Delete a synthetic event."""
    for index, event in enumerate(EVENTS):
        if event["event_id"] == event_id:
            deleted = EVENTS.pop(index)
            return {"status": "deleted", "event": deleted}
    raise ValueError(f"Event not found: {event_id}")


if __name__ == "__main__":
    mcp.run()
