
reserved_word = [
    ["if","IF"],
    ["else","ELSE"],
    ["int","INT"],
    ["string","STRING"],
    ["char","CHAR"],
    ["boolean","BOOLEAN"],
    ["var","VAR"],
    ["true","TRUE"],
    ["false","FALSE"]
    ]
estado = 0
auxlexico = ""

#"Verificador de Linea de Codigo": Este es un acumulador el cual sirve
#como pivote para determinar en que linea del codigo existe un error
#de analisis lexico.
vlc = 1

errores = []

def DatoNuevo():
    pass

def lexer(entrada):
    estado = 0
    tokens = []
    token = ""
    
    for caracter in entrada:
        
        print (caracter)

        if estado == 0:
            
            if caracter == " " or caracter == "" or caracter == "\n" or caracter == '"' or caracter == "(":
                estado = 4
            else:
                if caracter.isdigit():
                    estado = 1
                else:
                    if caracter.isalpha():                    
                        estado = 2
                    else:
                        estado = 3

        if estado == 1:
            token += caracter
            estado = 0
        
        if estado == 2:
            token += caracter
            estado = 0
        
        if estado == 3:
            token += caracter
            estado = 0

        if estado == 4:
            if token != "" or token != "\n" or token != '':
                tokens.append(token)
                token = ""
            #Aqui debe de analizarse si es un simbolo como los estados de 
            #aceptacion o si es un error lexico
            #token = ""
            estado = 0
        
        estado = 0        
    print(tokens)
    return ""