import time
import random


OPENING_SCRIPTS = [
    "Ê khoan đi đã, bạn vừa vào live này là có duyên đó. MINI không bán hàng, chỉ nói chuyện cho vui thôi.",
    "Chào mọi người, MINI đang livestream nè. Ai vào thì comment một tiếng để MINI biết nhaa."
]

ALL_QUESTIONS = [
    "Ủa sao im ru vậy ta, có ai ở đây không nè?",
    "Mọi người ơi, vào nói chuyện với MINI đi mà.",
    "Nếu bây giờ cho bạn 10 triệu, bạn sẽ nghỉ làm hay vẫn đi làm?",
    "Bạn nghĩ tiền quan trọng hay hạnh phúc quan trọng hơn?",
    "Bạn thích sống một mình hay sống chung với ai đó?",
    "MINI đang tò mò lắm, mọi người ơi vào comment với MINI đi mà.",
    "Ai đang xem mà chưa comment thì comment đi, MINI muốn biết tên bạn nè.",
    "Nếu được quay lại quá khứ, bạn muốn thay đổi điều gì?",
    "Cuối tuần rồi mọi người có đi chơi đâu không?",
    "Có điều gì bí mật mà bạn chưa kể cho ai nghe không?",
    "Bạn thích trời mưa hay trời nắng hơn?",
    "Nếu trúng số 1 tỷ, bạn sẽ làm gì đầu tiên?",
    "Crush của bạn biết bạn thích họ chưa?",
    "Bạn thích ăn mặn hay ăn ngọt?",
    "Có ai đang ở một mình không, giơ tay lên nào?",
    "Điều gì khiến bạn cười nhiều nhất gần đây?",
    "Bạn thích đi biển hay đi núi hơn?",
    "Người yêu lý tưởng của bạn phải như thế nào?",
    "Bạn có tin vào định mệnh không?",
    "Điều bạn sợ nhất trên đời là gì?",
    "Nếu chỉ được ăn 1 món suốt đời, bạn chọn món gì?",
    "Bạn thích sáng sớm hay đêm khuya hơn?",
    "Điều bạn hối hận nhất trong đời là gì?",
    "Bạn thích một mình hay ở chỗ đông người?"
]


class AutoQuestion:
    def __init__(self):
        self.last_activity_time = 0
        self.last_question_time = 0
        self.silence_interval = 15
        self.used_questions = set()
        
    def update_activity(self):
        self.last_activity_time = time.time()
        
    def get_opening_script(self) -> str:
        return random.choice(OPENING_SCRIPTS)
    
    def _get_question(self) -> str:
        """Lấy câu hỏi không lặp"""
        available = [q for q in ALL_QUESTIONS if q not in self.used_questions]
        
        if not available:
            self.used_questions.clear()
            available = ALL_QUESTIONS
        
        question = random.choice(available)
        self.used_questions.add(question)
        return question
    
    def check_and_get_question(self) -> str:
        if self.last_activity_time == 0:
            return None
            
        elapsed = time.time() - self.last_activity_time
        question_elapsed = time.time() - self.last_question_time
        
        if elapsed >= self.silence_interval and question_elapsed >= self.silence_interval:
            self.last_question_time = time.time()
            return self._get_question()
            
        return None
