from tocken import Token
from tocken import Tipo

class Analyzer:

    list_tockens = list()
    list_failure = list()
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
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
            # S0 -> S1
            if self.caracter == "(":
                self.agregarToken(Tipo.PARENT_DER , self.caracter)
            elif self.caracter == ")":
                self.agregarToken(Tipo.PARENT_IZQ , self.caracter)
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
            
            # S0 - S2
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexema(posicion)
                self.S2(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema
                
            # S0 -> S3
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexema(posicion)
                self.lexema += self.caracter
                
            
        return ""
    
    def S2(self, posInicial, tamanio):
        inicial = posInicial
        final = posInicial+tamanio
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
            
            if auxcaracter.isalpha():                
                self.lexema += self.caracter
            elif auxcaracter.isalpha():
                self.lexema += self.caracter
            else:
                self.errores.append(inicial)                
            inicial += 1

    def S3(self):
        pass

    def S4(self):
        pass

    def S5(self):
        pass

    def agregarToken(self, tipo, valor):
        nuevo = Token(tipo, valor)
        self.list_tockens.append(nuevo)
        self.lexema = ""
    
    def getTamanioLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "." or self.codigo[i] == ",":
                break
            longitud += 1
        return longitud