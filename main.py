from service.FunctionService import FunctionService

if __name__ == "__main__":

    print('Soma:', FunctionService.sum(5, 9))
    print('Mult:', FunctionService.multiplication(10, 3))
    print('Pow:', FunctionService.pow(3, 3))
    print('Factorial:', FunctionService.factorial(5))