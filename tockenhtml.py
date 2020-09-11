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

    # Palabras Reservadas
    HTML = 7
    HEAD = 8
    TITLE = 9
    BODY = 10
    SUB_TITLE = 11
    PARRAFO = 12
    IMAGEN = 13
    HIPERVINCULO = 14
    LISTAS = 15
    ESTILO = 16
    TABLE = 17
    TH = 18
    TR = 19
    TD = 20
    CAPTION = 21
    COLGROUP = 22
    COL = 23
    THEAD = 24
    TBODY = 25
    TFOOT = 26
    STYLE = 27

    DOBLECOMILLA = 28
    COMILLA = 29

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken = tipo
        self.valorToken = valor
