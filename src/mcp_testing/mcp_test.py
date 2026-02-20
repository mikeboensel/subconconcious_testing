"""Generic MCP Server Explorer.

Connects to any MCP server via stdio or streamable HTTP, discovers all
capabilities (tools, resources, prompts, resource templates), and optionally
calls a tool.

Usage:
    # Stdio transport
    uv run src/mcp_testing/mcp_test.py stdio npx -y @upstash/context7-mcp

    # Streamable HTTP transport
    uv run src/mcp_testing/mcp_test.py http https://mcp.context7.com/mcp

    # Call a specific tool after discovery
    uv run src/mcp_testing/mcp_test.py stdio npx -y @upstash/context7-mcp \
        --call-tool resolve-library-id '{"libraryName":"react"}'
"""

import argparse
import asyncio
import json
import os
import shutil

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    line = "=" * 60
    print(f"\n{line}")
    print(f"  {title}")
    print(line)


def print_json(data: object, indent: int = 2) -> None:
    print(json.dumps(data, indent=indent, default=str))


# ---------------------------------------------------------------------------
# MCPServerExplorer — server-agnostic
# ---------------------------------------------------------------------------

class MCPServerExplorer:
    """Explores any MCP server through a connected ClientSession."""

    def __init__(self, session: ClientSession) -> None:
        self.session = session
        self.tools: list = []
        self.resources: list = []
        self.prompts: list = []
        self.resource_templates: list = []

    async def discover_all(self) -> None:
        self.tools = await self.discover_tools()
        self.resources = await self.discover_resources()
        self.prompts = await self.discover_prompts()
        self.resource_templates = await self.discover_resource_templates()

    async def discover_tools(self) -> list:
        try:
            result = await self.session.list_tools()
            return list(result.tools)
        except Exception as e:
            print(f"  Could not list tools: {e}")
            return []

    async def discover_resources(self) -> list:
        try:
            result = await self.session.list_resources()
            return list(result.resources)
        except Exception as e:
            print(f"  Could not list resources: {e}")
            return []

    async def discover_prompts(self) -> list:
        try:
            result = await self.session.list_prompts()
            return list(result.prompts)
        except Exception as e:
            print(f"  Could not list prompts: {e}")
            return []

    async def discover_resource_templates(self) -> list:
        try:
            result = await self.session.list_resource_templates()
            return list(result.resource_templates)
        except Exception as e:
            print(f"  Could not list resource templates: {e}")
            return []

    async def call_tool(self, name: str, arguments: dict) -> object:
        result = await self.session.call_tool(name, arguments)
        return result


# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------

def display_tools(tools: list) -> None:
    print_header(f"Tools ({len(tools)})")
    if not tools:
        print("  None found.")
        return
    for i, tool in enumerate(tools, 1):
        print(f"\n  [{i}] {tool.name}")
        if tool.description:
            desc = tool.description
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"      Description: {desc}")
        if tool.inputSchema:
            props = tool.inputSchema.get("properties", {})
            required = tool.inputSchema.get("required", [])
            if props:
                print("      Parameters:")
                for pname, pschema in props.items():
                    req = " (required)" if pname in required else ""
                    ptype = pschema.get("type", "any")
                    pdesc = pschema.get("description", "")
                    if len(pdesc) > 100:
                        pdesc = pdesc[:100] + "..."
                    print(f"        - {pname}: {ptype}{req}")
                    if pdesc:
                        print(f"          {pdesc}")


def display_resources(resources: list) -> None:
    print_header(f"Resources ({len(resources)})")
    if not resources:
        print("  None found.")
        return
    for i, res in enumerate(resources, 1):
        print(f"\n  [{i}] {res.uri}")
        if res.name:
            print(f"      Name: {res.name}")
        if res.description:
            print(f"      Description: {res.description}")
        if res.mimeType:
            print(f"      MIME type: {res.mimeType}")


def display_prompts(prompts: list) -> None:
    print_header(f"Prompts ({len(prompts)})")
    if not prompts:
        print("  None found.")
        return
    for i, prompt in enumerate(prompts, 1):
        print(f"\n  [{i}] {prompt.name}")
        if prompt.description:
            print(f"      Description: {prompt.description}")
        if prompt.arguments:
            print("      Arguments:")
            for arg in prompt.arguments:
                req = " (required)" if arg.required else ""
                print(f"        - {arg.name}{req}")
                if arg.description:
                    print(f"          {arg.description}")


def display_resource_templates(templates: list) -> None:
    print_header(f"Resource Templates ({len(templates)})")
    if not templates:
        print("  None found.")
        return
    for i, tmpl in enumerate(templates, 1):
        print(f"\n  [{i}] {tmpl.uriTemplate}")
        if tmpl.name:
            print(f"      Name: {tmpl.name}")
        if tmpl.description:
            print(f"      Description: {tmpl.description}")
        if tmpl.mimeType:
            print(f"      MIME type: {tmpl.mimeType}")


async def display_server_info(explorer: MCPServerExplorer) -> None:
    print_header("Discovering server capabilities...")
    await explorer.discover_all()

    display_tools(explorer.tools)
    display_resources(explorer.resources)
    display_prompts(explorer.prompts)
    display_resource_templates(explorer.resource_templates)

    total = (
        len(explorer.tools)
        + len(explorer.resources)
        + len(explorer.prompts)
        + len(explorer.resource_templates)
    )
    print_header("Summary")
    print(f"  Tools:              {len(explorer.tools)}")
    print(f"  Resources:          {len(explorer.resources)}")
    print(f"  Prompts:            {len(explorer.prompts)}")
    print(f"  Resource Templates: {len(explorer.resource_templates)}")
    print(f"  Total capabilities: {total}")


# ---------------------------------------------------------------------------
# Connection functions
# ---------------------------------------------------------------------------

async def connect_stdio(
    command: str, args: list[str], env: dict[str, str] | None = None,
) -> tuple:
    """Connect to an MCP server via stdio transport.

    Returns (AsyncExitStack, ClientSession).
    """
    from contextlib import AsyncExitStack

    if not shutil.which(command):
        raise FileNotFoundError(
            f"Command '{command}' not found on PATH. "
            "Make sure it is installed and accessible."
        )

    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=env or {**os.environ},
    )

    exit_stack = AsyncExitStack()
    read, write = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    session = await exit_stack.enter_async_context(
        ClientSession(read, write)
    )
    await session.initialize()
    return exit_stack, session


async def connect_http(
    url: str, headers: dict[str, str] | None = None,
) -> tuple:
    """Connect to an MCP server via streamable HTTP transport.

    Returns (AsyncExitStack, ClientSession).
    """
    from contextlib import AsyncExitStack

    exit_stack = AsyncExitStack()
    read, write, _ = await exit_stack.enter_async_context(
        streamablehttp_client(url=url, headers=headers or {})
    )
    session = await exit_stack.enter_async_context(
        ClientSession(read, write)
    )
    await session.initialize()
    return exit_stack, session


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generic MCP Server Explorer — discover any MCP server's capabilities.",
    )
    parser.add_argument(
        "--call-tool",
        nargs=2,
        metavar=("TOOL_NAME", "JSON_ARGS"),
        help="Call a tool after discovery. Provide tool name and JSON arguments.",
    )

    subparsers = parser.add_subparsers(dest="transport", required=True)

    # stdio subcommand
    stdio_parser = subparsers.add_parser(
        "stdio",
        help="Connect via stdio transport (local subprocess).",
    )
    stdio_parser.add_argument(
        "command",
        help="Command to run the MCP server (e.g. 'npx', 'python').",
    )
    stdio_parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Arguments for the server command.",
    )

    # http subcommand
    http_parser = subparsers.add_parser(
        "http",
        help="Connect via streamable HTTP transport (remote server).",
    )
    http_parser.add_argument(
        "url",
        help="URL of the MCP server endpoint.",
    )
    http_parser.add_argument(
        "--header",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="HTTP headers to send (repeatable). E.g. --header 'Authorization=Bearer tok'",
    )

    return parser.parse_args()


async def async_main() -> None:
    args = parse_args()

    exit_stack = None
    try:
        if args.transport == "stdio":
            print(f"Connecting via stdio: {args.command} {' '.join(args.args)}")
            exit_stack, session = await connect_stdio(args.command, args.args)

        elif args.transport == "http":
            headers = {}
            for h in args.header:
                if "=" not in h:
                    print(f"Warning: skipping malformed header (no '='): {h}")
                    continue
                key, value = h.split("=", 1)
                headers[key.strip()] = value.strip()
            print(f"Connecting via HTTP: {args.url}")
            exit_stack, session = await connect_http(args.url, headers)

        explorer = MCPServerExplorer(session)
        await display_server_info(explorer)

        # Optional tool call
        if args.call_tool:
            tool_name, json_args = args.call_tool
            try:
                arguments = json.loads(json_args)
            except json.JSONDecodeError as e:
                print(f"\nError: invalid JSON for tool arguments: {e}")
                return

            print_header(f"Calling tool: {tool_name}")
            print(f"  Arguments: {json.dumps(arguments, indent=2)}")
            try:
                result = await explorer.call_tool(tool_name, arguments)
                print(f"\n  Result:")
                for content in result.content:
                    if hasattr(content, "text"):
                        text = content.text
                        # Try to pretty-print if it's JSON
                        try:
                            parsed = json.loads(text)
                            print_json(parsed)
                        except (json.JSONDecodeError, TypeError):
                            print(f"  {text}")
                    else:
                        print(f"  {content}")
            except Exception as e:
                print(f"\n  Tool call failed: {e}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if exit_stack:
            await exit_stack.aclose()
            print("\nDisconnected.")


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
