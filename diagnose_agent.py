import asyncio

from speakerops.agent import root_agent


async def main():
    print("root_agent tools:", len(root_agent.tools))

    for i, toolset in enumerate(root_agent.tools, 1):
        print()
        print("=" * 70)
        print(i, type(toolset).__name__)
        print("prefix:", getattr(toolset, "tool_name_prefix", None))
        print("filter:", getattr(toolset, "tool_filter", None))

        tools = await toolset.get_tools()

        for tool in tools:
            prefix = getattr(toolset, "tool_name_prefix", None)
            expected = f"{prefix}{tool.name}" if prefix else tool.name
            print("RAW:", tool.name, " | EXPECTED EXPOSED:", expected)

    for toolset in root_agent.tools:
        try:
            await toolset.close()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
