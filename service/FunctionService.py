class FunctionService:
    def sum(x, y):
        if y == 0:
            return x
        else:
            return next(sum(x, y - 1)) 

    def subtraction(self):
        pass

    def multiplication(self):
        pass

    def potentiation(self):
        pass

    def factorial(self):
        pass

    def roofDivision(self):
        pass

    def floorDivision(self):
        pass

    def percentage(self):
        pass

    def module(self):
        pass
    
    def __next(x):
        return x + 1