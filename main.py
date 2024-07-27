from service.FunctionService import FunctionService
from domain.Character import  Character

if __name__ == "__main__":
    print('Soma:', FunctionService.sum(5, 9))               # Esperado: 14
    print('Subtração:', FunctionService.subtraction(15, 9))  # Esperado: 6
    print('Multiplicação:', FunctionService.multiplication(10, 3))  # Esperado: 30
    print('Potência:', FunctionService.pow(3, 3))           # Esperado: 27
    print('Fatorial:', FunctionService.factorial(5))        # Esperado: 120
    print('Divisão Teto:', FunctionService.roofDivision(10, 3))  # Esperado: 4
    print('Divisão Piso:', FunctionService.floorDivision(10, 3))  # Esperado: 3
    print('Porcentagem:', FunctionService.percentage(20, 50))  # Esperado: 10 (20% de 50 é 10)
    print('Módulo:', FunctionService.modulus(10, 3))         # Esperado: 1 (10 % 3 é 1)

    character = Character("PedrinhoBoiola", 100, 0)
