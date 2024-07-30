from service.FunctionService import FunctionService
from domain.characters.CharacterHealer import CharacterHealer
from domain.characters.CharacterTank import CharacterTank
from domain.characters.CharacterDamage import CharacterDamage

from domain.questions.Questions import Questions

from domain.player.Player import Player

from service.MatchService import MatchService

if __name__ == "__main__":
    print("\nTESTE DAS FUNÇÕES\n")
    print('Soma:', FunctionService.sum(5, 9))  # Esperado: 14
    print('Subtração:', FunctionService.subtraction(15, 9))  # Esperado: 6
    print('Multiplicação:', FunctionService.multiplication(10, 3))  # Esperado: 30
    print('Potência:', FunctionService.pow(3, 3))  # Esperado: 27
    print('Fatorial:', FunctionService.factorial(5))  # Esperado: 120
    print('Divisão Teto:', FunctionService.roofDivision(10, 3))  # Esperado: 4
    print('Divisão Piso:', FunctionService.floorDivision(10, 3))  # Esperado: 3
    print('Porcentagem:', FunctionService.percentage(20, 50))  # Esperado: 10 (20% de 50 é 10)
    print('Módulo:', FunctionService.modulus(10, 3))  # Esperado: 1 (10 % 3 é 1)
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
    # level = input("Escolha o nível da pergunta (easy, normal, hard, ultimate): ").lower()
    # print(questions.ask_question(level))
    print("------------------------------------------\n")

    print("TESTE JOGO\n")

    player1 = Player("Julio", character_damage)
    player2 = Player("Pedro", character_healer)
    player3 = Player("Maria", CharacterHealer("Maria", 100, 3))

    match = MatchService()
    match.addPlayer(player1)
    match.addPlayer(player2)
    match.addPlayer(player3)
    match.addPlayer(player1)

    match.startMatch()
    print("Primeiro agressor: ", match.attacker.playerId)
    print("Vida Player1: ", player1.getCharacter().hp)
    match.attack("light", 50, player1)
    print("Vida Player1 depois: ", player1.getCharacter().hp)
    print("------------------------------------------\n")
