from tockenhtml import Token
from tockenhtml import Tipo
import subprocess
# El video de la explicacion de este codigo es el video del 26/08/20

class AnalyzerHTML:

    list_tockens = []
    list_path = []
    list_failure = list()
    post_errors = list()
    caracter = ""
    lexema = ""
    codigo = ""
    lineaspath = 2
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
            
            # S0 -> Sq (Simbolos del Lenguaje)
            if self.caracter == "/":
                self.agregarToken(Tipo.DIAGONAL , self.caracter)
            
            elif self.caracter == "=":
                self.agregarToken(Tipo.IGUAL, self.caracter)

            elif self.caracter == '"':
                # S0 -> S8
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                # S8 -> S8
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    self.lexema += self.codigo[x]
                self.agregarToken(Tipo.VALOR , self.lexema)
                # S8 -> S9
                self.agregarToken(Tipo.DOBLECOMILLA, self.caracter)
                posicion = posicion+tamanio_lexema+1
            
            elif self.caracter == "'":
                # S0 - S10
                self.agregarToken(Tipo.COMILLA, self.caracter)
                tamanio_lexema = self.getPosicionCierreD(posicion+1)
                # S10 -> S10
                for x in range(posicion+1, posicion+1+tamanio_lexema):
                    self.lexema += self.codigo[x]
                # S10 -> S11
                self.agregarToken(Tipo.VALOR , self.lexema)
                posicion = posicion+tamanio_lexema+1            

            elif self.caracter == ">":
                # S0 -> S12
                self.agregarToken(Tipo.MAYOR , self.caracter)
                tamanio_lexema = self.getPosicionCierre(posicion)
                # S12 -> S12
                for x in range(posicion+1, posicion+tamanio_lexema):
                    self.lexema += self.codigo[x]
                # S13 -> S13
                self.agregarToken(Tipo.VALOR , self.lexema)
                posicion = posicion+tamanio_lexema-1

            # S0 -> S5
            elif self.caracter == "<":
                self.lexema += self.caracter
                val = self.S5(posicion+1)
                posicion = val
            
            # S0 -> S1
            elif self.caracter.isalpha():
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S1(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1
            
            # S0 -> S3
            elif self.caracter.isnumeric():
                tamanio_lexema = self.getTamanioLexemaTexto(posicion)
                self.S3(posicion, posicion+tamanio_lexema)
                posicion = posicion+tamanio_lexema-1

            elif self.caracter == " " or self.caracter == "\t" or self.caracter=="\n":
                posicion +=1
                continue
            else:
                self.agregarErrores(posicion, self.caracter)
            posicion += 1
        
        self.limpiarErrores()
        for p in self.list_path:
            if len(p.replace("PATHW:","")) != len(p):
                
                nameFile= p.replace("PATHW:","").replace(" ","")+"\salidahtml.html"
                if nameFile!='':
                    contenido=self.codigo
                    archi1=open(nameFile, "w", encoding="utf-8")
                    archi1.write(contenido) 
                    archi1.close()
        self.abrirErroresHTML()
        self.list_failure.clear()
        self.list_tockens.clear()
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
        
        self.lexema = ""
        while  (inicial < final):
            auxcaracter = self.codigo[inicial]
            # S1 -> S2
            if auxcaracter.isalpha():                
                self.S2(inicial, final)
                break
            else:
                self.agregarErrores(inicial, auxcaracter)
            inicial += 1

    def S2(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S2 -> S2
            if auxcaracter.isalpha():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)
            # S2 -> S2
            elif auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.ID, self.lexema)  
            else:
                self.agregarErrores(posInicial, auxcaracter)
            posInicial += 1

    def S3(self, posInicial, posFinal):
        auxcaracter = ""
        while  (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]

            # S3 -> S3
            if auxcaracter.isnumeric():
                self.lexema += auxcaracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            elif auxcaracter == ".":
                if  (posInicial == posFinal):
                    self.lexema += auxcaracter
                    self.S4(posInicial, posFinal)
                break
            else:
                self.agregarErrores(posInicial, auxcaracter)
            posInicial += 1

    def S4(self, posInicial, posFinal):
        caracter = ""
        while  (posInicial < posFinal):
            caracter = self.codigo[posInicial]

            # S4 -> S4
            if caracter.isnumeric():
                self.lexema += caracter
                if  (posInicial+1 == posFinal):
                    self.agregarToken(Tipo.VALOR, self.lexema)
            else:
                self.agregarErrores(posInicial, self.caracter)
            posInicial += 1

    def S5(self, posInicial):
        auxcaracter = ""
        posFinal = len(self.codigo)
        while (posInicial < posFinal):
            auxcaracter = self.codigo[posInicial]
            if  (posInicial+2) > posFinal:
                posInicial = posFinal-1
                break
            else:
                # S5 -> S6
                if  auxcaracter == "!" and self.codigo[posInicial + 1] == "-" and self.codigo[posInicial + 2] == "-":
                    self.lexema = ""  
                    val = self.S6(posInicial+3)
                    posInicial = val
                    break
                else: 
                    self.agregarToken(Tipo.MENOR, self.lexema)
                    posInicial -= 1
                    break               
            posInicial += 1
        return posInicial

    def S6(self, posInicial):
        auxcaracter = ""
        posFinal = len(self.codigo)
        auxpath = ""
        while (posInicial < posFinal):
            
            auxcaracter = self.codigo[posInicial]

            if posInicial+2 != posFinal-1:
                # S6 -> S7
                if  auxcaracter == "-" and self.codigo[posInicial + 1] == "-" and self.codigo[posInicial + 2] == ">":
                    posInicial = posInicial+2
                    if auxpath != "":
                        self.list_path.append(auxpath)
                        self.lineaspath -= 1
                    break
                else:
                    if self.lineaspath > 0:
                        auxpath += auxcaracter
                posInicial += 1
            else:
                posInicial = posFinal - 1
                break
        return posInicial

    def agregarErrores(self, tipo, valor):
        #self.list_tockens.append(nuevo)
        self.list_failure.append([tipo, valor])

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

    def getPosicionCierre(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.codigo)-1):
            if self.codigo[i] == "<":
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
    
    def limpiarErrores(self):
        for i in reversed(self.list_failure):
            salida = self.codigo[:i[0]]+' '+self.codigo[i[0]+1:]
            self.codigo = salida
    
    def abrirErroresHTML(self):
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
        
        archi1=open("errorhtml.html", "w", encoding="utf-8")
        archi1.write(completo) 
        archi1.close()
        if acum != 1:
            self.cmd("start errorhtml.html")

    def cmd(self, commando):
        subprocess.run(commando, shell=True)