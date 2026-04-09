from langchain_core.tools import tool


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí."""

    expense_dict = {}
    try:
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue
            parts = item.split(":")
            if len(parts) != 2:
                return f"❌ Lỗi định dạng: '{item}' không đúng cú pháp 'tên:số_tiền'."
            name = parts[0].strip().replace("_", " ").title()
            amount = int(parts[1].strip())
            expense_dict[name] = amount
    except ValueError:
        return "❌ Lỗi: Số tiền trong phần chi phí phải là số nguyên (không có ký tự đặc biệt)."

    total_spent = sum(expense_dict.values())
    remaining = total_budget - total_spent

    def fmt(amount: int) -> str:
        return f"{abs(amount):,}".replace(",", ".") + "đ"

    lines = ["📋 Bảng chi phí:"]
    for name, amount in expense_dict.items():
        lines.append(f"  - {name}: {fmt(amount)}")

    lines.append("  ---")
    lines.append(f"  Tổng chi:  {fmt(total_spent)}")
    lines.append(f"  Ngân sách: {fmt(total_budget)}")

    if remaining >= 0:
        lines.append(f"  Còn lại:   {fmt(remaining)} ✅")
    else:
        lines.append(f"  Còn lại:   -{fmt(remaining)}")
        lines.append(f"\n⚠️  Vượt ngân sách {fmt(remaining)} ! Cần điều chỉnh.")

    return "\n".join(lines)
