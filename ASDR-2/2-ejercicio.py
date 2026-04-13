import sys
sys.setrecursionlimit(500)   # suficiente para cadenas de prueba, evita loops silenciosos

#  estado global 
tokens   = []
posicion = 0


def ver_siguiente():
    return tokens[posicion] if posicion < len(tokens) else '$'  # '$' = fin de cadena

def hacer_match(token_esperado):
    global posicion
    if ver_siguiente() == token_esperado:
        posicion += 1                         # consumir token si coincide
    else:
        raise SyntaxError(                    # lanzar error para activar backtracking
            f"Se esperaba '{token_esperado}', se encontró '{ver_siguiente()}'"
        )

def intentar(funcion):
    global posicion
    pos_guardada = posicion                   # snapshot antes de intentar
    try:
        funcion()
        return True                           # producción exitosa, posición avanzada
    except Exception:
        posicion = pos_guardada              # restaurar: como si no se hubiera intentado
        return False

# no terminales

def parsear_S():
    # terminal fijo, se intenta primero para cortar recursividad indirecta
    if intentar(lambda: (hacer_match('dos'), parsear_C())):          # S -dos C
        return
    #  Se intenta después del caso seguro
    if intentar(lambda: (parsear_B(), hacer_match('uno'))):           # S - B uno
        return
    # no consumir nada, no lanzar error

def parsear_A():
    # terminal fijo, sin riesgo de recursión
    if intentar(lambda: hacer_match('cuatro')):                       
        return
    #  puede derivar en e, así que puede avanzar o no
    if intentar(lambda: (parsear_S(), hacer_match('tres'), parsear_B(), parsear_C())):
        return
   

def parsear_B():

    if intentar(lambda: (parsear_A(), hacer_match('cinco'), parsear_C(), hacer_match('seis'))):  
        return
    

def parsear_C():
    
    if intentar(lambda: (hacer_match('siete'), parsear_B())):         
        return
    

# punto de entrada

def parsear(entrada):
    global tokens, posicion
    tokens   = entrada.split()    # tokenizar por espacios; "" → []
    posicion = 0
    parsear_S()
    if ver_siguiente() != '$':    # si quedan tokens S no los consumió → inválida
        raise SyntaxError(
            f"Tokens sobrantes a partir de '{ver_siguiente()}': "
            f"cadena no pertenece al lenguaje"
        )
    print(f"   Aceptada : '{entrada if entrada else 'ε'}'")

# pruebas

if __name__ == "__main__":
    pruebas_validas = [
        "",
        "dos",
        "uno",
        "dos siete",
        "cinco seis uno",
        "cuatro cinco seis uno",
        "cuatro cinco siete seis uno",
        "dos siete cinco seis",
    ]

    pruebas_invalidas = [
        "dos dos",
        "uno uno",
        "siete siete",
        "cuatro cuatro",
        "tres",
        "seis",
        "siete",
    ]

    print("=" * 55)
    print("  PRUEBAS VÁLIDAS")
    print("=" * 55)
    for cadena in pruebas_validas:
        try:
            parsear(cadena)
        except Exception as e:
            print(f"   Error inesperado en '{cadena}': {e}")

    print()
    print("=" * 55)
    print("  PRUEBAS INVÁLIDAS")
    print("=" * 55)
    for cadena in pruebas_invalidas:
        try:
            parsear(cadena)
            print(f"   Debería fallar pero fue aceptada: '{cadena}'")
        except SyntaxError as e:
            print(f"   Rechazada : '{cadena}'")
            print(f"    Motivo    : {e}")
        except RecursionError:
            print(f"   Loop infinito detectado en: '{cadena}'")