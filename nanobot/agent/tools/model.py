"""Tools for managing AI models."""

from typing import Any, Callable, Awaitable
from nanobot.agent.tools.base import Tool


class ListModelsTool(Tool):
    """Tool to list available AI models."""
    
    name = "list_models"
    description = "List available AI models and the currently active model."
    parameters = {
        "type": "object",
        "properties": {},
    }

    def __init__(self, get_models_cb: Callable[[], list[str]], current_model: str):
        super().__init__()
        self.get_models_cb = get_models_cb
        self.current_model = current_model

    async def execute(self) -> str:
        models = self.get_models_cb()
        active = self.current_model
        
        res = "Available models (configured providers):\n"
        for m in models:
            status = "(active)" if m == active else ""
            res += f"- {m} {status}\n"
        
        res += "\nYou can switch to any of these models using the switch_model tool."
        return res


class SwitchModelTool(Tool):
    """Tool to switch the active AI model."""
    
    name = "switch_model"
    description = "Switch the currently active AI model."
    parameters = {
        "type": "object",
        "properties": {
            "model": {
                "type": "string",
                "description": "The identifier of the model to switch to (e.g., 'nvidia/meta/llama-3.1-70b-instruct')"
            }
        },
        "required": ["model"]
    }

    def __init__(self, switch_cb: Callable[[str], Awaitable[None]]):
        super().__init__()
        self.switch_cb = switch_cb

    async def execute(self, model: str) -> str:
        try:
            await self.switch_cb(model)
            return f"Successfully switched to model: {model}"
        except Exception as e:
            return f"Failed to switch model: {str(e)}"
