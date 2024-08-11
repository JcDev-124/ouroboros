class FunctionService:
    @staticmethod
    def sum(x, y):
        if y == 0:
            return x
        else:
            return FunctionService.__next(FunctionService.sum(x, (y - 1)))

    @staticmethod
    def subtraction(x,y):
        if y == 0:
            return x
        else:
            return FunctionService.subtraction(FunctionService.__prev(x), (y - 1))

    @staticmethod
    def multiplication(x, y):
        if y == 0:
            return 0
        else:
            return FunctionService.sum(x, FunctionService.multiplication(x, (y - 1)))

    @staticmethod
    def pow(x, pow):
        if pow == 0:
            return 1
        else:
            return FunctionService.multiplication(x, FunctionService.pow(x, (pow - 1)))

    @staticmethod
    def factorial(x):
        if x == 0:
            return 1
        else:
            return FunctionService.multiplication(x, FunctionService.factorial((x - 1)))

    @staticmethod
    def roofDivision(x, y):
        if y == 0:
            raise ValueError("Divisor não pode ser zero")
        result = FunctionService.floorDivision(x, y)
        if FunctionService.multiplication(result, y) == x:
            return result
        else:
            return FunctionService.__next(result)

    @staticmethod
    def floorDivision(x, y):
        if y == 0:
            raise ValueError("Divisor não pode ser zero")
        if x < y:
            return 0
        else:
            return FunctionService.__next(FunctionService.floorDivision(FunctionService.subtraction(x, y), y))

    @staticmethod
    def percentage(x, y):
        return FunctionService.floorDivision(FunctionService.multiplication(x, y), 100)

    @staticmethod
    def modulus(x, y):
        if y == 0:
            raise ValueError("Divisor não pode ser zero")
        if x < y:
            return x
        else:
            return FunctionService.modulus(FunctionService.subtraction(x, y), y)

    def max(self, x, y):
        if FunctionService.subtraction(x, y) >= 0:
            return x
        else:
            return y

    def min(self, x, y):
        if FunctionService.subtraction(x, y) <= 0:
            return x
        else:
            return y

    def equal(self, x, y):
        return FunctionService.subtraction(x, y) == 0

    def different(self, x, y):
        return FunctionService.subtraction(x,y) != 0

    @staticmethod
    def __next(x):
        return (x + 1)

    @staticmethod
    def __prev(x):
        return (x - 1)