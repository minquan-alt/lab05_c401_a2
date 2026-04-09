from langchain_core.tools import tool

# ==============================================================================
# FLIGHTS_DB
# ==============================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố."""

    key = (origin, destination)

    if key in FLIGHTS_DB:
        flights = FLIGHTS_DB[key]
        message_title = f"Chuyến bay từ {origin} đến {destination}:\n"
    else:
        reverse_key = (destination, origin)
        if reverse_key in FLIGHTS_DB:
            flights = FLIGHTS_DB[reverse_key]
            message_title = (
                f"Không tìm thấy chuyến bay từ {origin} đi {destination}.\n"
                f"=> Gợi ý chiều ngược lại ({destination} -> {origin}):\n"
            )
        else:
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    formatted_flights = [message_title]
    for idx, flight in enumerate(flights, 1):
        price_str = f"{flight['price']:,}".replace(",", ".") + "đ"
        info = (
            f"  {idx}. {flight['airline']} | "
            f"{flight['departure']} - {flight['arrival']} | "
            f"Hạng {flight['class']} | "
            f"Giá: {price_str}"
        )
        formatted_flights.append(info)

    return "\n".join(formatted_flights)
