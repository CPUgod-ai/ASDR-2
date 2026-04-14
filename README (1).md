# Parsers Descendentes Recursivos con Backtracking

## Introduccion

En este taller se implementan tres Analizadores Sintacticos Descendentes Recursivos (ASDR) con backtracking especulativo, uno por ejercicio. Cada gramatica presenta conflictos que impiden el analisis LL(1), y en algunos casos recursividad izquierda que debe eliminarse antes de implementar el parser. La funcion `intentar()` es el mecanismo central: guarda la posicion del parser, intenta una produccion, y la restaura si falla.

---

## Estructura del proyecto

Todos los archivos tienen que estar en la misma carpeta.

```
ASDR-2/
├── ejercicio1.py     <- ASDR ejercicio 1, eliminacion de recursividad en B
├── ejercicio2.py     <- ASDR ejercicio 2, recursividad indirecta S→B→A→S
├── ejercicio3.py     <- ASDR ejercicio 3, eliminacion de recursividad en S
└── README.md               
```

---

## Requisitos

```bash
python3 --version   # cualquier version 3.6 o superior
```

No requiere dependencias externas.

---

## Como ejecutarlo

```bash
python3 ejercicio1.py
python3 ejercicio2.py
python3 ejercicio3.py
```

Cada script imprime dos bloques: pruebas validas aceptadas y pruebas invalidas rechazadas con su motivo.

---

## Gramaticas y transformaciones

### Ejercicio 1 — recursividad directa en `B`

```
B → B cuatro C cinco  |  ε     <- se elimina introduciendo B'
B' → cuatro C cinco B'  |  ε   <- recursion derecha, segura para ASDR
```

### Ejercicio 2 — sin transformacion

```
S → B uno  |  dos C  |  ε      <- recursividad indirecta S→B→A→S
```

Se controla con orden de alternativas: `dos C` primero para cortar el ciclo antes de que se active.

### Ejercicio 3 — recursividad directa en `S`

```
S → S uno  |  A B C            <- se elimina introduciendo S'
S  → A B C S'
S' → uno S'  |  ε              <- S' absorbe los "uno" del ciclo original
```

---

## Analisis LL(1)

Ninguna de las tres gramaticas es LL(1).

| | Ejercicio 1 | Ejercicio 2 | Ejercicio 3 |
|---|---|---|---|
| **Transformacion** | Si, introduce `B'` | No | Si, introduce `S'` |
| **Conflictos** | `S`, `C` | `S`, `A`, `B` (5 conflictos) | `B`, `C` |
| **Riesgo de loop** | Bajo | Alto (`S→B→A→S`) | Ninguno |

---

## Salida por consola
Ejercicio 1
<img width="414" height="246" alt="image" src="https://github.com/user-attachments/assets/415d11e0-4932-4432-abca-46fe7f5881c2" />
Ejercicio 2
<img width="637" height="492" alt="image" src="https://github.com/user-attachments/assets/89b2b789-07e8-47ee-9f28-625c7c4c4c76" />
Ejercicio 3
<img width="653" height="498" alt="image" src="https://github.com/user-attachments/assets/1ceca368-f915-4738-9600-344e8f947f8d" />



## Mecanismo de backtracking

Los tres parsers comparten la misma estructura base:

```python
def intentar(funcion):
    global posicion
    pos_guardada = posicion       # snapshot antes de intentar
    try:
        funcion()
        return True               # produccion exitosa
    except Exception:
        posicion = pos_guardada  # restaurar si falla
        return False
```

**Regla de orden en las alternativas:**
1. Producciones con terminal fijo al inicio — primero, sin riesgo de recursion.
2. Producciones recursivas — despues.
3. Produccion `ε` — siempre al final, es el caso por defecto.

---

## Conclusion

Los tres ejercicios demuestran que la recursividad izquierda y los conflictos LL(1) no impiden construir un parser descendente recursivo: la recursividad directa se elimina mecanicamente con un no terminal auxiliar, la indirecta se controla con el orden de alternativas, y los conflictos se resuelven con backtracking especulativo. El precio es que el parser puede retroceder multiples veces, pero para gramaticas de este tamano el costo es despreciable.
