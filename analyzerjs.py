from tockenjs import Token
from tockenjs import Tipo
import subprocess
import os
# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerJS:

    list_tockens = []
    list_path = []
    list_failure = list()
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
    lineaspath = 2 
    errores = []   
    reporte = []
    cantidadgrafos = 2

    def lexer(self, entrada):
        posicion = 0
        while posicion < len(entrada):
            self.codigo = entrada
            self.caracter = entrada[posicion]
            
            # S0 -> S1 (Simbolos del Lenguaje)
            if self.caracter == "(":
                if self.cantidadgrafos == 2:
                    self.ingresarGrafo("S1",["S0","S1",self.caracter])
                    self.cantidadgrafos -= 1
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
            
            # S0 -> S12
            elif self.caracter == '"':
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                # S12 - > S12
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    self.lexema += self.codigo[x]
                self.agregarToken(Tipo.VALOR , self.lexema)
                # S12 -> S13
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                posicion = posicion+tamanio_lexema+1
            
            # S0 -> S14
            elif self.caracter == "'":
                self.agregarToken(Tipo.COMILLA, self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                # S14 -> S14
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    self.lexema += self.codigo[x]
                # S14 -> S15
                self.agregarToken(Tipo.VALOR , self.lexema)
                posicion = posicion+tamanio_lexema+1
            
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
        
        self.limpiarErrores()
        for p in self.list_path:
            if len(p.replace("PATHW","")) != len(p):
                
                nameFile= p.replace("PATHW","").replace(" ","").replace("->","")+"\salidajs.js"
                if nameFile!='':
                    contenido=self.codigo
                    archi1=open(nameFile, "w", encoding="utf-8")
                    archi1.write(contenido) 
                    archi1.close()
        self.abrirErroresJS()
        self.imagenAFD()
        self.list_failure.clear()
        self.list_tockens.clear()
        return ""
    
    def S2(self, posInicial, posFinal):
        inicial = posInicial
        final = posFinal

        for x in range (inicial, final):
            self.lexema += self.codigo[x]
        
        aux_lexema = self.lexema.lower()

        if aux_lexema == "var":
            if self.cantidadgrafos == 1:
                self.ingresarGrafo("S2",["S0","S2",aux_lexema])
                self.cantidadgrafos -= 1
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
            # S3 -> S3
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

            # S4 -> S5
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
            
            # S6 -> S7
            if  auxcaracter == "*":
                self.lexema += auxcaracter   
                val = self.S7(posInicial+1)
                posInicial = val
                break
            
            # S6 -> S11
            elif auxcaracter == "/":
                tamaniolexema = self.getTamanioComentario(posInicial)
                posInicial = posInicial + tamaniolexema
                self.lexema = ""
                break
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
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "." or self.codigo[i] == "," or self.codigo[i] == "=" or self.codigo == "<" or self.codigo == ">" or self.codigo[i] == "+" or self.codigo[i] == "-" or self.codigo[i] == "!" or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo == "|" or self.codigo == "&" or self.codigo[i] == '/':
                break
            longitud += 1
        return longitud

    def getTamanioLexemaNumero(self, posInicial):  
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == " " or self.codigo[i] == "(" or self.codigo[i] == ")" or self.codigo[i] == "{" or self.codigo[i] == "}" or self.codigo[i] == ";" or self.codigo[i] == ":" or self.codigo[i] == "," or self.codigo[i] == "=" or self.codigo == "<" or self.codigo == ">" or self.codigo[i] == "+" or self.codigo[i] == "-" or self.codigo[i] == "!" or self.codigo[i] == "*" or self.codigo[i] == '"' or self.codigo[i] == "'" or self.codigo[i] == "\n" or self.codigo == "|" or self.codigo == "&" or self.codigo[i] == '/':
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
            salida = self.codigo[:i[0]]+' '+self.codigo[i[0]+1:]
            self.codigo = salida

    def abrirErroresJS(self):
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
        
        archi1=open("errorjs.html", "w", encoding="utf-8")
        archi1.write(completo) 
        archi1.close()
        if acum != 1:
            self.cmd("start errorjs.html")

    def cmd(self, commando):
        subprocess.run(commando, shell=True)

    def ingresarGrafo(self, estadosaceptacion, transiciones):
        self.reporte.append([estadosaceptacion, transiciones])

    def imagenAFD(self):
        encabezado = 'digraph unix {\n'+ 'size="5,6";\n'+ 'rankdir="LR";\n'
        
        estadosaceptacion = ""

        for x in self.reporte:
            estadosaceptacion = estadosaceptacion+","+x[0]
        primeraparte = "node [shape = doublecircle]"+estadosaceptacion[1:]+";\n"
        cuerpo = ""
        for x in self.reporte:
            cuerpo = cuerpo+x[1][0]+" -> "+x[1][1]+' [label="'+x[1][2]+'"] \n'
        
        final = "}"
        texto = encabezado+primeraparte+cuerpo+final
        nombre = "imagen"+str(self.cantidadgrafos)+".txt"
        objFichero = open(nombre,'w')
        nuevotexto = texto
        objFichero.write(nuevotexto)
        objFichero.close()

        os.system("dot -Tpng "+nombre+" -o imagenproyecto.png")   