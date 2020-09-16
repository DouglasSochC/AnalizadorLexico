from enum import Enum

class Tipo(Enum):
    # Simbolos del lenguaje
    NINGUNO = 1
    VALOR = 2
    PARENT_IZQ = 3
    PARENT_DER = 4
    MULTIPLICACION = 5
    DIVISION = 6
    SUMA = 7
    RESTA = 8

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken = tipo
        self.valorToken = valor
