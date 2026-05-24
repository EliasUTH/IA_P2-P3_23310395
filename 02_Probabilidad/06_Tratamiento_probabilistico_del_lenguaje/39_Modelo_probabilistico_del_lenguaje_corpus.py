import random

print("=== MODELO PROBABILÍSTICO DEL LENGUAJE (Bigramas) ===\n")

# --- 1. EL CORPUS (Datos de entrenamiento) ---
# Puedes ampliar este texto con cualquier párrafo largo
corpus = """
la inteligencia artificial es el futuro de la computación
la computación es una herramienta poderosa para la ciencia
la ciencia busca entender la inteligencia humana y la artificial
el futuro de la ciencia depende de la computación avanzada
"""

# --- 2. PREPROCESAMIENTO ---
# Limpiamos y tokenizamos el texto
tokens = corpus.lower().split()

# --- 3. ENTRENAMIENTO DEL MODELO ---
# Creamos un diccionario de frecuencias: {palabra_actual: {siguiente_palabra: conteo}}
modelo = {}

for i in range(len(tokens) - 1):
    actual = tokens[i]
    siguiente = tokens[i+1]
    
    if actual not in modelo:
        modelo[actual] = {}
    
    modelo[actual][siguiente] = modelo[actual].get(siguiente, 0) + 1

# --- 4. GENERACIÓN DE TEXTO ---
def generar_texto(palabra_inicio, longitud=10):
    if palabra_inicio not in modelo:
        return "La palabra inicial no está en el corpus."
    
    frase = [palabra_inicio]
    palabra_actual = palabra_inicio
    
    for _ in range(longitud - 1):
        # Obtenemos las posibles siguientes palabras y sus pesos
        opciones = list(modelo[palabra_actual].keys())
        pesos = list(modelo[palabra_actual].values())
        
        # Selección probabilística (Ruleta de Darwin/Monte Carlo)
        siguiente = random.choices(opciones, weights=pesos)[0]
        frase.append(siguiente)
        palabra_actual = siguiente
        
        if palabra_actual not in modelo:
            break # Fin de la cadena si no hay transiciones
            
    return " ".join(frase)

# --- 5. RESULTADOS ---
print("Modelado completado.")
print("-" * 50)
palabra_semilla = "la"
texto_generado = generar_texto(palabra_semilla, longitud=12)

print(f"Palabra inicial: '{palabra_semilla}'")
print(f"Texto generado:  '{texto_generado}...'")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. La IA no 'escribe' con sentido común, sino siguiendo la estadística del corpus.")
print("2. 'random.choices' asegura que las palabras más frecuentes tengan más peso.")
print("3. Este es el principio básico (aunque simplificado) de cómo funcionan los LLMs.")