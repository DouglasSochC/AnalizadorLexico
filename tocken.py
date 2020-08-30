
def tipoTocken(indice):
    respuesta = ""
    if indice == 1:
        respuesta = "CADENA"
    if indice == 2:
        respuesta = "SIMBOLO"
    if indice == 3:
        respuesta = "PALABRA_RESERVADA"    
    if indice == 4:
        respuesta = "NUMERO_ENTERO"
    if indice == 5:
        respuesta = "NUMERO_REAL"
    if indice == 6:
        respuesta = "SIGNO_MAS"
    if indice == 7:
        respuesta = "SIGNO_MEN"
    if indice == 8:
        respuesta = "SIGNO_POR"
    if indice == 9:
        respuesta = "SIGNO_DIV"
    if indice == 10:
        respuesta = "SIGNO_POW"
    if indice == 11:
        respuesta = "PRS_IZQ"
    if indice == 12:
        respuesta = "PRS_DER"
    return respuesta