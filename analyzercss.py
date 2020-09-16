from tockencss import Token
from tockencss import Tipo
from tkinter import filedialog
import subprocess
# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerCSS:

    list_tockens = []
    list_path = []
    list_failure = []
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
    errores = []
    lineaspath = 2
    bitacoracss = []
    lineadeanalisis = 0
    consolabitacoracss = ""

    def lexer(self, entrada):
        posicion = 0
        while posicion < len(entrada):
            self.codigo = entrada
            self.caracter = entrada[posicion]
            
            # S0 -> S1 (Simbolos del Lenguaje)
            if self.caracter == "(":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.PARENT_IZQ , self.caracter)
            elif self.caracter == ")":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.PARENT_DER , self.caracter)
            elif self.caracter == "{":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.LLAVEIZQ , self.caracter)
            elif self.caracter == "}":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.LLAVEDER , self.caracter)
            elif self.caracter == ";":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.PUNTOCOMA , self.caracter)
            elif self.caracter == ":":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.DOSPUNTOS , self.caracter)
            elif self.caracter == ".":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.PUNTO , self.caracter)
            elif self.caracter == ",":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.COMA , self.caracter)
            elif self.caracter == "-":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.GUION, self.caracter)
            elif self.caracter == "*":
                self.ingresarBitacoraCSS("S0","S1",self.caracter)
                self.agregarToken(Tipo.ASTERISCO, self.caracter)
            
            
            elif self.caracter == '"':
                # S0 -> S12
                self.ingresarBitacoraCSS("S0","S12",self.caracter)
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    # S12 - S12
                    self.ingresarBitacoraCSS("S12","S12",self.codigo[x])
                    self.lexema += self.codigo[x]
                self.agregarToken(Tipo.VALOR , self.lexema)
                # S12 -> S13
                self.ingresarBitacoraCSS("S12","S13",self.caracter)
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                posicion = posicion+tamanio_lexema+1
            
            # S0 -> S14
            elif self.caracter == "'":
                self.agregarToken(Tipo.COMILLA, self.caracter)
                self.ingresarBitacoraCSS("S0","S14",self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                
                # S14 -> S14
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    self.lexema += self.codigo[x]
                    self.ingresarBitacoraCSS("S14","S14",self.codigo[x])
                self.agregarToken(Tipo.VALOR , self.lexema)
                # S14 -> S15
                self.ingresarBitacoraCSS("S14","S15",self.caracter)
                self.agregarToken(Tipo.COMILLA , self.caracter)
                posicion = posicion+tamanio_lexema+1
            
            # S0 -> S6
            elif self.caracter == "/":
                self.lexema += self.caracter
                self.ingresarBitacoraCSS("S0","S6",self.caracter)
                val = self.S6(posicion+1)
                posicion = val

            # S0 - S2 (Reservadas | Identificadores)
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S2(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            # S0 -> S4 (Numericos)
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexemaNumero(posicion)
                self.S4(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1

            # S0 -> S9
            elif self.caracter == "#" or self.caracter == ".":
                self.ingresarBitacoraCSS("S0","S9",self.caracter)
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.lexema += self.caracter
                # S9 -> S3
                self.ingresarBitacoraCSS("S9","S3","")
                self.S3(posicion+1, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1

            #Este solo realiza la siguiente iteracion, quiero decir que no se toma 
            # en cuenta estos caracteres
            elif self.caracter == " " or self.caracter == "\t":
                posicion +=1
                continue
            elif self.caracter == "\n":
                self.lineadeanalisis +=1
                posicion +=1
                continue
            else:
                self.agregarErrores(posicion, self.caracter)
            posicion += 1
        
        self.limpiarErrores()
        for p in self.list_path:
            if len(p.replace("PATHW:","")) != len(p):
                
                nameFile= p.replace("PATHW:","").replace(" ","")+"\salidacss.css"
                if nameFile!='':
                    contenido=self.codigo
                    archi1=open(nameFile, "w", encoding="utf-8")
                    archi1.write(contenido) 
                    archi1.close()
        self.abrirErroresCSS()
        self.list_failure.clear()
        self.list_tockens.clear()
        for x in self.bitacoracss:
            self.consolabitacoracss += x[0]+'->'+x[1]+':'+x[2]+"\n"
        return self.consolabitacoracss
    
    def S2(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal
        aux_lexema = ""

        for x in range (inicial, final):
            aux_lexema += self.codigo[x]
        
        aux_lexema = aux_lexema.lower()

        if aux_lexema == "color":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.COLOR, aux_lexema)
            return
        elif aux_lexema == "text-align":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.TEXT_ALIGN, aux_lexema)
            return
        elif aux_lexema == "opacity":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.OPACITY, aux_lexema)
            return
        elif aux_lexema == "display":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.DISPLAY, aux_lexema)
            return
        elif aux_lexema == "line-height":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.LINE_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "width":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.WIDTH, aux_lexema)
            return
        elif aux_lexema == "height":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.HEIGHT, aux_lexema)
            return
        elif aux_lexema == "position":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.POSITION, aux_lexema)
            return
        elif aux_lexema == "bottom":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BOTTOM, aux_lexema)
            return
        elif aux_lexema == "top":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.TOP, aux_lexema)
            return
        elif aux_lexema == "right":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.RIGHT, aux_lexema)
            return
        elif aux_lexema == "left":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.LEFT, aux_lexema)
            return    
        elif aux_lexema == "float":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.FLOAT, aux_lexema)
            return
        elif aux_lexema == "clear":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.CLEAR, aux_lexema)
            return
        elif aux_lexema == "max-width":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MAX_WIDTH, aux_lexema)
            return
        elif aux_lexema == "min-width":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MIN_WIDTH, aux_lexema)
            return
        elif aux_lexema == "max-height":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MAX_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "min-height":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MIN_HEIGHT, aux_lexema)
            return
        elif aux_lexema == "border":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BORDER, aux_lexema)
            return
        elif aux_lexema == "border-style":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BO_STYLE, aux_lexema)
            return
        elif aux_lexema == "background":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BACKGROUND, aux_lexema)
            return
        elif aux_lexema == "background-image":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BACK_IMAGE, aux_lexema)
            return
        elif aux_lexema == "background-color":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.BACK_COLOR, aux_lexema)
            return
        elif aux_lexema == "font":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.FONT, aux_lexema)
            return
        elif aux_lexema == "font-family":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.F_FAMILY, aux_lexema)
            return
        elif aux_lexema == "font-style":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.F_STYLE, aux_lexema)
            return
        elif aux_lexema == "font-weight":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.F_WEIGHT, aux_lexema)
            return
        elif aux_lexema == "font-size":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.F_SIZE, aux_lexema)
            return
        elif aux_lexema == "padding":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.PADDING, aux_lexema)
            return
        elif aux_lexema == "padding-left":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.P_LEFT, aux_lexema)
            return
        elif aux_lexema == "padding-right":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.P_RIGHT, aux_lexema)
            return
        elif aux_lexema == "padding-bottom":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.P_BOTTOM, aux_lexema)
            return
        elif aux_lexema == "padding-top":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.P_TOP, aux_lexema)
            return
        elif aux_lexema == "margin":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MARGIN, aux_lexema)
            return
        elif aux_lexema == "margin-top":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MA_TOP, aux_lexema)
            return
        elif aux_lexema == "margin-right":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MA_RIGHT, aux_lexema)
            return
        elif aux_lexema == "margin-bottom":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
            self.agregarToken(Tipo.MA_BOTTOM, aux_lexema)
            return
        elif aux_lexema == "margin-left":
            self.ingresarBitacoraCSS("S0","S2",aux_lexema)
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
        acum = 1
        while  (posInicial < posFinal):
            aux_caracter = self.codigo[posInicial]

            # S3 -> S3
            if aux_caracter.isalpha():
                if acum == 1:
                    self.ingresarBitacoraCSS("S0","S3",aux_caracter)
                    acum -= 1
                else:
                    self.ingresarBitacoraCSS("S3","S3",aux_caracter)
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)
            
            # S3 -> S3    
            elif aux_caracter == "-" or aux_caracter == "#":
                self.ingresarBitacoraCSS("S3","S3",aux_caracter)
                self.lexema += aux_caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)
            
            # S3 -> S3
            elif aux_caracter.isnumeric():
                self.ingresarBitacoraCSS("S3","S3",aux_caracter)
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
        acum = 1
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S4 -> S4
            if auxcaracter.isnumeric():
                if acum == 1:
                    self.ingresarBitacoraCSS("S0","S4",auxcaracter)
                    acum -=1
                else:
                    self.ingresarBitacoraCSS("S4","S4",auxcaracter)
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)

            # S4 -> S5
            elif auxcaracter == ".":
                self.ingresarBitacoraCSS("S4","S5",auxcaracter)
                self.lexema += auxcaracter
                self.S5(posInicial+1, posFinal)
                break

            # S4 -> S8
            elif auxcaracter.isalpha():
                self.S8(posInicial, posFinal)
                break

            # S4 -> S4
            elif auxcaracter == "%":
                self.ingresarBitacoraCSS("S4","S4",auxcaracter)
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
                self.ingresarBitacoraCSS("S5","S5",auxcaracter)
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)

            # S5 -> S8
            elif auxcaracter.isalpha():
                self.S8(posInicial, posFinal)
                break
            
            # S5 -> S5
            elif auxcaracter == "%":
                self.ingresarBitacoraCSS("S5","S5",auxcaracter)
                self.lexema += auxcaracter
                self.agregarToken(Tipo.PORCENTAJE, self.lexema)

            else:
                self.agregarErrores(posInicial, self.lexema)
            posInicial += 1

    def S6(self, posInicial):
        auxcaracter = ""

        while (posInicial < len(self.codigo)):
            auxcaracter = self.codigo[posInicial]
            
            # S6 -> S7
            if  auxcaracter == "*":
                self.ingresarBitacoraCSS("S6","S7",auxcaracter)
                self.lexema += auxcaracter   
                val = self.S7(posInicial+1)
                posInicial = val
                break

            # S6 -> S11
            elif auxcaracter == "/":
                self.ingresarBitacoraCSS("S6","S11",auxcaracter)
                tamaniolexema = self.getTamanioComentario(posInicial)
                posInicial = posInicial + tamaniolexema
                self.lexema = ""
                break
            #Esto se hizo de esta forma ya que si despues de un / se encuentra algun simbolo
            #que no sea / ó * entonces ese simbolo debe de ser analizado a partir del S0 y
            #se toma la / como un error lexico
            else:
                # S0
                posNueva = posInicial - 1
                posInicial = posNueva
                self.agregarErrores(posNueva, self.codigo[posNueva])
                break
            posInicial += 1
        return posInicial

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
                    self.ingresarBitacoraCSS("S7","S10","*/")
                    posInicial = posInicial+1
                    if auxpath != "":
                        self.list_path.append(auxpath)
                        self.lineaspath -= 1
                    break
                
                # S7 -> S7
                else:
                    self.ingresarBitacoraCSS("S7","S7",auxcaracter)
                    if self.lineaspath > 0:
                        auxpath += auxcaracter
                posInicial += 1                                
            else:
                self.agregarErrores(posError, self.codigo[posError])
                posInicial = posError
                break
        return posInicial

    def S8(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal
        aux_lexema = ""

        for x in range (inicial, final):
            aux_lexema += self.codigo[x]
        
        aux_lexema = aux_lexema.lower()
        
        if aux_lexema == "px" or aux_lexema == "em" or aux_lexema == "rem" or aux_lexema == "vh" or aux_lexema == "vw" or aux_lexema == "in" or aux_lexema == "cm" or aux_lexema == "mm" or aux_lexema == "pt" or aux_lexema == "pc":
            self.ingresarBitacoraCSS("S","S8",aux_lexema)
            self.lexema += aux_lexema
            self.agregarToken(Tipo.UNIDAD_MEDIDA, self.lexema)
            return
        else:
            self.agregarToken(Tipo.VALOR, self.lexema)
            for x in range (inicial, final):
                self.agregarErrores(x, self.codigo[x])

    def agregarErrores(self, posicion, valor):
        self.list_failure.append([posicion, valor, self.lineadeanalisis])
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
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "," or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo[i] == "/":
                break
            longitud += 1
        return longitud

    def getTamanioLexemaNumero(self, posInicial):
        longitud = 0    
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo[i] == "," or self.codigo[i] == "/" or self.codigo[i] == "*":
                break
            longitud += 1
        return longitud

    def getPosicionCierreD(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == '"' or self.codigo[i] == "'":
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
    
    def limpiarErrores(self):
        for i in reversed(self.list_failure):
            salida = self.codigo[:i[0]]+self.codigo[i[0]+1:]
            self.codigo = salida
    
    def ingresarBitacoraCSS(self, estadouno, estadodos, valor):
        self.bitacoracss.append([estadouno, estadodos, valor])
    
    def abrirErroresCSS(self):
        encabezado="""<html>
        <head><title>Errores del Archivo</title></head>
        <body>

        <h1>Errores</h1>

        <table border ='1'>
        <tr>
        <td><strong>No</strong></td>
        <td><strong>Posicion Caracter</strong></td>
        <td><strong>Descripcion</strong></td>
        </tr>
        """
        cuerpo = ""
        acum = 1
        for x in self.list_failure:
            cuerpo += "<tr><td>"+str(acum)+"</td>"+"<td>"+str(x[0])+"</td>"+"<td>"+x[1]+"</td></tr>"
            acum +=1

        pie ="""</body>
        </html> """
        completo = encabezado + cuerpo + pie
        
        archi1=open("errorcss.html", "w", encoding="utf-8")
        archi1.write(completo) 
        archi1.close()
        if acum != 1:
            self.cmd("start errorcss.html")

    def cmd(self, commando):
        subprocess.run(commando, shell=True)