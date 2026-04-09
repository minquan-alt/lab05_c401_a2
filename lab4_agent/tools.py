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
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu FLIGHTS_DB với key (origin, destination)
    # - Nếu tìm thấy -> format danh sách chuyến bay dễ đọc, bao gồm giá tiền
    # - Nếu không tìm thấy -> thử tra ngược (destination, origin) xem có không,
    #   nếu cũng không có -> "Không tìm thấy chuyến bay từ X đến Y."
    # - Gợi ý: format giá tiền có dấu chấm phân cách (1.450.000đ)
    

    # 1. Bắt đầu với việc tìm kiếm chiều đi yêu cầu  
    key = (origin, destination)
    
    if key in FLIGHTS_DB:
        flights = FLIGHTS_DB[key]
        message_title = f"Chuyến bay từ {origin} đến {destination}:\n"
    else:
        # 2. Thử tra chiều ngược lại nếu không có chiều đi
        reverse_key = (destination, origin)
        if reverse_key in FLIGHTS_DB:
            flights = FLIGHTS_DB[reverse_key]
            # Báo cho người dùng biết chiều đi không có nhưng có chiều về
            message_title = f"Không tìm thấy chuyến bay từ {origin} đi {destination}.\n=> Gợi ý chiều ngược lại ({destination} -> {origin}):\n"
        else:
            # 3. Trả về thông báo không tìm thấy trong cả hai trường hợp
            return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # 4. Format danh sách thành chuỗi thân thiện
    formatted_flights = [message_title]
    for idx, flight in enumerate(flights, 1):
        # Xử lý giá tiền: Dùng định dạng hàng nghìn có dấu phẩy rồi thế phẩy thành chấm (VD: 1.450.000đ)
        price_str = f"{flight['price']:,}".replace(",", ".") + "đ"
        
        info = (
            f"  {idx}. {flight['airline']} | "
            f"{flight['departure']} - {flight['arrival']} | "
            f"Hạng {flight['class']} | "
            f"Giá: {price_str}"
        )
        formatted_flights.append(info)
        
    return "\n".join(formatted_flights)  
 



    

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # TODO: Sinh viên tự triển khai
    # - Tra cứu HOTELS_DB[city]
    # - Lọc theo max_price_per_night
    # - Sắp xếp theo rating giảm dần
    # - Format đẹp. Nếu không có kết quả -> "Không tìm thấy khách sạn tại X
    #   với giá dưới Y/đêm. Hãy thử tăng ngân sách."
    # 1. Kiểm tra xem thành phố có trong dữ liệu không
    if city not in HOTELS_DB:
        return f"Hiện tại chúng tôi không có dữ liệu khách sạn tại thành phố {city}."

    # 2. Lấy danh sách khách sạn của thành phố đó
    all_hotels = HOTELS_DB[city]

    # 3. Lọc theo giá tối đa (List Comprehension)
    filtered_hotels = [h for h in all_hotels if h['price_per_night'] <= max_price_per_night]

    # 4. Nếu không có khách sạn nào sau khi lọc
    if not filtered_hotels:
        # Định dạng giá tiền để thông báo cho dễ đọc
        formatted_max = f"{max_price_per_night:,}".replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {formatted_max}đ/đêm. Hãy thử tăng ngân sách."

    # 5. Sắp xếp theo rating giảm dần (Từ cao đến thấp)
    # reverse=True để đưa rating cao nhất lên đầu
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)

    # 6. Format kết quả trả về
    result = f"Tìm thấy {len(sorted_hotels)} khách sạn tại {city} phù hợp với yêu cầu:\n"
    result += "=" * 60 + "\n"

    for h in sorted_hotels:
        # Format giá tiền (VD: 1.500.000đ)
        p_str = f"{h['price_per_night']:,}".replace(",", ".") + "đ"
        
        # Tạo chuỗi sao (VD: 4 sao -> ****)
        stars_str = "⭐" * h['stars']
        
        result += f"   - Tên: {h['name'].upper()}\n"
        result += f"   - Hạng: {stars_str} ({h['stars']} sao)\n"
        result += f"   - Khu vực: {h['area']}\n"
        result += f"   - Giá: {p_str}/đêm\n"
        result += f"   - Đánh giá: {h['rating']}/5.0\n"
        result += "-" * 30 + "\n"

    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # 1. Parse chuỗi expenses thành dict {tên: số_tiền}
    # Định dạng input: 'vé_máy_bay:890000,khách_sạn:650000'
    expense_dict = {}
    try:
        for item in expenses.split(","):
            item = item.strip()
            if not item:
                continue  # Bỏ qua phần tử rỗng
            # Tách chuỗi thành tên và số tiền qua dấu ':'
            parts = item.split(":")
            if len(parts) != 2:
                return f"❌ Lỗi định dạng: '{item}' không đúng cú pháp 'tên:số_tiền'."
            name = parts[0].strip().replace("_", " ").title()  # 'vé_máy_bay' -> 'Vé Máy Bay'
            amount = int(parts[1].strip())  # Có thể raise ValueError nếu không phải số
            expense_dict[name] = amount
    except ValueError:
        return f"❌ Lỗi: Số tiền trong phần chi phí phải là số nguyên (không có ký tự đặc biệt)."

    # 2. Tính tổng chi phí
    total_spent = sum(expense_dict.values())

    # 3. Tính số tiền còn lại
    remaining = total_budget - total_spent

    # 4. Helper format số tiền
    def fmt(amount: int) -> str:
        return f"{abs(amount):,}".replace(",", ".") + "đ"

    # 5. Xây dựng bảng chi tiết
    lines = ["📋 Bảng chi phí:"]
    for name, amount in expense_dict.items():
        lines.append(f"  - {name}: {fmt(amount)}")

    lines.append("  ---")
    lines.append(f"  Tổng chi:  {fmt(total_spent)}")
    lines.append(f"  Ngân sách: {fmt(total_budget)}")

    # 6. Xử lý còn lại hoặc vượt ngân sách
    if remaining >= 0:
        lines.append(f"  Còn lại:   {fmt(remaining)} ✅")
    else:
        lines.append(f"  Còn lại:   -{fmt(remaining)}")
        lines.append(f"\n⚠️  Vượt ngân sách {fmt(remaining)} ! Cần điều chỉnh.")

    return "\n".join(lines)

# --- KẾT THÚC CODE tools.py ---