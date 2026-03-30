from typing import Callable

from agent_tools.schemas.input.retrieval import *
from agent_tools.functions.retrieval import *


def get_tool_desc(function: Callable):
    if not function.__doc__:
        return ""
    return function.__doc__.strip()


TOOLS = {
    "sql_query_tool": {
        "function": database_query_tool,
        "input_schema": SqlQueryInput,
        "description": get_tool_desc(database_query_tool)
    },
    "policy_query_tool": {
        "function": policy_query_tool,
        "input_schema": PolicyQueryInput,
        "description": get_tool_desc(policy_query_tool)
    }
}