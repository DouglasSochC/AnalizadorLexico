from tockenalgebra import Token
from tockenalgebra import Tipo
# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerAlgebra:

    list_tockens = []
    list_path = []
    list_failure = []
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
    errores = []
    lineaspath = 2
    lineadeanalisis = 1
    posicionenlinea = 0 

    def lexer(self, entrada):
        print(entrada.split("\n"))
        posicion = 0
        while posicion < len(entrada):
            self.codigo = entrada
            self.caracter = entrada[posicion]
            
            # S0 -> S1 (Simbolos del Lenguaje)
            if self.caracter == "(":
                self.agregarToken(Tipo.PARENT_IZQ , self.caracter)
            elif self.caracter == ")":
                self.agregarToken(Tipo.PARENT_DER , self.caracter)
            elif self.caracter == "*":
                self.agregarToken(Tipo.MULTIPLICACION , self.caracter)
            elif self.caracter == "/":
                self.agregarToken(Tipo.DIVISION , self.caracter)
            elif self.caracter == "-":
                self.agregarToken(Tipo.RESTA, self.caracter)
            elif self.caracter == "+":
                self.agregarToken(Tipo.SUMA, self.caracter)
            
            # S0 - S2 (Reservadas | Identificadores)
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexema(posicion)
                self.S3(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            # S0 -> S4 (Numericos)
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexema(posicion)
                self.S4(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            #Este solo realiza la siguiente iteracion, quiero decir que no se toma 
            # en cuenta estos caracteres
            elif self.caracter == " " or self.caracter == "\t" or self.caracter == "\n":
                posicion +=1
                continue
            posicion += 1
        self.analizarExpresion()
        self.list_tockens.clear()
        return ""

    def S3(self, posInicial, posFinal):
        aux_caracter = ""
        while  (posInicial < posFinal):
            aux_caracter = self.codigo[posInicial]

            # S3 -> S3
            if aux_caracter.isalpha():
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            
            # S3 -> S3
            elif aux_caracter.isnumeric():
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)  
            # ESTO ES UNA DUDA POR SI NO SE DA CORRECTAMENTE EL /**/
            # SE DEBE DE HACER UN BREAK
            else:
                self.agregarErrores(posInicial, aux_caracter)
            posInicial += 1

    def S4(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S4 -> S4
            if auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)

            # S4 -> S5
            elif auxcaracter == ".":
                self.lexema += auxcaracter
                self.S5(posInicial+1, posFinal)
                break
            posInicial += 1

    def S5(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S5 -> S5
            if auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            else:
                self.agregarErrores(posInicial, self.lexema)
            posInicial += 1   

    def S7(self, posInicial):
        auxcaracter = ""
        posFinal = len(self.codigo)
        auxpath = ""
        posError = posInicial - 2
        while (posInicial < posFinal):
            
            auxcaracter = self.codigo[posInicial]            
            
            if (posInicial+1) != posFinal-1:
                                
                # S7 -> S10
                if  auxcaracter == "*" and self.codigo[posInicial + 1] == "/":
                    posInicial = posInicial+1
                    if auxpath != "":
                        self.list_path.append(auxpath)
                        self.lineaspath -= 1
                    break
                
                # S7 -> S7
                else:
                    if self.lineaspath > 0:
                        auxpath += auxcaracter
                posInicial += 1                                
            else:
                self.agregarErrores(posError, self.codigo[posError])
                posInicial = posError
                break
        return posInicial

    def analizarExpresion(self):
        acumulador = 0
        for i in self.list_tockens:
            if i[1] == "(":
                acumulador += 1
            if i[1] == ")":
                acumulador -= 1
        if acumulador == 0:
            print("Es correcta la expresion")
        else:
            print("Es incorrecta la expresion")

    def agregarErrores(self, posicion, valor):
        self.list_failure.append([posicion, valor, self.lineadeanalisis])
        self.lexema = ""

    def agregarToken(self, tipo, valor):
        nuevo = Token(tipo, valor)
        #self.list_tockens.append(nuevo)
        self.list_tockens.append([tipo, valor])
        self.lexema = ""
    
    def getTamanioLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            #El / debe de estar validado aqui ya que si encuentra hola(){}/*esto es una prueba en una misma linea*/
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "*" or self.codigo[i] == "/" or self.codigo[i] == "-" or self.codigo[i] == "+" or self.codigo[i] == "\n":
                break
            longitud += 1
        return longitud