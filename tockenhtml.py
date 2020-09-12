from enum import Enum

class Tipo(Enum):
    # Simbolos del lenguaje
    MAYOR = 1
    MENOR = 2
    DIAGONAL = 3
    IGUAL = 4
    
    # Expresiones Regulares
    VALOR = 5
    NINGUNO = 6
    ID = 7

    # Palabras Reservadas
    HTML = 8
    HEAD = 9
    TITLE = 10
    BODY = 11
    SUB_TITLE = 12
    PARRAFO = 13
    IMAGEN = 14
    HIPERVINCULO = 15
    LISTAS = 16
    ESTILO = 17
    TABLE = 18
    TH = 19
    TR = 20
    TD = 21
    CAPTION = 22
    COLGROUP = 23
    COL = 24
    THEAD = 25
    TBODY = 26
    TFOOT = 27
    STYLE = 28

    DOBLECOMILLA = 29
    COMILLA = 30

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken = tipo
        self.valorToken = valor
