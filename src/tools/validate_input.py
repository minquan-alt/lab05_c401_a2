from langchain_core.tools import tool

@tool
def validate_input(model: str = None, model_year: int = None, firmware: str = None):
    """
    Validate vehicle metadata.
    Required before performing diagnosis.
    """

    missing = []

    if not model:
        missing.append("model")

    if not model_year:
        missing.append("model_year")

    if not firmware:
        missing.append("firmware")

    if missing:
        return {
            "valid": False,
            "missing_fields": missing
        }

    return {
        "valid": True
    }
