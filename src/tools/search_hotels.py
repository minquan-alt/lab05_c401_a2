from langchain_core.tools import tool

# ==============================================================================
# HOTELS_DB
# ==============================================================================

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm."""

    if city not in HOTELS_DB:
        return f"Hiện tại chúng tôi không có dữ liệu khách sạn tại thành phố {city}."

    all_hotels = HOTELS_DB[city]
    filtered_hotels = [h for h in all_hotels if h["price_per_night"] <= max_price_per_night]

    if not filtered_hotels:
        formatted_max = f"{max_price_per_night:,}".replace(",", ".")
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới {formatted_max}đ/đêm. "
            "Hãy thử tăng ngân sách."
        )

    sorted_hotels = sorted(filtered_hotels, key=lambda x: x["rating"], reverse=True)

    result = f"Tìm thấy {len(sorted_hotels)} khách sạn tại {city} phù hợp với yêu cầu:\n"
    result += "=" * 60 + "\n"

    for h in sorted_hotels:
        p_str = f"{h['price_per_night']:,}".replace(",", ".") + "đ"
        stars_str = "⭐" * h["stars"]

        result += f"   - Tên: {h['name'].upper()}\n"
        result += f"   - Hạng: {stars_str} ({h['stars']} sao)\n"
        result += f"   - Khu vực: {h['area']}\n"
        result += f"   - Giá: {p_str}/đêm\n"
        result += f"   - Đánh giá: {h['rating']}/5.0\n"
        result += "-" * 30 + "\n"

    return result
