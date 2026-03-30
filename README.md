# 🎀 MINI AI - TikTok Livestream Bot

Bot AI tự động tương tác với người xem trên TikTok Livestream, sử dụng AI để trả lời bình luận, chào mừng người xem, và phát nhạc theo yêu cầu.

## ✨ Tính năng chính

- 🤖 **Trả lời tự động**: AI trả lời bình luận của người xem bằng tiếng Việt
- 👋 **Chào mừng người xem**: Tự động chào khi có người vào live
- 🎵 **Phát nhạc theo yêu cầu**: Người xem có thể yêu cầu mở nhạc
- 🎁 **Cảm ơn quà tặng**: Tự động cảm ơn khi nhận được quà
- 💬 **Hỏi tự động**: Bot tự động đặt câu hỏi khi không có tương tác
- 🔊 **Text-to-Speech**: Chuyển đổi văn bản thành giọng nói tự nhiên
- 🎭 **VSeeFace Integration**: Tích hợp với VSeeFace để hiển thị avatar 3D

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- Windows (khuyến nghị)
- Ollama (để chạy AI model)
- VSeeFace (tùy chọn, để hiển thị avatar)

## 🚀 Cài đặt

### 1. Clone hoặc tải dự án về

```bash
git clone <repository-url>
cd LIVESTREEM
```

### 2. Cài đặt Python dependencies

```bash
pip install -r requirements.txt
```

Các thư viện cần thiết:
- `customtkinter` - Giao diện người dùng
- `TikTokLive` - Kết nối với TikTok Livestream
- `edge-tts` - Text-to-Speech của Microsoft
- `pygame` - Phát nhạc

### 3. Cài đặt Ollama và AI Model

1. Tải và cài đặt Ollama từ: https://ollama.ai
2. Tải model AI (mặc định: qwen2.5:32b):

```bash
ollama pull qwen2.5:32b
```

Bạn có thể thay đổi model trong file `config/ai.json`

### 4. Cài đặt VSeeFace (Tùy chọn)

Nếu muốn sử dụng avatar 3D, tải VSeeFace và đặt vào thư mục `VSeeFace/`

## ⚙️ Cấu hình

### File cấu hình trong thư mục `config/`:

#### `config/ai.json`
```json
{
  "model": "qwen2.5:32b"
}
```
- Thay đổi model AI tại đây

#### `config/system.json`
```json
{
  "language": "vi",
  "debug": true
}
```
- `language`: Ngôn ngữ (vi = tiếng Việt)
- `debug`: Bật/tắt chế độ debug

#### `config/tts.json`
- Cấu hình giọng đọc Text-to-Speech

#### `config/session.json`
- Lưu thông tin phiên làm việc

## 🎮 Sử dụng

### 1. Khởi động ứng dụng

```bash
python Tiktok.py
```

### 2. Đăng nhập TikTok Live

1. Mở ứng dụng
2. Nhập username TikTok của bạn
3. Nhấn "Kết nối"

### 3. Các chức năng chính

#### Trả lời bình luận
- Bot tự động đọc và trả lời bình luận của người xem
- Sử dụng AI để tạo câu trả lời tự nhiên

#### Phát nhạc
- Người xem có thể yêu cầu mở nhạc
- Người tặng quà sẽ nhận được lượt mở nhạc miễn phí
- File nhạc đặt trong thư mục `mp3/`

#### Hỏi tự động
- Khi không có tương tác, bot sẽ tự động đặt câu hỏi
- Giúp duy trì sự sôi động của livestream

## 📁 Cấu trúc dự án

```
LIVESTREEM/
├── ai/                      # Module AI
│   ├── responder.py        # Xử lý trả lời AI
│   ├── auto_question.py    # Hỏi tự động
│   ├── music_player.py     # Quản lý phát nhạc
│   ├── comment_queue.py    # Hàng đợi bình luận
│   └── storyteller.py      # Kể chuyện
├── tiktok/                  # Module TikTok
│   ├── client.py           # Kết nối TikTok Live
│   ├── events.py           # Xử lý sự kiện
│   └── filters.py          # Lọc spam
├── tts/                     # Module Text-to-Speech
│   ├── tts_engine.py       # Engine TTS
│   └── voice_manager.py    # Quản lý giọng nói
├── giaodien/                # Giao diện người dùng
│   ├── main_ui.py          # Giao diện chính
│   ├── settings_ui.py      # Cài đặt
│   └── live_view.py        # Hiển thị live
├── config/                  # File cấu hình
├── mp3/                     # Thư mục nhạc
│   ├── replies/            # Nhạc trả lời
│   ├── stories/            # Nhạc kể chuyện
│   └── system/             # Nhạc hệ thống
├── logs/                    # File log
├── VSeeFace/               # VSeeFace (tùy chọn)
├── Tiktok.py               # File chính
└── requirements.txt        # Dependencies
```

## 🔧 Tùy chỉnh

### Thay đổi AI Model

Chỉnh sửa `config/ai.json`:
```json
{
  "model": "llama2"
}
```

Các model khuyến nghị:
- `qwen2.5:32b` - Tốt cho tiếng Việt
- `llama2` - Nhẹ hơn
- `mistral` - Cân bằng

### Thêm nhạc

Đặt file MP3 vào các thư mục trong `mp3/`:
- `mp3/replies/` - Nhạc nền khi trả lời
- `mp3/stories/` - Nhạc khi kể chuyện
- `mp3/system/` - Nhạc hệ thống

### Tùy chỉnh giọng nói

Chỉnh sửa `config/tts.json` để thay đổi giọng đọc

## 🐛 Xử lý lỗi

### Lỗi kết nối TikTok
- Kiểm tra username có đúng không
- Đảm bảo đang livestream
- Thử kết nối lại

### Lỗi AI không trả lời
- Kiểm tra Ollama đã chạy chưa: `ollama serve`
- Kiểm tra model đã tải: `ollama list`
- Xem log trong `logs/system.log`

### Lỗi TTS không đọc
- Kiểm tra kết nối internet
- Thử khởi động lại ứng dụng

## 📝 Lưu ý

- Bot chỉ hoạt động khi bạn đang livestream
- Cần kết nối internet để sử dụng TTS
- Ollama cần chạy trong background
- Không spam quá nhiều tin nhắn

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo Pull Request hoặc báo lỗi qua Issues.

## 📄 License

Dự án này được phát hành dưới giấy phép MIT.

## 💡 Tips

- Sử dụng model AI nhẹ hơn nếu máy yếu
- Tắt debug mode trong production để tăng hiệu suất
- Backup file cấu hình trước khi cập nhật
- Kiểm tra log thường xuyên để phát hiện lỗi

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra file log trong `logs/system.log`
2. Đọc phần Xử lý lỗi ở trên
3. Tạo Issue trên GitHub với thông tin chi tiết

---

Chúc bạn livestream vui vẻ! 🎉
"# PYTHON-TIKTOKLIVE" 
