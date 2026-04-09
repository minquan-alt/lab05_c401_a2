from langchain_core.tools import tool

@tool
def validate_input(model: str = None, model_year: int = None, firmware: str = None):
    """
    Validate metadata required by diagnostic pipeline.
    This step only checks presence, it does not normalize or repair data.
    """
    missing = []

    if model_year is None:
        missing.append("model_year")

    if not firmware:
        missing.append("firmware")

    return {
        "valid": len(missing) == 0,
        "missing_fields": missing
    }
