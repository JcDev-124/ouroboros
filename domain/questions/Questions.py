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
                question="Qual o resultado de divisão chão(9, 2)?",
                function="floorDivision",
                values=(9, 2),
                answer=4
            ),
            Question(
                question="Qual a função primitiva usada para definir a função soma?\n a) Zero\n b) Sucessor\n c) Projeção\n d) Recursão",
                function="none",
                values=(),
                answer="b"
            ),
            Question(
                question="Qual o resultado de subtracao(7, 3)?",
                function="subtraction",
                values=(7, 3),
                answer=4
            ),
            Question(
                question="Qual o resultado de multiplicação(10, 2)?",
                function="multiplication",
                values=(10, 2),
                answer=20
            ),
            Question(
                question="Qual o resultado de fatorial(2)?",
                function="factorial",
                values=(2,),
                answer=2
            ),
            Question(
                question="Qual o resultado de divisão chão(5, 2)?",
                function="floorDivision",
                values=(5, 2),
                answer=2
            ),
            Question(
                question="Qual a função primitiva usada para definir a função subtração?\n a) zero\n b) antecessora\n c) projeção\n d) recursão",
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
                question="Qual o resultado de divisão teto(7, 3)?",
                function="roofDivision",
                values=(7, 3),
                answer=3
            ),
            Question(
                question="Qual o resultado de resto divisao(10, 3)?",
                function="modulus",
                values=(10, 3),
                answer=1
            ),
            Question(
                question="Qual a função primitiva usada para definir a função multiplicacao?\n a) Soma\n b) Subtracao\n c) Fatorial\n d) Máximo",
                function="none",
                values=(),
                answer="a"
            ),
            Question(
                question="Qual o resultado de elevado(3, 3)?",
                function="pow",
                values=(3, 3),
                answer=27
            ),
            Question(
                question="Qual o resultado de fatorial(6)?",
                function="factorial",
                values=(6,),
                answer=720
            ),
            Question(
                question="Qual o resultado de divisão teto(16, 3)?",
                function="roofDivision",
                values=(16, 3),
                answer=6
            ),
            Question(
                question="Qual o resultado de resto divisao(16, 5)?",
                function="modulus",
                values=(16, 5),
                answer=1
            ),
            Question(
                question="Qual a função primitiva usada para definir a função potencia?\n a) multiplicação\n b) subtracao\n c) fatorial\n d) maximo",
                function="none",
                values=(),
                answer="a"
            ),
            Question(
                question="Qual a função primitiva usada para definir a função fatorial?\n a) maximo\n b) subtracao\n c) fatorial\n d) multiplicação",
                function="none",
                values=(),
                answer="c"
            ),
            Question(
                question="Qual o resultado de percentual(15, 60)?",
                function="modulus",
                values=(15, 60),
                answer=9
            ),
            Question(
                question="Qual o resultado de percentual(25, 36)?",
                function="modulus",
                values=(25, 36),
                answer=9
            ),
            Question(
                question="Esta pilha de recursão corresponde a qual função? [Pilha: subtracao(7, subtracao(3, 1))]\n a) subtracao\n b) soma\n c) multiplicacao\n d) fatorial",
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
                question="Qual o resultado de divisão chão(35, 6)?",
                function="floorDivision",
                values=(35, 6),
                answer=5
            ),
            Question(
                question="Qual o resultado de divisão chão(40, 9)?",
                function="floorDivision",
                values=(40, 9),
                answer=4
            ),
            Question(
                question="Qual o resultado de divisão teto(55, 6)?",
                function="roofDivision",
                values=(55, 6),
                answer=10
            ),
            Question(
                question="Qual o resultado de divisão teto(48, 9)?",
                function="roofDivision",
                values=(48, 9),
                answer=6
            ),
            Question(
                question="Qual o resultado de divisão chão(35, 6)?",
                function="floorDivision",
                values=(35, 6),
                answer=5
            ),
            Question(
                question="Qual o resultado de divisão chão(42, 9)?",
                function="floorDivision",
                values=(42, 9),
                answer=4
            ),
            Question(
                question="Qual o resultado de divisão teto(53, 6)?",
                function="roofDivision",
                values=(53, 6),
                answer=9
            ),
            Question(
                question="Qual o resultado de divisão teto(36, 7)?",
                function="roofDivision",
                values=(36, 7),
                answer=6
            ),
            Question(
                question="Qual a função primitiva usada para definir a função divisão chão?\n a) subtracao\n b) soma\n c) máximo\n d) mínimo",
                function="none",
                values=(),
                answer="a"
            ),
            Question(
                question="Qual o resultado de divisão teto(25, 6)?",
                function="roofDivision",
                values=(25, 6),
                answer=5
            ),
            Question(
                question="Esta pilha de recursão corresponde a qual função? [Pilha: fatorial(3, multiplicacao(2, fatorial(1)))]\n a) multiplicacao\n b) subtracao\n c) soma\n d) fatorial",
                function="none",
                values=(),
                answer="d"
            ),
            Question(
                question="Qual o resultado de divisão chão(44, 7)?",
                function="floorDivision",
                values=(44, 7),
                answer=6
            ),
            Question(
                question="Qual o resultado de divisão chão(81, 8)?",
                function="floorDivision",
                values=(81, 8),
                answer=10
            ),
            Question(
                question="Qual o resultado de divisão teto(39, 4)?",
                function="roofDivision",
                values=(39, 4),
                answer=10
            ),
            Question(
                question="Qual o resultado de divisão teto(72, 5)?",
                function="roofDivision",
                values=(72, 5),
                answer=15
            ),
            Question(
                question="Qual o resultado de divisão chão(56, 8)?",
                function="floorDivision",
                values=(56, 8),
                answer=7
            ),
            Question(
                question="Qual o resultado de divisão chão(63, 11)?",
                function="floorDivision",
                values=(63, 11),
                answer=5
            ),
            Question(
                question="Qual o resultado de divisão teto(98, 10)?",
                function="roofDivision",
                values=(98, 10),
                answer=10
            ),
            Question(
                question="Qual o resultado de divisão teto(57, 6)?",
                function="roofDivision",
                values=(57, 6),
                answer=10
            ),
            Question(
                question="Qual a função primitiva usada para definir a função fatorial?\n a) soma\n b) multiplicacao\n c) fatorial\n d) subtracao",
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
            ), Question(
                question="Qual o resultado de elevado(4, 3)?",
                function="pow",
                values=(4, 3),
                answer=64
            ), Question(
                question="Qual o resultado de elevado(4, 4)?",
                function="pow",
                values=(4, 4),
                answer=256
            ), Question(
                question="Qual o resultado de divisão chão(220, 12)?",
                function="floorDivision",
                values=(220, 12),
                answer=18
            ), Question(
                question="Qual o resultado de divisão teto(250, 16)?",
                function="roofDivision",
                values=(250, 16),
                answer=16
             ),Question(
                question="Qual o resultado de divisão teto(315, 11)?",
                function="roofDivision",
                values=(315, 11),
                answer=29
            ), Question(
                question="Qual o resultado de divisão chão(190, 12)?",
                function="floorDivision",
                values=(190, 12),
                answer=15
            ), Question(
                question="Qual o resultado de divisão teto(230, 16)?",
                function="roofDivision",
                values=(230, 16),
                answer=15
             ),Question(
                question="Qual o resultado de divisão teto(315, 11)?",
                function="roofDivision",
                values=(145, 14),
                answer=11
            ), Question(
                question="Qual o resultado de divisão chão(225, 19)?",
                function="floorDivision",
                values=(225, 19),
                answer=11
            ), Question(
                question="Qual o resultado de divisão teto(270, 14)?",
                function="roofDivision",
                values=(250, 16),
                answer=20
             ),Question(
                question="Qual o resultado de divisão teto(280, 17)?",
                function="roofDivision",
                values=(280, 17),
                answer=17
            ),Question(
                question="Qual o resultado de percentual(30, 120)?",
                function="modulus",
                values=(30, 120),
                answer=36
            ),
            Question(
                question="Qual o resultado de percentual(60, 150)?",
                function="modulus",
                values=(60, 150),
                answer=90
            ),Question(
                question="Qual o resultado de percentual(40, 210)?",
                function="modulus",
                values=(40, 210),
                answer=84
            ),
            Question(
                question="Qual o resultado de percentual(60, 160)?",
                function="modulus",
                values=(60, 160),
                answer=96
            ),Question(
                question="Qual o resultado de divisão chão(310, 14)?",
                function="floorDivision",
                values=(310, 14),
                answer=22
            ), Question(
                question="Qual o resultado de divisão teto(215, 14)?",
                function="roofDivision",
                values=(215, 14),
                answer=16
             ),Question(
                question="Qual o resultado de divisão teto(290, 15)?",
                function="roofDivision",
                values=(290, 15),
                answer=20
            ), Question(
                question="Qual o resultado de divisão chão(305, 11)?",
                function="floorDivision",
                values=(305, 11),
                answer=27
            ), Question(
                question="Qual o resultado de divisão teto(250, 16)?",
                function="roofDivision",
                values=(250, 16),
                answer=16
             ),Question(
                question="Qual o resultado de divisão teto(320, 15)?",
                function="roofDivision",
                values=(320, 15),
                answer=22
            ),Question(
                question="Qual o resultado de percentual(15, 60)?",
                function="modulus",
                values=(15, 60),
                answer=9
            ),
            Question(
                question="Qual o resultado de percentual(30, 120)?",
                function="modulus",
                values=(30, 120),
                answer=36
            ),
            Question(
                question="Qual o resultado de percentual(40, 160)?",
                function="modulus",
                values=(40, 160),
                answer=64
            ),

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

