tokens = []        # lista de tokens generada al tokenizar la entrada
posicion = 0       # índice que apunta al token actual (lookahead)

def ver_siguiente():
    # Retorna el token actual sin consumirlo (lookahead de 1 símbolo)
    return tokens[posicion] if posicion < len(tokens) else '$'  # si no hay más tokens fin de cadena


def hacer_match(token_esperado):
    # Compara el token actual con el esperado
    # Si coinciden  avanza (consume el token)
    # Si no coinciden  lanza error (activa backtracking)
    global posicion
    if ver_siguiente() == token_esperado:
        posicion += 1  # avanzar al siguiente token
    else:
        raise SyntaxError(f"Se esperaba '{token_esperado}', se encontró '{ver_siguiente()}'")

def intentar(funcion):
    # Implementa backtracking:
    # - Guarda la posición actual
    # - Intenta aplicar una producción
    # - Si falla → restaura la posición
    global posicion
    pos_guardada = posicion
    try:
        funcion()         # intenta ejecutar la producción
        return True       # éxito → se mantiene avance
    except:
        posicion = pos_guardada  # fallo -volver al estado anterior
        return False

def parsear_S():
    # Se prueban las alternativas en orden usando backtracking

    if intentar(lambda: (parsear_B(), hacer_match('uno'))):  # S-B uno
        return

    if intentar(lambda: (hacer_match('dos'), parsear_C())):  # S-dos C
        return
                     

def parsear_A():
    

    if intentar(lambda: (parsear_S(), hacer_match('tres'), parsear_B(), parsear_C())):
        return

    if intentar(lambda: hacer_match('cuatro')):  # A -cuatro
        return


def parsear_B():

    if intentar(lambda: (parsear_A(), hacer_match('cinco'), parsear_C(), hacer_match('seis'))):
        return


def parsear_C():

    if intentar(lambda: (hacer_match('siete'), parsear_B())):
        return
    
def parsear(entrada):
    # Función principal:
    # - Tokeniza la entrada
    # - Inicia el análisis desde S
    # - Verifica que no queden tokens sobrantes

    global tokens, posicion

    tokens = entrada.split()   
    posicion = 0               # iniciar desde el primer token

    parsear_S()                # comenzar desde el símbolo inicial

    # Si aún quedan tokens  error sintáctico
    if ver_siguiente() != '$':
        raise SyntaxError(f"Tokens sobrantes desde '{ver_siguiente()}'")

    print(f"Cadena aceptada: '{entrada if entrada else 'ε'}'")


#  PRUEBAS 

if __name__ == "__main__":

    # Cadenas válidas según la gramática
    pruebas_validas = [
        "",                 
        "uno",              
        "dos",            
        "dos siete",        
        "cuatro cinco seis uno",
        "dos siete cuatro cinco seis"
    ]

    # Cadenas inválidas (no cumplen la gramática)
    pruebas_invalidas = [
        "dos dos",
        "cinco seis",
        "siete",
        "dos dos siete",
        "cuatro cuatro"
    ]

    print("PRUEBAS VÁLIDAS:")
    for cadena in pruebas_validas:
        try:
            parsear(cadena)
        except Exception as e:
            print(f" Error inesperado en '{cadena}': {e}")

    print("\nPRUEBAS INVÁLIDAS:")
    for cadena in pruebas_invalidas:
        try:
            parsear(cadena)
            print(f" Debería fallar pero pasó: '{cadena}'")
        except:
            print(f" Correctamente rechazada: '{cadena}'")