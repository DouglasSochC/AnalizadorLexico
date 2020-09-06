from enum import Enum

class Tipo(Enum):
    # Simbolos del lenguaje
    LLAVEIZQ = 1
    LLAVEDER = 2
    PARENT_IZQ = 3
    PARENT_DER = 4
    DOSPUNTOS = 5
    PUNTOCOMA = 6
    COMA = 7
    PUNTO = 8

    # Expresiones Logicas Relacionales
    SIGNO_IGUAL = 9
    SIGNO_DISTINTO= 10
    SIGNO_MAYORQ = 11
    SIGNO_MENORQ = 12
    SIGNO_MAYORIGUAL = 13
    SIGNO_MENORIGUAL = 14

    # Expresiones Logicas del Lenguaje
    CONJUNCION = 15 #&&
    DISYUNCION = 16 #||
    NEGACION = 17 #!EXP

    # Palabras Reservadas
    VAR = 18
    IF = 19
    ELSE = 20
    ELSE_IF = 21
    FOR = 22
    WHILE = 23
    DO = 24
    CONTINUE = 25
    BREAK = 26
    RETURN = 27
    FUNCTION = 28
    CONSTRUCTOR = 29
    CLASS = 30
    MATH_POW = 31

    # Expresion Aritmetica
    SUMA = 32
    RESTA = 33
    MULTIPLICACION = 34
    DIVISION = 35
    POTENCIA = 36

    # Expresiones Regulares
    VALOR = 37 # Es el reconocimiento de un entero seguido de una cadena o solo un entero
    ID = 38
    NINGUNO = 39

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken = tipo
        self.valorToken = valor
