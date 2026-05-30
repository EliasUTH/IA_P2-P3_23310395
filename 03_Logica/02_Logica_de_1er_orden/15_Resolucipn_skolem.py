print("=== RESOLUCIÓN FOL: ALGORITMO DE SKOLEMIZACIÓN ===\n")
# Contadores globales para generar nombres únicos
contador_constantes = 1
contador_funciones = 1


def aplicar_sustitucion_skolem(termino, var_objetivo, reemplazo):
    """
    Recorre la estructura de un predicado y reemplaza la variable 
    existencial por su nueva Constante o Función de Skolem.
    """
    if isinstance(termino, str):
        return reemplazo if termino == var_objetivo else termino
    elif isinstance(termino, tuple):
        # Si es un predicado (ej. ("Ama", "x", "y")), aplicamos recursión
        return tuple(aplicar_sustitucion_skolem(arg, var_objetivo, reemplazo) for arg in termino)
    elif isinstance(termino, list):
        # Si es una lista de sentencias (ej. dentro de un AND)
        return [aplicar_sustitucion_skolem(t, var_objetivo, reemplazo) for t in termino]
    return termino



def skolemizar(expresion, contexto_universal=None):
    """
    Recorre el Árbol Sintáctico Abstracto (AST) de la fórmula lógica,
    rastrea los cuantificadores universales activos y elimina los existenciales.
    """
    global contador_constantes, contador_funciones
    if contexto_universal is None:
        contexto_universal = []


    # Caso Base: Si llegamos a un Predicado simple, lo retornamos tal cual
    if not isinstance(expresion, tuple) or expresion[0] not in ["ALL", "EXISTS", "AND", "OR", "NOT"]:
        return expresion
    operador = expresion[0]


    # --- REGLA 1: CUANTIFICADOR UNIVERSAL ---
    if operador == "ALL":
        var = expresion[1]
        cuerpo = expresion[2]
        # Agregamos la variable al contexto (las funciones de Skolem dependerán de ella)
        nuevo_contexto = contexto_universal + [var]
        cuerpo_skolemizado = skolemizar(cuerpo, nuevo_contexto)
        return ("ALL", var, cuerpo_skolemizado)


    # --- REGLA 2: CUANTIFICADOR EXISTENCIAL (El núcleo del algoritmo) ---
    elif operador == "EXISTS":
        var = expresion[1]
        cuerpo = expresion[2]
        

        if not contexto_universal:
            # No hay dependencia universal: Usamos una CONSTANTE de Skolem
            reemplazo = f"C_sk{contador_constantes}"
            contador_constantes += 1
            print(f"  [Skolem] Reemplazando '{var}' por Constante: {reemplazo}")
        else:
            # Hay dependencia: Usamos una FUNCIÓN de Skolem con las variables del contexto
            dependencias = ",".join(contexto_universal)
            reemplazo = f"F_sk{contador_funciones}({dependencias})"
            contador_funciones += 1
            print(f"  [Skolem] Reemplazando '{var}' por Función: {reemplazo} dependiente de {contexto_universal}")
            


        # Inyectamos el reemplazo en el cuerpo y eliminamos el "EXISTS"
        cuerpo_sustituido = aplicar_sustitucion_skolem(cuerpo, var, reemplazo)
        # Continuamos evaluando el interior por si hay más cuantificadores
        return skolemizar(cuerpo_sustituido, contexto_universal)



    # --- REGLA 3: OPERADORES LÓGICOS (Paso recursivo) ---
    elif operador in ["AND", "OR"]:
        # Skolemizamos ambas ramas de la operación
        rama_izq = skolemizar(expresion[1], contexto_universal)
        rama_der = skolemizar(expresion[2], contexto_universal)
        return (operador, rama_izq, rama_der)
    elif operador == "NOT":
        return ("NOT", skolemizar(expresion[1], contexto_universal))



# --- PRUEBAS DE LABORATORIO ---
def probar(nombre, formula):
    print(f"\n--- {nombre} ---")
    print(f"Original: {formula}")
    resultado = skolemizar(formula)
    print(f"Skolemizada: {resultado}")


# CASO 1: Existencial Puro (Genera Constante)
# "Existe alguien que es rico" -> EXISTS x (Rico(x))
f1 = ("EXISTS", "x", ("Rico", "x"))
probar("CASO 1: Constante", f1)


# CASO 2: Existencial Anidado en Universal (Genera Función)
# "Todo el mundo ama a alguien" -> ALL x (EXISTS y (Ama(x, y)))
f2 = ("ALL", "x", ("EXISTS", "y", ("Ama", "x", "y")))
probar("CASO 2: Función de Skolem", f2)


# CASO 3: Múltiples Dependencias
# "Para todo estudiante y todo curso, existe un libro que el estudiante usa en el curso"
# ALL e (ALL c (EXISTS l (Usa(e, c, l))))
f3 = ("ALL", "e", 
        ("ALL", "c", 
            ("EXISTS", "l", 
                ("Usa", "e", "c", "l")
            )
        )
     )


probar("CASO 3: Función Multi-Variable", f3)
print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Contexto Acumulativo: La lista 'contexto_universal' actúa como una memoria temporal que viaja por el árbol sintáctico hacia abajo. Si encuentra un ALL, memoriza la variable. Si encuentra un EXISTS, usa esa memoria para construir la función.")
print("2. Desaparición del Cuantificador: Nota que en la salida skolemizada, el nodo ('EXISTS', ...) desaparece por completo del árbol resultante. Esto simplifica la fórmula dejándola lista para la forma CNF.")
print("3. Unicidad Matemática: Es crucial que el generador cree funciones nuevas (F_sk1, F_sk2) cada vez. Reutilizar una función de Skolem implicaría matemáticamente afirmar que dos cosas distintas son obligatoriamente la misma.")