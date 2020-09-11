from tockencss import Token
from tockencss import Tipo

# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerCSS:

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
            elif self.caracter == "-":
                self.agregarToken(Tipo.GUION, self.caracter)
            elif self.caracter == "*":
                self.agregarToken(Tipo.ASTERISCO, self.caracter)
            elif self.caracter == '"':
                self.agregarToken(Tipo.NINGUNO, self.caracter)
            elif self.caracter == "'":
                self.agregarToken(Tipo.NINGUNO, self.caracter)
            
            # S0 -> S6
            elif self.caracter == "/":
                self.lexema += self.caracter
                val = self.S6(posicion+1)
                posicion = val

            # S0 - S2 (Reservadas | Identificadores)
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S2(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            # S0 -> S9
            elif self.caracter == "#" or self.caracter == ".":
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.lexema += self.caracter
                # S9 -> S3
                self.S3(posicion+1, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            # S0 -> S4 (Numericos)
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexemaNumero(posicion)
                self.S4(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1

            #Este solo realiza la siguiente iteracion, quiero decir que no se toma 
            # en cuenta estos caracteres
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
        aux_lexema = ""

        for x in range (inicial, final):
            aux_lexema += self.codigo[x]
        
        aux_lexema = aux_lexema.lower()

        if aux_lexema == "color":
            self.agregarToken(Tipo.COLOR, aux_lexema)
            return
        elif aux_lexema == "text-align":
            self.agregarToken(Tipo.TEXT_ALIGN, aux_lexema)
            return
        elif aux_lexema == "opacity":
            self.agregarToken(Tipo.OPACITY, aux_lexema)
            return
        elif aux_lexema == "display":
            self.agregarToken(Tipo.DISPLAY, aux_lexema)
            return
        elif aux_lexema == "line-height":
            self.agregarToken(Tipo.LINE_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "width":
            self.agregarToken(Tipo.WIDTH, aux_lexema)
            return
        elif aux_lexema == "height":
            self.agregarToken(Tipo.HEIGHT, aux_lexema)
            return
        elif aux_lexema == "position":
            self.agregarToken(Tipo.POSITION, aux_lexema)
            return
        elif aux_lexema == "bottom":
            self.agregarToken(Tipo.BOTTOM, aux_lexema)
            return
        elif aux_lexema == "top":
            self.agregarToken(Tipo.TOP, aux_lexema)
            return
        elif aux_lexema == "right":
            self.agregarToken(Tipo.RIGHT, aux_lexema)
            return
        elif aux_lexema == "left":
            self.agregarToken(Tipo.LEFT, aux_lexema)
            return    
        elif aux_lexema == "float":
            self.agregarToken(Tipo.FLOAT, aux_lexema)
            return
        elif aux_lexema == "clear":
            self.agregarToken(Tipo.CLEAR, aux_lexema)
            return
        elif aux_lexema == "max-width":
            self.agregarToken(Tipo.MAX_WIDTH, aux_lexema)
            return
        elif aux_lexema == "min-width":
            self.agregarToken(Tipo.MIN_WIDTH, aux_lexema)
            return
        elif aux_lexema == "max-height":
            self.agregarToken(Tipo.MAX_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "min-height":
            self.agregarToken(Tipo.MIN_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "border":
            self.agregarToken(Tipo.BORDER, aux_lexema)
            return
        elif aux_lexema == "border-style":
            self.agregarToken(Tipo.BO_STYLE, aux_lexema)
            return
        elif aux_lexema == "background":
            self.agregarToken(Tipo.BACKGROUND, aux_lexema)
            return
        elif aux_lexema == "background-image":
            self.agregarToken(Tipo.BACK_IMAGE, aux_lexema)
            return
        elif aux_lexema == "background-color":
            self.agregarToken(Tipo.BACK_COLOR, aux_lexema)
            return
        elif aux_lexema == "font":
            self.agregarToken(Tipo.FONT, aux_lexema)
            return
        elif aux_lexema == "font-family":
            self.agregarToken(Tipo.F_FAMILY, aux_lexema)
            return
        elif aux_lexema == "font-style":
            self.agregarToken(Tipo.F_STYLE, aux_lexema)
            return
        elif aux_lexema == "font-weight":
            self.agregarToken(Tipo.F_WEIGHT, aux_lexema)
            return
        elif aux_lexema == "font-size":
            self.agregarToken(Tipo.F_SIZE, aux_lexema)
            return
        elif aux_lexema == "padding":
            self.agregarToken(Tipo.PADDING, aux_lexema)
            return
        elif aux_lexema == "padding-left":
            self.agregarToken(Tipo.P_LEFT, aux_lexema)
            return
        elif aux_lexema == "padding-right":
            self.agregarToken(Tipo.P_RIGHT, aux_lexema)
            return
        elif aux_lexema == "padding-bottom":
            self.agregarToken(Tipo.P_BOTTOM, aux_lexema)
            return
        elif aux_lexema == "padding-top":
            self.agregarToken(Tipo.P_TOP, aux_lexema)
            return
        elif aux_lexema == "margin":
            self.agregarToken(Tipo.MARGIN, aux_lexema)
            return
        elif aux_lexema == "margin-top":
            self.agregarToken(Tipo.MA_TOP, aux_lexema)
            return
        elif aux_lexema == "margin-right":
            self.agregarToken(Tipo.MA_RIGHT, aux_lexema)
            return
        elif aux_lexema == "margin-bottom":
            self.agregarToken(Tipo.MA_BOTTOM, aux_lexema)
            return
        elif aux_lexema == "margin-left":
            self.agregarToken(Tipo.MA_LEFT, aux_lexema)
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
        aux_caracter = ""
        while  (posInicial < posFinal):
            aux_caracter = self.codigo[posInicial]

            # S3 -> S3
            if aux_caracter.isalpha():
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)
            
            # S3 -> S3    
            elif aux_caracter == "-" or aux_caracter == "#":
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)
            
            # S3 -> S3
            elif aux_caracter.isnumeric():
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)  
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

            # S4 -> S8
            elif auxcaracter.isalpha():
                self.S8(posInicial, posFinal)
                break
            elif auxcaracter == "%":
                self.lexema += auxcaracter
                self.agregarToken(Tipo.PORCENTAJE, self.lexema)
            else:
                self.agregarErrores(posInicial, auxcaracter)
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

            # S5 -> S8
            elif auxcaracter.isalpha():
                self.S8(posInicial, posFinal)
                break
            else:
                self.agregarErrores(posInicial, self.lexema)
            posInicial += 1

    def S6(self, posInicial):
        auxcaracter = ""
        posError = posInicial-1
        while (posInicial < len(self.codigo)):
            auxcaracter = self.codigo[posInicial]
            
            # S6 -> S7
            if  auxcaracter == "*":
                self.lexema += auxcaracter   
                val = self.S7(posInicial+1, posInicial)
                posInicial = val
                break
            # S6 -> S12
            elif auxcaracter == "/":
                tamaniolexema = self.getTamanioComentario(posInicial)
                posInicial = posInicial + tamaniolexema
                self.lexema = ""
                break
            elif posInicial == (len(self.codigo)-1):
                posInicial = posError
                break

            #Esto se hizo de esta forma ya que si despues de un / se encuentra algun simbolo
            #que no sea / ó * entonces ese simbolo debe de ser analizado a partir del S0 y
            #se toma la / como un error lexico
            else:
                # S0
                self.agregarErrores(posInicial, auxcaracter)                
            posInicial += 1
        return posInicial

    def S7(self, posInicial, posError):
        auxcaracter = ""
        posFinal = len(self.codigo)

        while (posInicial < len(self.codigo)):
            # Analizar las posicion en S10
            auxcaracter = self.codigo[posInicial]            

            #Este se encarga de reconocer si el /* es un error lexico ya que si
            #se llega al final del analisis, y no encontro el */ entonces si, el
            #/* es un error lexico
            if (posInicial == (posFinal-1)):
                self.agregarErrores(posError, self.lexema)
                posInicial = posError
                break
            
            # S7 -> S10
            elif  auxcaracter == "*":
                #self.lexema += auxcaracter
                val = self.S10(posInicial+1, posError)
                posInicial = val
                break

            # S7 -> S7
            else:
                #AQUI DEBE DE IR UN AFD QUE ANALICE LA DIRECCION
                #EN LA QUE VA A MOSTRAR EL ARCHIVO LIMPIO
                pass
            posInicial += 1
        return posInicial

    def S10(self, posInicial, posError):
        
        auxcaracter = ""
        posFinal = len(self.codigo)

        while (posInicial < posFinal):
            auxcaracter += self.codigo[posInicial]
            
            # S10 -> S10
            if  self.codigo[posInicial] == "*":
                pass
            
            # S10 -> S11
            elif self.codigo[posInicial] == "/":
                self.lexema == ""
                break

            elif posInicial == (posFinal-1):
                self.agregarErrores(posError, self.lexema)
                posInicial = posError
                break

            # S10 -> S7
            else:
                val = self.S7(posInicial, posError)
                posInicial = val
                break
            posInicial += 1
        return posInicial

    def S8(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal
        aux_lexema = ""

        for x in range (inicial, final):
            aux_lexema += self.codigo[x]
        
        aux_lexema = aux_lexema.lower()

        if aux_lexema == "px" or aux_lexema == "em" or aux_lexema == "vh" or aux_lexema == "vw" or aux_lexema == "in" or aux_lexema == "cm" or aux_lexema == "mm" or aux_lexema == "pt" or aux_lexema == "pc":
            self.lexema += aux_lexema
            self.agregarToken(Tipo.UNIDAD_MEDIDA, self.lexema)
            return
        else:
            self.agregarErrores(posInicial, aux_lexema)

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
            #El / debe de estar validado aqui ya que si encuentra hola(){}/*esto es una prueba en una misma linea*/
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "," or self.codigo[i] == "+" or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo[i] == "/":
                break
            longitud += 1
        return longitud

    def getTamanioLexemaNumero(self, posInicial):
        longitud = 0    
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo[i] == ",":
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