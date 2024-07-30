from service.FunctionService import FunctionService
class Question:
    def __init__(self, question, function, values, answer):
        self.question = question
        self.function = function
        self.values = values
        self.answer = answer


    #Tem um modo mais otimizado, porem precisavamos utilizar as funcoes recursivas criadas por nós, rsrs :(
    def validate_answer(self, user_answer):

        functionService = FunctionService()
        if isinstance(self.answer, int):
            return int(user_answer) == self.answer

        if self.function == 'sum':
            return user_answer.lower() == functionService.sum(self.values)
        if self.function == 'subtraction':
            return user_answer.lower() == functionService.subtraction(self.values)
        if self.function == 'multiplication':
            return user_answer.lower() == functionService.multiplication(self.values)
        if self.function == 'pow':
            return user_answer.lower() == functionService.pow(self.values)
        if self.function == 'factorial':
            return user_answer.lower() == functionService.factorial(self.values)
        if self.function == 'roofDivison':
            return user_answer.lower() == functionService.roofDivision(self.values)
        if self.function == 'floorDivison':
            return user_answer.lower() == functionService.floorDivision(self.values)
        if self.function == 'percentage':
            return user_answer.lower() == functionService.percentage(self.values)
        if self.function == 'modulus':
            return user_answer.lower() == functionService.modulus(self.values)
        if self.function == 'max':
            return user_answer.lower() == max(self.values)
        if self.function == 'min':
            return user_answer.lower() == min(self.values)
        if self.function == 'none':
            return user_answer.lower() == self.answer





    def __repr__(self):
        return f"Question(question='{self.question}', function='{self.function}', values={self.values}, answer='{self.answer}')"
