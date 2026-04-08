# UX exercise — Vietnam Airlines NEO Assistant

## Sản phẩm: Vietnam Airlines — NEO AI Assistant (hỗ trợ hành trình & dịch vụ chuyến bay)

## 4 paths

### 1. AI đúng

* User hỏi “Tôi được mang bao nhiêu kg hành lý xách tay?”
* NEO nhận diện đúng hạng vé của user và trả lời “Bạn được mang 12kg hành lý xách tay”
* User thấy đúng, không cần làm gì thêm
* UI: hiện câu trả lời + icon hành lý, không cần confirm

### 2. AI không chắc

* User hỏi “Tôi có được đổi vé không?”
* NEO không chắc vì còn phụ thuộc vào loại vé, hạng ghế hoặc điều kiện hoàn đổi
* UI: chỉ hiện câu trả lời chung chung hoặc không trả lời được
* Vấn đề: không có cơ chế hỏi thêm như “Bạn đang dùng loại vé nào?” hoặc “Bạn muốn đổi ngày hay đổi tên?”

### 3. AI sai

* User hỏi “Tôi có được vào phòng chờ không?”
* NEO trả lời “Có” vì nhận diện user là hạng thương gia, nhưng thực tế vé user là phổ thông
* User chỉ phát hiện khi đến sân bay
* Sửa: phải vào chat lại → nhập thêm thông tin vé → nhận câu trả lời mới → mất nhiều bước
* Vấn đề: không rõ AI có học từ correction này không

### 4. User mất niềm tin

* Sau nhiều lần NEO trả lời sai hoặc quá chung chung, user không còn tin tưởng thông tin từ AI nữa
* User quay lại tự tìm trên website hoặc gọi tổng đài
* Không có option “chuyển sang nhân viên hỗ trợ” hoặc “hiển thị nguồn chính thức”
* Không có fallback rõ ràng ngoài việc user tự tra cứu lại

## Path yếu nhất: Path 3 + 4

* Khi AI trả lời sai, recovery flow mất quá nhiều bước
* Không có feedback loop rõ — user sửa hoặc cung cấp thêm thông tin nhưng không biết AI có học không
* Không có exit/fallback cho user mất niềm tin, ví dụ:

  * “Chuyển sang nhân viên hỗ trợ”
  * “Xem chính sách chính thức”
  * “Tạo yêu cầu hỗ trợ”

## Gap marketing vs thực tế

* Marketing: “NEO giúp bạn đồng hành suốt chuyến đi với câu trả lời nhanh và chính xác”
* Thực tế: AI chỉ xử lý tốt các câu hỏi phổ biến như hành lý, check-in, giờ bay
* Các trường hợp edge case như:

  * đổi vé nhiều chặng
  * hoàn vé quốc tế
  * nâng hạng bằng dặm
  * quyền lợi theo hạng hội viên
    thường dễ bị trả lời sai hoặc thiếu thông tin
* Gap lớn nhất: marketing không nói rõ AI có giới hạn và vẫn cần con người hỗ trợ ở các case phức tạp

## Sketch

* As-is: user hỏi → NEO trả lời → nếu sai user phải tự hỏi lại hoặc tự tra cứu
* To-be:

  * user hỏi → NEO trả lời
  * nếu confidence thấp: hiện “Bạn muốn cung cấp thêm thông tin vé để mình hỗ trợ chính xác hơn không?”
  * user bổ sung thông tin
  * NEO cập nhật câu trả lời
  * hiện thêm:

    * “Thông tin này dựa trên điều kiện vé của bạn”
    * “NEO đã ghi nhận phản hồi để cải thiện câu trả lời lần sau”
    * “Nếu cần, bạn có thể chuyển sang nhân viên hỗ trợ”
