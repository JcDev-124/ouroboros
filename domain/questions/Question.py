class Question:
    def __init__(self, question, function, values, answer):
        self.question = question
        self.function = function
        self.values = values
        self.answer = answer

    def validate_answer(self, user_answer):
        if isinstance(self.answer, int):
            return int(user_answer) == self.answer
        return user_answer.lower() == self.answer.lower()

    def __repr__(self):
        return f"Question(question='{self.question}', function='{self.function}', values={self.values}, answer='{self.answer}')"
