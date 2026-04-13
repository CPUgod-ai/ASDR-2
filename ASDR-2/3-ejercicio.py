# estado global
tokens   = []
posicion = 0

#  utilidades 

def ver_siguiente():
    return tokens[posicion] if posicion < len(tokens) else '$'  # '$' = fin de cadena

def hacer_match(token_esperado):
    global posicion
    if ver_siguiente() == token_esperado:
        posicion += 1                          # consumir token si coincide
    else:
        raise SyntaxError(                     # activar backtracking en el llamador
            f"Se esperaba '{token_esperado}', se encontró '{ver_siguiente()}'"
        )

def intentar(funcion):
    global posicion
    pos_guardada = posicion                    # snapshot antes de intentar la producción
    try:
        funcion()
        return True                            # producción aplicada con éxito
    except Exception:
        posicion = pos_guardada               # restaurar: producción descartada
        return False

# no terminales 

def parsear_S():
    
    # No hay alternativas aquí: si A, B, C o S' fallan, todo falla
    parsear_A()
    parsear_B()
    parsear_C()
    parsear_Sp()

def parsear_Sp():
    # PRED(S'→uno S') = {uno}  sin conflicto con PRED(S'→ε) = {$}  → esta sí es LL(1)
    if intentar(lambda: (hacer_match('uno'), parsear_Sp())):  # S' → uno S'  (recursión derecha)
        return
    # S' → ε

def parsear_A():
    # PRED(A→dos B C) = {dos} y PRED(A→ε) = {cuatro,tres,uno,$} → sin solapamiento → LL(1) local
    if intentar(lambda: (hacer_match('dos'), parsear_B(), parsear_C())):  # A → dos B C
        return
    # A → ε

def parsear_B():
    # Backtracking: intentar C tres primero. Si C consume 'cuatro' pero no hay 'tres' → retrocede → B→ε
    if intentar(lambda: (parsear_C(), hacer_match('tres'))):  # B → C tres
        return
    

def parsear_C():
    
    if intentar(lambda: (hacer_match('cuatro'), parsear_B())):  # C → cuatro B
        return
    

# punto de entrada 

def parsear(entrada):
    global tokens, posicion
    tokens   = entrada.split()    # tokenizar; entrada vacía "" → lista vacía []
    posicion = 0
    parsear_S()
    if ver_siguiente() != '$':    # tokens sin consumir → cadena inválida
        raise SyntaxError(
            f"Tokens sobrantes a partir de '{ver_siguiente()}': "
            f"cadena no pertenece al lenguaje"
        )
    print(f"  Aceptada : '{entrada if entrada else 'ε'}'")

#  pruebas 

if __name__ == "__main__":
    pruebas_validas = [
        "",
        "uno",
        "uno uno",
        "dos",
        "dos tres",
        "cuatro",
        "cuatro tres",
        "dos cuatro tres",
        "cuatro uno",
        "dos cuatro tres uno uno",
    ]

   
    pruebas_invalidas = [
        "dos dos",
        "dos uno dos",
        "cuatro cuatro",
        "cuatro tres cuatro",
        "uno cuatro",
        "dos tres dos",
    ]

    print("=" * 55)
    print("  PRUEBAS VÁLIDAS")
    print("=" * 55)
    for cadena in pruebas_validas:
        try:
            parsear(cadena)
        except Exception as e:
            print(f"  Error inesperado en '{cadena}': {e}")

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