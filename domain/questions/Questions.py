import random

from domain.questions.Question import Question

class Questions:


    def __init__(self):
        self.questions_easy = [
            Question(
                question="Qual o resultado de soma(2, 3)?",
                function="sum",
                values=(2, 3),
                answer=5
            ),
            Question(
                question="Qual o resultado de subtracao(5, 2)?",
                function="subtraction",
                values=(5, 2),
                answer=3
            ),
            Question(
                question="Qual o resultado de multiplicacao(3, 2)?",
                function="multiplication",
                values=(3, 2),
                answer=6
            ),
            Question(
                question="Qual o resultado de fatorial(3)?",
                function="factorial",
                values=(3,),
                answer=6
            ),
            Question(
                question="Qual o resultado de divisão_chão(9, 2)?",
                function="floorDivision",
                values=(9, 2),
                answer=4
            ),
            Question(
                question="Qual a função primitiva usada para definir a função soma?\n a) Zero\n b) Sucessor\n c) Projeção\n d) Recursão",
                function="none",
                values=(),
                answer="b"
            )
        ]
        
        self.questions_normal = [
            Question(
                question="Qual o resultado de elevado(2, 3)?",
                function="pow",
                values=(2, 3),
                answer=8
            ),
            Question(
                question="Qual o resultado de fatorial(4)?",
                function="factorial",
                values=(4,),
                answer=24
            ),
            Question(
                question="Qual o resultado de divisão_teto(7, 3)?",
                function="roofDivision",
                values=(7, 3),
                answer=3
            ),
            Question(
                question="Qual o resultado de resto_divisao(10, 3)?",
                function="modulus",
                values=(10, 3),
                answer=1
            ),
            Question(
                question="Qual o resultado de máximo(5, 7)?",
                function="max",
                values=(5, 7),
                answer=7
            ),
            Question(
                question="Qual a função primitiva usada para definir a função multiplicacao?\n a) Soma\n b) Subtracao\n c) Fatorial\n d) Máximo",
                function="none",
                values=(),
                answer="a"
            )
        ]
        
        self.questions_hard = [
            Question(
                question="Qual o resultado de percentual(50, 20)?",
                function="percentage",
                values=(50, 20),
                answer=10
            ),
            Question(
                question="Qual o resultado de fatorial(5)?",
                function="factorial",
                values=(5,),
                answer=120
            ),
            Question(
                question="Qual o resultado de divisão_chão(15, 4)?",
                function="floorDivision",
                values=(15, 4),
                answer=3
            ),
            Question(
                question="Qual o resultado de mínimo(12, 9)?",
                function="min",
                values=(12, 9),
                answer=9
            ),
            Question(
                question="Esta pilha de recursão corresponde a qual função? [Pilha: soma(2, soma(2, 0))]\n a) soma\n b) subtracao\n c) multiplicacao\n d) fatorial",
                function="none",
                values=(),
                answer="a"
            ),
            Question(
                question="Qual a função primitiva usada para definir a função fatorial?\n a) Soma\n b) Multiplicacao\n c) Subtracao\n d) Máximo",
                function="none",
                values=(),
                answer="b"
            )
        ]
        
        self.questions_ultimate = [
            Question(
                question="Qual o resultado de elevado(3, 4)?",
                function="pow",
                values=(3, 4),
                answer=81
            ),
            Question(
                question="Qual o resultado de divisão_teto(25, 6)?",
                function="roofDivision",
                values=(25, 6),
                answer=5
            ),
            Question(
                question="Qual o resultado de máximo(18, 20)?",
                function="max",
                values=(18, 20),
                answer=20
            ),
            Question(
                question="Esta pilha de recursão corresponde a qual função? [Pilha: fatorial(3, multiplicacao(2, fatorial(1)))]\n a) multiplicacao\n b) subtracao\n c) soma\n d) fatorial",
                function="none",
                values=(),
                answer="d"
            ),
            Question(
                question="Qual a função primitiva usada para definir a função divisão_chão?\n a) Subtracao\n b) Soma\n c) Máximo\n d) Mínimo",
                function="none",
                values=(),
                answer="a"
            ),
            Question(
                question="Esta pilha de recursão corresponde a qual função? [Pilha: subtracao(7, subtracao(3, 1))]\n a) subtracao\n b) soma\n c) multiplicacao\n d) fatorial",
                function="none",
                values=(),
                answer="a"
            )
        ]
    
    def get_question(self, level):
        if level == 'easy':
            question = random.choice(self.questions_easy)
        elif level == 'normal':
            question = random.choice(self.questions_normal)
        elif level == 'hard':
            question = random.choice(self.questions_hard)
        elif level == 'ultimate':
            question = random.choice(self.questions_ultimate)
        else:
            return "Invalid difficulty level. Choose between 'easy', 'normal', 'hard', or 'ultimate'."
        
        return question

    def ask_question(self, level, userAnswer):
        questions = Questions()
        question = questions.get_question(level)

        if isinstance(question, str):
            print(question)
            return

        print(question.question)

        if question.validate_answer(userAnswer):
            return True
        else:
            return False