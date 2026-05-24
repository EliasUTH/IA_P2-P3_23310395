import random

print("=== GRAMÁTICA PROBABILÍSTICA LEXICALIZADA (LPCFG) ===\n")

# --- 1. DEFINICIÓN DE LA GRAMÁTICA LEXICALIZADA ---
# Estructura: (NoTerminal, PalabraCabeza) -> [([Producciones], Probabilidad)]
# Nota: La palabra cabeza se hereda de los hijos para dar coherencia.
l_pcfg = {
    ("S", "come"): [
        (["NP(robot)", "VP(come)"], 1.0)
    ],
    ("NP", "robot"): [
        (["Det(el)", "N(robot)"], 1.0)
    ],
    ("VP", "come"): [
        (["V(come)", "NP(aceite)"], 0.7),
        (["V(come)", "NP(manzana)"], 0.3)
    ],
    ("NP", "aceite"): [
        (["N(aceite)"], 1.0)
    ],
    ("NP", "manzana"): [
        (["Det(una)", "N(manzana)"], 1.0)
    ],
    # Producciones Terminales
    ("Det", "el"): [ (["el"], 1.0) ],
    ("Det", "una"): [ (["una"], 1.0) ],
    ("N", "robot"): [ (["robot"], 1.0) ],
    ("N", "aceite"): [ (["aceite"], 1.0) ],
    ("N", "manzana"): [ (["manzana"], 1.0) ],
    ("V", "come"): [ (["come"], 1.0) ]
}

# --- 2. MOTOR DE EXPANSIÓN LEXICALIZADA ---

def expandir_lexicalizado(no_terminal, cabeza):
    llave = (no_terminal, cabeza)
    
    if llave not in l_pcfg:
        return [cabeza] # Es un terminal
    
    # Seleccionar regla basada en la cabeza léxica
    reglas = l_pcfg[llave]
    produccion = random.choices([r[0] for r in reglas], [r[1] for r in reglas])[0]
    
    resultado = []
    for hijo in produccion:
        # Extraer el nuevo NoTerminal y su cabeza (ej: "VP(come)" -> "VP", "come")
        if "(" in hijo:
            nuevo_nt = hijo.split("(")[0]
            nueva_cabeza = hijo.split("(")[1].replace(")", "")
            resultado.extend(expandir_lexicalizado(nuevo_nt, nueva_cabeza))
        else:
            resultado.append(hijo)
            
    return resultado

# --- 3. EJECUCIÓN ---

print("Generando oraciones donde el verbo dicta la estructura de los objetos...")
print("-" * 65)

for i in range(5):
    # Iniciamos con la oración cuya cabeza es el verbo principal "come"
    palabras = expandir_lexicalizado("S", "come")
    oracion = " ".join(palabras).strip()
    print(f"Oración {i+1}: {oracion.capitalize()}.")

print("-" * 65)
print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Lexicalización: Cada regla conoce su 'cabeza' (el núcleo semántico).")
print("2. Coherencia: El verbo 'come' prefiere 'aceite' (70%) sobre 'manzana' (30%)")
print("   porque en este corpus simulado, el sujeto es un robot.")
print("3. Estructura: Las dependencias léxicas resuelven la ambigüedad de adjunción.")