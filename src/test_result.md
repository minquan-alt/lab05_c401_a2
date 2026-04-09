## Test Case 2
```console

Bạn:  tìm chuyến bay  Hà  nội  đi  đà nẵng 

TravelBuddy đang suy nghĩ...

[DEBUG] response.tool_calls: []
[DEBUG] response.content (100 chars): '{"name": "search_flights", "arguments": {"origin": "Hà Nội", "destination": "Đà Nẵng"}}'

🔧 [Fallback] Chuyển hướng sang ToolNode: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})

[DEBUG] response.tool_calls: []
[DEBUG] response.content (100 chars): 'Chuyến bay:\n1. Vietnam Airlines | 06:00 - 07:20 | Hạng economy | Giá: 1.450.000đ\n2. Vietnam Airlines'

💬 Trả lời trực tiếp

TravelBuddy: Chuyến bay:
1. Vietnam Airlines | 06:00 - 07:20 | Hạng economy | Giá: 1.450.000đ
2. Vietnam Airlines | 14:00 - 15:20 | Hạng business | Giá: 2.800.000đ
3. VietJet Air | 08:30 - 09:50 | Hạng economy | Giá: 890.000đ
4. Bamboo Airways | 11:00 - 12:20 | Hạng economy | Giá: 1.200.000đ

Gợi ý thêm: Bạn có thể chọn chuyến bay giá rẻ nhất là VietJet Air với 890.000đ hoặc Vietnam Airlines với 1.450.000đ, tùy thuộc vào nhu cầu và ngân sách của bạn.

```

## Test Case 1

```

Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...

[DEBUG] response.tool_calls: []
[DEBUG] response.content (100 chars): 'Chào bạn! Rất vui được giúp bạn lên kế hoạch cho chuyến du lịch sắp tới. Bạn có ý định đi đến những '

💬 Trả lời trực tiếp

TravelBuddy: Chào bạn! Rất vui được giúp bạn lên kế hoạch cho chuyến du lịch sắp tới. Bạn có ý định đi đến những nơi nào không? Nếu chưa, tôi có thể gợi ý một số địa điểm nổi tiếng ở Việt Nam mà bạn có thể tham khảo:

1. **Hà Nội**: Thành phố cổ kính với nhiều di tích lịch sử và văn hóa.
2. **Đà Nẵng**: Biển Mỹ Khê, Đà Lạt, và nhiều địa điểm du lịch hấp dẫn khác.
3. **Phú Quốc**: Du lịch biển, trải nghiệm phong cảnh thiên nhiên tuyệt đẹp.
4. **Hồ Chí Minh**: Thành phố hiện đại với nhiều công trình kiến trúc độc đáo.

Bạn có muốn tôi gợi ý một địa điểm cụ thể không? Hoặc bạn có yêu cầu đặc biệt nào khác?


```

## Test Case 3

```

Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...

--- Iteration 1/5 ---
[DEBUG] tool_calls: []
[DEBUG] content (100 chars): 'Chào bạn! Rất vui được tư vấn cho chuyến đi của bạn.\n\nĐầu tiên, tôi sẽ tìm kiếm vé máy bay từ Hà Nội'
🔧 [Fallback] Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
📦 Kết quả:
Chuyến bay từ Hà Nội đến Phú Quốc:

  1. Vietnam Airlines | 07:00 - 09:15 | Hạng economy | Giá: 2.100.000đ
  2. VietJet Air | 10:00 - 12:15 | Hạng economy | Giá: 1.350.000đ
  3. VietJet Air | 16:00 - 18:15 | Hạng economy | Giá: 1.100.000đ


--- Iteration 2/5 ---
[DEBUG] tool_calls: []
[DEBUG] content (100 chars): 'Chào bạn! Tôi đã tìm được các chuyến bay từ Hà Nội đến Phú Quốc:\n\n  1. Vietnam Airlines | 07:00 - 09'
🔧 [Fallback] Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:2100000'})
📦 Kết quả:
📋 Bảng chi phí:
  - Vé Máy Bay: 2.100.000đ
  ---
  Tổng chi:  2.100.000đ
  Ngân sách: 5.000.000đ
  Còn lại:   2.900.000đ ✅


--- Iteration 3/5 ---
[DEBUG] tool_calls: []
[DEBUG] content (100 chars): 'Chào bạn! Tôi đã tính toán ngân sách còn lại sau khi trừ chi phí vé máy bay:\n\n📋 Bảng chi phí:\n  - Vé'
🔧 [Fallback] Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1458})
📦 Kết quả:
Không tìm thấy khách sạn tại Phú Quốc với giá dưới 1.458đ/đêm. Hãy thử tăng ngân sách.


--- Iteration 4/5 ---
[DEBUG] tool_calls: []
[DEBUG] content (100 chars): 'Chào bạn! Rất tiếc là tôi không tìm thấy khách sạn phù hợp với ngân sách của bạn. Bạn có thể thử tăn'
💬 Trả lời trực tiếp (kết thúc vòng lặp)

TravelBuddy: Chào bạn! Rất tiếc là tôi không tìm thấy khách sạn phù hợp với ngân sách của bạn. Bạn có thể thử tăng ngân sách lên một chút để tìm được lựa chọn tốt hơn.

Nếu bạn muốn giữ ngân sách 5 triệu, tôi có thể đề xuất cho bạn một số điểm du lịch khác ở Phú Quốc mà chi phí sẽ thấp hơn:

1. Bà Nà Hills: Khu vui chơi giải trí lớn với nhiều trò chơi và hoạt động thú vị.
2. Cát trắng: Địa điểm nổi tiếng với bãi biển đẹp và các hoạt động biển như tắm, câu cá.
3. Nhà hàng địa phương: Thử những món ăn ngon miệng của vùng biển.

Bạn có muốn tôi giúp bạn lên kế hoạch cho một trong những điểm du lịch này không?

```

## Test Case 4
```
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...

[DEBUG] response.tool_calls: []
[DEBUG] response.content (100 chars): 'Để tìm kiếm khách sạn phù hợp, tôi cần biết thành phố bạn muốn ở và ngân sách của bạn. Bạn có thể cu'

💬 Trả lời trực tiếp

TravelBuddy: Để tìm kiếm khách sạn phù hợp, tôi cần biết thành phố bạn muốn ở và ngân sách của bạn. Bạn có thể cung cấp thêm thông tin không?

```


## Test Case 5

```
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...

[DEBUG] response.tool_calls: []
[DEBUG] response.content (100 chars): 'Tôi xin lỗi vì đã gây hiểu lầm, nhưng tôi không thể giúp bạn với yêu cầu đó. Tôi là trợ lý du lịch c'

💬 Trả lời trực tiếp

TravelBuddy: Tôi xin lỗi vì đã gây hiểu lầm, nhưng tôi không thể giúp bạn với yêu cầu đó. Tôi là trợ lý du lịch của TravelBuddy và chuyên về tư vấn du lịch Việt Nam dựa trên ngân sách thực tế của khách hàng. Nếu bạn có câu hỏi liên quan đến du lịch hoặc cần hỗ trợ trong việc lên kế hoạch chuyến đi, tôi sẽ rất vui lòng giúp đỡ!

```
