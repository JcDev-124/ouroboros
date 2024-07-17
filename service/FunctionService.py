class FunctionService:
    @staticmethod
    def sum(x, y):
        if y == 0:
            return x
        else:
            return FunctionService.__next(FunctionService.sum(x, (y - 1))) 

    def subtraction(self):
        pass

    def multiplication(x, y):
        if y == 0:
            return 0
        else:
            return FunctionService.sum(x, FunctionService.multiplication(x, (y - 1)))

    def pow(x, pow):
        if pow == 0:
            return 1
        else:
            return FunctionService.multiplication(x, FunctionService.pow(x, (pow - 1)))

    def factorial(x):
        if x == 0:
            return 1
        else:
            return FunctionService.multiplication(x, FunctionService.factorial((x - 1)))

    def roofDivision(self):
        pass

    def floorDivision(self):
        pass

    def percentage(self):
        pass

    def module(self):
        pass
    
    def __next(x):
        return (x + 1)