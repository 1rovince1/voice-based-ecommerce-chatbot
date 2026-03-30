from typing import Any
import inspect


async def dispatch_tool(
        registry: dict[str, dict],
        tool_name: str,
        args: dict[str, Any],
        application_context: dict | None = None
) -> dict[str, Any]:

    application_context = application_context or {}
    
    if tool_name not in registry:
        raise ValueError(f"Unknown tool {tool_name}")
    
    tool = registry[tool_name]
    function = tool["function"]
    input_schema = tool["input_schema"]
    # output_schema = tool["output_schema"]

    # validate input
    try:
        input_model = input_schema(**args)
    except Exception as e:
        raise ValueError(f"Invalid input for tool {tool_name}: {e}")
    
    kwargs = input_model.model_dump(
        exclude_none=True,
        exclude_defaults=True
    )

    # check if function accepts application_context
    sig = inspect.signature(function)
    if application_context is not None and "application_context" in sig.parameters:
        kwargs["application_context"] = application_context
    
    # call function
    try:
        if inspect.iscoroutinefunction(function):
            result = await function(**kwargs)
        else:
            result = function(**kwargs)
    except Exception as e:
        raise RuntimeError(f"Tool {tool_name} execution failed: {e}")
    
    # # validate output
    # try:
    #     output_model = output_schema(**result.model_dump())
    # except Exception as e:
    #     raise RuntimeError(f"Invalid output from tool {tool_name}: {e}")
    
    # return output_model.model_dump()
    return result