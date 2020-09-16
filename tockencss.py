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
    GUION = 9
    ASTERISCO = 10
    
    # Expresiones Regulares
    VALOR = 11 # Es el reconocimiento de un entero seguido de una cadena o solo un entero
    ID = 12
    NINGUNO = 13

    # Palabras Reservadas
    COLOR = 14    
    TEXT_ALIGN = 15
    OPACITY = 16
    DISPLAY = 17
    LINE_HEIGHT = 18
    WIDTH = 19
    HEIGHT = 20
    POSITION = 21
    BOTTOM = 22
    TOP = 23
    RIGHT = 24
    LEFT = 25
    FLOAT = 26
    CLEAR = 27
    MAX_WIDTH = 28
    MIN_WIDTH = 29
    MAX_HEIGHT = 30
    MIN_HEIGHT = 31
    #BORDER -> BO
    BORDER = 32
    BO_STYLE = 33
    #BACKGROUND -> BACK
    BACKGROUND = 34
    BACK_COLOR = 35
    BACK_IMAGE = 36
    #FONT -> F
    FONT = 37
    F_FAMILY = 38
    F_STYLE = 39
    F_SIZE = 40
    F_WEIGHT = 41
    #PADDING -> P
    PADDING = 42
    P_LEFT = 43
    P_TOP = 44
    P_RIGHT = 45
    P_BOTTOM = 46
    #MARGIN -> MA
    MARGIN = 47
    MA_TOP = 48
    MA_RIGHT = 49
    MA_BOTTOM = 50
    MA_LEFT = 51

    UNIDAD_MEDIDA = 52
    PORCENTAJE = 53
    COLORES = 54
    URL = 55
    CADENAS = 56
    COMILLA = 57
    DOBLECOMILLA = 58

class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor):
        self.tipoToken = tipo
        self.valorToken = valor
