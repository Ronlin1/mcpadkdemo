import asyncio
import traceback

from speakerops.agent import (
    gmail,
    drive,
    docs_read,
    docs_write,
    calendar_read,
    calendar_write,
    universal,
    developer_knowledge,
)

SERVERS = [
    ("Gmail", gmail),
    ("Drive", drive),
    ("Docs Read", docs_read),
    ("Docs Write", docs_write),
    ("Calendar Read", calendar_read),
    ("Calendar Write", calendar_write),
    ("Universal Search", universal),
    ("Developer Knowledge", developer_knowledge),
]


async def main():
    for name, toolset in SERVERS:
        print()
        print("=" * 70)
        print(name)
        print("=" * 70)

        try:
            tools = await toolset.get_tools()
            print(f"OK - {len(tools)} tools")
            for tool in tools:
                print("  ", tool.name)
        except Exception as exc:
            print("FAILED:", type(exc).__name__, str(exc))
            traceback.print_exc()

    for _, toolset in SERVERS:
        try:
            await toolset.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
