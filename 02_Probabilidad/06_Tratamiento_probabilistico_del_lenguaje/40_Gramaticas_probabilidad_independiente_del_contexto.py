import random

print("=== GRAMÁTICA PROBABILÍSTICA INDEPENDIENTE DEL CONTEXTO (PCFG) ===\n")

# --- 1. DEFINICIÓN DE LA GRAMÁTICA ---
# Estructura: { NoTerminal: [ ( [Producción], Probabilidad ) ] }
# Las probabilidades de cada NoTerminal deben sumar 1.0
pcfg = {
    "S": [
        (["NP", "VP"], 1.0)
    ],
    "NP": [
        (["Det", "N"], 0.7),
        (["NombrePropio"], 0.3)
    ],
    "VP": [
        (["V", "NP"], 0.6),
        (["V"], 0.4)
    ],
    "Det": [
        (["el"], 0.6),
        (["un"], 0.4)
    ],
    "N": [
        (["robot"], 0.5),
        (["científico"], 0.5)
    ],
    "NombrePropio": [
        (["Gemini"], 0.5),
        ([" Turing"], 0.5)
    ],
    "V": [
        (["estudia"], 0.5),
        (["crea"], 0.5)
    ]
}

# --- 2. MOTOR DE GENERACIÓN ESTOCÁSTICA ---

def generar(simbolo):
    """Expande un símbolo basado en las probabilidades de la gramática."""
    # Si el símbolo no está en la gramática, es un terminal (palabra)
    if simbolo not in pcfg:
        return [simbolo]
    
    # Elegir una regla de producción basada en su peso
    producciones = pcfg[simbolo]
    opciones = [p[0] for p in producciones]
    pesos = [p[1] for p in producciones]
    
    # Elección probabilística
    eleccion = random.choices(opciones, weights=pesos)[0]
    
    # Expandir recursivamente cada símbolo de la elección
    resultado = []
    for s in eleccion:
        resultado.extend(generar(s))
    
    return resultado

# --- 3. EJECUCIÓN ---

print("Generando oraciones aleatorias basadas en probabilidades...")
print("-" * 60)

for i in range(5):
    oracion = generar("S")
    texto = " ".join(oracion).replace("  ", " ").strip()
    print(f"Oración {i+1}: {texto.capitalize()}.")

print("-" * 60)
print("\n=== ANÁLISIS TÉCNICO ===")
print("1. El símbolo inicial 'S' se expande siguiendo las reglas de probabilidad.")
print("2. La recursividad permite que la gramática sea 'Independiente del Contexto'.")
print("3. NP (Sujeto) tiene un 70% de ser 'Articulo + Sustantivo' y 30% un 'Nombre Propio'.")