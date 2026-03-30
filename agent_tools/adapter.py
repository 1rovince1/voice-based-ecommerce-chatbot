from typing import Dict, List


def build_ollama_tools(registry: Dict[str, Dict]) -> List:
    tools = []
    
    for name, tool in registry.items():
        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": tool["description"],
                "parameters": tool["input_schema"].model_json_schema()
            }
        })

    return tools