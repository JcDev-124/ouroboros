from service.FunctionService import FunctionService
from domain.CharacterHealer import CharacterHealer
from domain.CharacterTank import CharacterTank
from domain.CharacterDamage import CharacterDamage
from domain.Character import Character

from domain.questions.Questions import Questions

if __name__ == "__main__":
    print("\nTESTE DAS FUNÇÕES\n")
    print('Soma:', FunctionService.sum(5, 9))               # Esperado: 14
    print('Subtração:', FunctionService.subtraction(15, 9))  # Esperado: 6
    print('Multiplicação:', FunctionService.multiplication(10, 3))  # Esperado: 30
    print('Potência:', FunctionService.pow(3, 3))           # Esperado: 27
    print('Fatorial:', FunctionService.factorial(5))        # Esperado: 120
    print('Divisão Teto:', FunctionService.roofDivision(10, 3))  # Esperado: 4
    print('Divisão Piso:', FunctionService.floorDivision(10, 3))  # Esperado: 3
    print('Porcentagem:', FunctionService.percentage(20, 50))  # Esperado: 10 (20% de 50 é 10)
    print('Módulo:', FunctionService.modulus(10, 3))         # Esperado: 1 (10 % 3 é 1)
    print("------------------------------------------\n")
    character_healer = CharacterHealer("[Forch]", 200, 4)
    character_damage = CharacterDamage("[Echelon]", 200, 4)
    character_tank = CharacterTank("Felcra", 200, 4)
    character_tank2 = CharacterTank("Gustavinho", 1000, 0)

    print("TESTE BASICO DE ATAQUES\n")
    print("Vida antes do ataque:", character_healer.get_hp())
    character_damage.heavy_attack(100, character_healer)
    print("Vida depois do ataque", character_healer.get_hp())
    print("Ta vivo?", character_healer.is_alive())
    character_damage.heavy_attack(100, character_healer)
    print("Ta vivo?", character_healer.is_alive())
    print("------------------------------------------\n")


    print("TESTE ULTIMATE TANQUE\n")

    try:
        character_damage.heavy_attack(5000, character_tank)
    except ValueError as e:
        print(e)

    character_damage.heavy_attack(100, character_tank)
    character_damage.heavy_attack(100, character_tank)
    print("Ta vivo?", character_tank.is_alive())
    print("Vida depois do ataque", character_tank.get_hp())
    print("------------------------------------------\n")

    print("TESTE ULTIMATE CURA\n")
    print("Vida antes da cura", character_healer.get_hp())
    character_healer.ult_attack()
    print("Vida depois da cura", character_healer.get_hp())
    print("------------------------------------------\n")

    print("TESTE ULTIMATE DAMAGE\n")
    character_tank2.shield = False
    print("Vida antes do ataque", character_tank2.get_hp())
    character_damage.ult_attack(100, character_tank2)
    print("Vida depois do ataque", character_tank2.get_hp())
    print("------------------------------------------\n")

    print("TESTE OBTER PERGUNTA\n")
    questions = Questions()
    print(questions.get_question('easy'))
    print(questions.get_question('normal'))
    print(questions.get_question('hard'))
    print(questions.get_question('ultimate'))
    print("------------------------------------------\n")

    #to do: criar uma classe para validar as respostas. recebe como parâmetro
    # a pergunta e a resposta dada pelo jogador e retorna 'True' para 
    # correto ou 'False' caso incorreto.

    



