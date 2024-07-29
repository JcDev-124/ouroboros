class Question:
    def __init__(self, question, function, values, answer):
        self.question = question
        self.function = function
        self.values = values
        self.answer = answer

    def __repr__(self):
        return f"Question(question='{self.question}', function='{self.function}', values={self.values}, answer='{self.answer}')"
