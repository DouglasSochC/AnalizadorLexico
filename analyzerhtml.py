from tockenhtml import Token
from tockenhtml import Tipo

# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerHTML:

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
            if self.caracter == "<":
                self.agregarToken(Tipo.MENOR , self.caracter)
            elif self.caracter == ">":
                self.agregarToken(Tipo.MAYOR , self.caracter)
            elif self.caracter == '"':
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
            elif self.caracter == "'":
                self.agregarToken(Tipo.COMILLA, self.caracter)
            elif self.caracter == '=':
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
            elif self.caracter == '/':
                self.agregarToken(Tipo.DIAGONAL, self.caracter)
            elif self.caracter.isalpha() or self.caracter.isnumeric():
                self.lexema += self.caracter
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S1(posicion+1, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            elif self.caracter == " " or self.caracter == "\t" or self.caracter=="\n":
                posicion +=1
                continue
            else:
                self.lexema += self.caracter
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S1(posicion+1, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            posicion += 1
        print("Estos son los tokens validos: ", self.list_tockens)
        print("Estos son los errores: ", self.list_failure)
        return ""
    
    def S1(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal

        for x in range (inicial, final):
            self.lexema += self.codigo[x]
        
        aux_lexema = self.lexema.lower()

        if aux_lexema == "html":
            self.agregarToken(Tipo.HTML, aux_lexema)
            return
        elif aux_lexema == "head":
            self.agregarToken(Tipo.HEAD, aux_lexema)
            return
        elif aux_lexema == "title":
            self.agregarToken(Tipo.TITLE, aux_lexema)
            return
        elif aux_lexema == "body":
            self.agregarToken(Tipo.BODY, aux_lexema)
            return
        elif aux_lexema == "h1":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "h2":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "h3":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "h4":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "h5":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "h6":
            self.agregarToken(Tipo.SUB_TITLE, aux_lexema)
            return
        elif aux_lexema == "p":
            self.agregarToken(Tipo.PARRAFO, aux_lexema)
            return
        elif aux_lexema == "img":
            self.agregarToken(Tipo.IMAGEN, aux_lexema)
            return    
        elif aux_lexema == "a":
            self.agregarToken(Tipo.HIPERVINCULO, aux_lexema)
            return
        elif aux_lexema == "ul":
            self.agregarToken(Tipo.LISTAS, aux_lexema)
            return
        elif aux_lexema == "ol":
            self.agregarToken(Tipo.LISTAS, aux_lexema)
            return
        elif aux_lexema == "li":
            self.agregarToken(Tipo.LISTAS, aux_lexema)
            return 
        elif aux_lexema == "style":
            self.agregarToken(Tipo.STYLE, aux_lexema)
            return 
        elif aux_lexema == "table":
            self.agregarToken(Tipo.TABLE, aux_lexema)
            return
        elif aux_lexema == "th":
            self.agregarToken(Tipo.TH, aux_lexema)
            return 
        elif aux_lexema == "tr":
            self.agregarToken(Tipo.TR, aux_lexema)
            return 
        elif aux_lexema == "td":
            self.agregarToken(Tipo.TD, aux_lexema)
            return
        elif aux_lexema == "caption":
            self.agregarToken(Tipo.CAPTION, aux_lexema)
            return
        elif aux_lexema == "colgroup":
            self.agregarToken(Tipo.COLGROUP, aux_lexema)
            return
        elif aux_lexema == "col":
            self.agregarToken(Tipo.COL, aux_lexema)
            return
        elif aux_lexema == "thead":
            self.agregarToken(Tipo.THEAD, aux_lexema)
            return
        elif aux_lexema == "tbody":
            self.agregarToken(Tipo.TBODY, aux_lexema)
            return
        elif aux_lexema == "tfoot":
            self.agregarToken(Tipo.TFOOT, aux_lexema)
            return
        else:
            self.agregarToken(Tipo.VALOR, aux_lexema)
            return

    def S2(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S3 -> S3
            if auxcaracter.isalpha():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            # S3 -> S3
            elif auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)  
            else:
                self.agregarErrores(posInicial, auxcaracter)
            posInicial += 1

    def S3(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S3 -> S3
            if auxcaracter.isalpha():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            # S3 -> S3
            elif auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            elif self.caracter == " " or self.caracter == "\t" or self.caracter=="\n":
                posInicial +=1
                continue  
            else:
                self.agregarErrores(posInicial, auxcaracter)
            posInicial += 1

    def agregarErrores(self, tipo, valor):
        #self.list_tockens.append(nuevo)
        self.list_failure.append([tipo, valor])
        self.lexema = ""

    def agregarToken(self, tipo, valor):
        #nuevo = Token(tipo, valor)
        #self.list_tockens.append(nuevo)
        self.list_tockens.append([tipo, valor])
        self.lexema = ""
    
    def getTamanioLexemaTexto(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == ">" or self.codigo[i] == "/" or self.codigo[i] == "<" or self.codigo[i] == "=" or self.codigo[i] == "\n" or self.codigo[i] == "'" or self.codigo[i] == '"' or self.codigo[i] == ":" or self.codigo[i] == ";":
                break
            longitud += 1
        return longitud
  