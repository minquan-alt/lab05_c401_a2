from langchain_core.tools import tool

@tool
def name_tool(city: str) -> str:
    ...
    
# sau khi viet tool, nho add vao tools_mapping.py