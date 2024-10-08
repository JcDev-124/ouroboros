from service.FunctionService import FunctionService
class Question:
    def __init__(self, question, function, values, answer):
        self.question = question
        self.function = function
        self.values = values
        self.answer = answer

    def validate_answer(self, user_answer):
        functionService = FunctionService()

        if isinstance(self.answer, int):
            return str(user_answer) == str(self.answer)

        elif isinstance(self.answer, str):
            if isinstance(user_answer, str):
                return user_answer[0].lower() == self.answer[0].lower()
            else:
                return False

        function_map = {
            'sum': functionService.sum,
            'subtraction': functionService.subtraction,
            'multiplication': functionService.multiplication,
            'pow': functionService.pow,
            'factorial': functionService.factorial,
            'roofDivision': functionService.roofDivision,
            'floorDivision': functionService.floorDivision,
            'percentage': functionService.percentage,
            'modulus': functionService.modulus,
            'max': functionService.max,
            'min': functionService.min
        }

        if self.function in function_map:
            result = function_map[self.function](self.values)
            return functionService.equal(user_answer.lower(), result)

        if self.function == 'none':
            return functionService.equal(user_answer.lower(), self.answer)

    def __repr__(self):
        return f"Question(question='{self.question}', function='{self.function}', values={self.values}, answer='{self.answer}')"
