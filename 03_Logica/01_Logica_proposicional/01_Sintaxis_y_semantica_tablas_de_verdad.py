import itertools
print("=== LÓGICA PROPOSICIONAL: SINTAXIS Y SEMÁNTICA ===\n")
# --- 1. SEMÁNTICA (Definición del significado de los operadores) ---
# Python ya incluye 'and', 'or', 'not'. Solo necesitamos definir los más avanzados.

def IMPLICA(p, q):
    """
    Condicional material (p => q).
    Solo es falso cuando p es Verdadero y q es Falso.
    """
    return (not p) or q



def EQUIVALE(p, q):
    """
    Bicondicional (p <=> q).
    Es verdadero si ambas variables tienen el mismo valor de verdad.
    """
    return p == q



# --- 2. SINTAXIS (Generador de Tablas de Verdad) ---
def tabla_de_verdad(variables, expresion, nombre_expresion="Expresión"):
    """
    Genera y muestra la tabla de verdad para cualquier fórmula proposicional.
    """
    # itertools.product genera todas las combinaciones posibles de True/False
    # Para n variables, genera 2^n filas.
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    # Imprimir encabezado de la tabla
    encabezado = " | ".join(variables) + f" || {nombre_expresion}"
    print("-" * len(encabezado))
    print(encabezado)
    print("-" * len(encabezado))
    # Evaluar la semántica para cada fila (cada combinación sintáctica)
    for valores in combinaciones:
        # Creamos un diccionario vinculando el nombre de la variable con su valor actual (V o F)
        entorno = dict(zip(variables, valores))
        # Evaluamos la expresión pasando las variables del entorno
        resultado = expresion(**entorno)
        # Formateo visual (Cambiamos True/False por V/F)
        fila_str = " | ".join(["V" if v else "F" for v in valores])
        res_str = "V" if resultado else "F"
        # Imprimir fila alineada
        print(f"{fila_str} ||    {res_str}")
    print("-" * len(encabezado) + "\n")



# --- 3. EJECUCIÓN Y PRUEBAS ---
# Caso A: Modus Ponens básico: (P AND Q) => R
variables_a = ["P", "Q", "R"]
# Usamos lambda para representar la fórmula sintáctica
formula_a = lambda P, Q, R: IMPLICA(P and Q, R)
print("Caso A: Si llueve (P) y salgo (Q), entonces me mojo (R).")
tabla_de_verdad(variables_a, formula_a, "(P ^ Q) => R")



# Caso B: Tautología (siempre es verdad): P OR NOT P
variables_b = ["P"]
formula_b = lambda P: P or (not P)
print("Caso B: Ley del Tercio Excluso (Tautología).")
tabla_de_verdad(variables_b, formula_b, "P v ~P")



print("=== ANÁLISIS DEL EXPERTO ===")
print("1. SINTAXIS: La estructura de la oración está definida por la función 'lambda'.")
print("2. SEMÁNTICA: La tabla demuestra el significado exacto evaluando V/F.")
print("3. ESCALABILIDAD: El código calcula 2^N escenarios automáticamente.")