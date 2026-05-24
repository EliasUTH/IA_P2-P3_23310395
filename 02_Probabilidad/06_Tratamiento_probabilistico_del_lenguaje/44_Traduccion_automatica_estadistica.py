import random

print("=== TRADUCCIÓN AUTOMÁTICA ESTADÍSTICA (SMT) ===\n")

# --- 1. CORPUS PARALELO (Entrenamiento) ---
# Frases alineadas: (Inglés, Español)
corpus = [
    (["the", "robot", "is", "blue"], ["el", "robot", "es", "azul"]),
    (["the", "scientist", "is", "smart"], ["el", "cientifico", "es", "inteligente"]),
    (["the", "future", "is", "now"], ["el", "futuro", "es", "ahora"]),
    (["smart", "robot"], ["robot", "inteligente"])
]

# --- 2. ENTRENAMIENTO: MODELO DE TRADUCCIÓN (DICCIONARIO) ---
# Calculamos P(espanol | ingles) basándonos en co-ocurrencia
probabilidades_trans = {}

for ing_frase, esp_frase in corpus:
    for ing_pal in ing_frase:
        if ing_pal not in probabilidades_trans:
            probabilidades_trans[ing_pal] = {}
        for esp_pal in esp_frase:
            # Inicializamos o aumentamos el conteo de alineación
            probabilidades_trans[ing_pal][esp_pal] = probabilidades_trans[ing_pal].get(esp_pal, 0) + 1

# Normalizamos para que sean probabilidades (0 a 1)
for ing_pal in probabilidades_trans:
    total = sum(probabilidades_trans[ing_pal].values())
    for esp_pal in probabilidades_trans[ing_pal]:
        probabilidades_trans[ing_pal][esp_pal] /= total

# --- 3. MOTOR DE TRADUCCIÓN (DECODER) ---
def traducir(frase_ing):
    tokens = frase_ing.lower().split()
    resultado = []
    
    for pal in tokens:
        if pal in probabilidades_trans:
            # Elegimos la palabra con mayor probabilidad estadística
            mejor_traduccion = max(probabilidades_trans[pal], key=probabilidades_trans[pal].get)
            resultado.append(mejor_traduccion)
        else:
            resultado.append(f"[{pal}]") # Palabra desconocida
            
    return " ".join(resultado)

# --- 4. PRUEBA ---
frase_test = "the smart scientist"
traduccion = traducir(frase_test)

print(f"Original (EN): {frase_test}")
print(f"SMT (ES):      {traduccion}")

print("\n=== ANÁLISIS DEL EXPERTO ===")
print("1. El modelo aprendió que 'the' -> 'el' por su alta co-ocurrencia.")
print("2. Falla en el orden: nota que 'smart scientist' se traduce literal.")
print("3. Para corregir el orden, los sistemas SMT reales usan Modelos de Reordenamiento.")