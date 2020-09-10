from tockenjs import Token
from tockenjs import Tipo

# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerJS:

    list_tockens = []
    list_failure = list()
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
    path = ""
    #"Verificador de Linea de Codigo": Este es un acumulador el cual sirve
    #como pivote para determinar en que linea del codigo existe un error
    #de analisis lexico.
    vlc = 1
    errores = []   

    def lexer(self, entrada):
        posicion = 0
        while posicion < len(entrada):
            self.codigo = entrada
            self.caracter = entrada[posicion]
            
            # S0 -> S1 (Simbolos del Lenguaje)
            if self.caracter == "(":
                self.agregarToken(Tipo.PARENT_IZQ , self.caracter)
            elif self.caracter == ")":
                self.agregarToken(Tipo.PARENT_DER , self.caracter)
            elif self.caracter == "{":
                self.agregarToken(Tipo.LLAVEIZQ , self.caracter)
            elif self.caracter == "}":
                self.agregarToken(Tipo.LLAVEDER , self.caracter)
            elif self.caracter == ";":
                self.agregarToken(Tipo.PUNTOCOMA , self.caracter)
            elif self.caracter == ":":
                self.agregarToken(Tipo.DOSPUNTOS , self.caracter)
            elif self.caracter == ".":
                self.agregarToken(Tipo.PUNTO , self.caracter)
            elif self.caracter == ",":
                self.agregarToken(Tipo.COMA , self.caracter)    
            elif self.caracter == "=":
                self.agregarToken(Tipo.SIGNO_IGUAL, self.caracter)
            elif self.caracter == "<":
                self.agregarToken(Tipo.SIGNO_IGUAL, self.caracter)
            elif self.caracter == ">":
                self.agregarToken(Tipo.SIGNO_IGUAL, self.caracter)
            elif self.caracter == "+":
                self.agregarToken(Tipo.SUMA, self.caracter)
            elif self.caracter == "-":
                self.agregarToken(Tipo.RESTA, self.caracter)
            elif self.caracter == "!":
                self.agregarToken(Tipo.SIGNO_DISTINTO, self.caracter)    
            elif self.caracter == "*":
                self.agregarToken(Tipo.MULTIPLICACION, self.caracter)
            elif self.caracter == "&":
                self.agregarToken(Tipo.MULTIPLICACION, self.caracter) 
            elif self.caracter == "|":
                self.agregarToken(Tipo.MULTIPLICACION, self.caracter)     
            elif self.caracter == '"':
                self.agregarToken(Tipo.NINGUNO, self.caracter)
            elif self.caracter == "'":
                self.agregarToken(Tipo.NINGUNO, self.caracter)
            elif self.caracter == "/":
                self.lexema += self.caracter
                val = self.S6(posicion+1)
                posicion = val

            # S0 - S2 (Reservadas | Identificadores)
            #Hay que recordar que en este lexema lleva guion bajo
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S2(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
                
            # S0 -> S4 (Numericos)
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexemaNumero(posicion)
                self.S4(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            elif self.caracter == " " or self.caracter == "\t" or self.caracter=="\n":
                posicion +=1
                continue
            else:
                self.agregarErrores(posicion, self.caracter)
            posicion += 1
        print("Estos son los tokens validos: ", self.list_tockens)
        print("Estos son los errores: ", self.list_failure)
        return ""
    
    def S2(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal

        for x in range (inicial, final):
            self.lexema += self.codigo[x]
        
        aux_lexema = self.lexema.lower()

        if aux_lexema == "var":
            self.agregarToken(Tipo.VAR, aux_lexema)
            return
        elif aux_lexema == "if":
            self.agregarToken(Tipo.IF, aux_lexema)
            return
        elif aux_lexema == "else":
            self.agregarToken(Tipo.ELSE, aux_lexema)
            return
        elif aux_lexema == "for":
            self.agregarToken(Tipo.FOR, aux_lexema)
            return
        elif aux_lexema == "while":
            self.agregarToken(Tipo.WHILE, aux_lexema)
            return
        elif aux_lexema == "do":
            self.agregarToken(Tipo.DO, aux_lexema)
            return
        elif aux_lexema == "continue":
            self.agregarToken(Tipo.CONTINUE, aux_lexema)
            return
        elif aux_lexema == "break":
            self.agregarToken(Tipo.BREAK, aux_lexema)
            return
        elif aux_lexema == "return":
            self.agregarToken(Tipo.RETURN, aux_lexema)
            return
        elif aux_lexema == "function":
            self.agregarToken(Tipo.FUNCTION, aux_lexema)
            return
        elif aux_lexema == "constructor":
            self.agregarToken(Tipo.CONSTRUCTOR, aux_lexema)
            return
        elif aux_lexema == "class":
            self.agregarToken(Tipo.CLASS, aux_lexema)
            return    


        self.lexema = ""
        while  (inicial < final):
            auxcaracter = self.codigo[inicial]
            
            # S0 -> S3
            if auxcaracter.isalpha():                
                self.S3(inicial, final)
                break
            else:
                self.agregarErrores(inicial, auxcaracter)
            inicial += 1

    def S3(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S3 -> S3
            if auxcaracter.isalpha():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)                    
            
            elif auxcaracter == "_":
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema) 

            # S3 -> S3
            elif auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)  
            else:
                self.agregarErrores(posInicial, auxcaracter)
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
            elif auxcaracter == ".":
                if  (posInicial == posFinal):
                    self.lexema += auxcaracter
                    self.S5(posInicial, posFinal)
                break
            else:
                self.agregarErrores(posInicial, auxcaracter)
            posInicial += 1

    def S5(self, posInicial, posFinal):
        caracter = ""
        while  (posInicial < posFinal):
            caracter = self.codigo[posInicial]

            # S5 -> S5
            if caracter.isnumeric():
                self.lexema += caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            else:
                self.agregarErrores(posInicial, self.caracter)
            posInicial += 1

    def S6(self, posInicial):
        auxcaracter = ""
        while (posInicial < len(self.codigo)):
            auxcaracter = self.codigo[posInicial]
            if  auxcaracter == "*":
                # S6 -> S7
                posInicial = self.S7(posInicial)

            elif auxcaracter == "/":
                tamaniolexema = self.getTamanioComentario(posInicial)
                posInicial = posInicial + tamaniolexema

            elif auxcaracter == " " or auxcaracter == "\t" or auxcaracter =="\n":
                break
            else:
                # S0
                self.agregarToken(Tipo.VALOR, self.lexema)
                posInicial += 1
                break
            posInicial += 1
        return posInicial

    def S7(self, posInicial):
        auxcaracter = ""
        while (posInicial < len(self.codigo)):
            # S0
            if  self.codigo[posInicial] == "*" and self.codigo[posInicial+1] == "/":
                self.lexema = ""
                posInicial += 1
                break
            else:
                # S7 -> S7
                auxcaracter += self.codigo[posInicial]
            posInicial += 1
        return posInicial

    def agregarErrores(self, tipo, valor):
        #self.list_tockens.append(nuevo)
        self.list_failure.append([tipo, valor])
        self.lexema = ""

    def agregarToken(self, tipo, valor):
        nuevo = Token(tipo, valor)
        #self.list_tockens.append(nuevo)
        self.list_tockens.append([tipo, valor])
        self.lexema = ""
    
    def getTamanioLexemaTexto(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "." or self.codigo[i] == "," or self.codigo[i] == "=" or self.codigo[i] == "+" or self.codigo[i] == "-" or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo == "|":
                break
            longitud += 1
        return longitud

    def getTamanioLexemaNumero(self, posInicial):
        longitud = 0    
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "." or self.codigo[i] == "," or self.codigo[i] == "=" or self.codigo[i] == "+" or self.codigo[i] == "-" or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n":
                break
            longitud += 1
        return longitud

    def getTamanioComentario(self, posInicial):
        longitud = 0    
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == "\n":
                break
            longitud += 1
        return longitud    