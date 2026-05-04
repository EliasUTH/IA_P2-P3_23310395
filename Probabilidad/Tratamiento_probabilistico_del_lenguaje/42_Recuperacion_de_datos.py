import math

print("=== SISTEMA DE RECUPERACIÓN DE INFORMACIÓN (IR) ===\n")

# --- 1. NUESTRA BASE DE DATOS (CORPUS) ---
documentos = [
    "El aprendizaje profundo es una rama de la inteligencia artificial",
    "Las redes neuronales imitan el funcionamiento del cerebro humano",
    "El algoritmo de Bayes se basa en la probabilidad condicional",
    "La inteligencia artificial y el aprendizaje automático son el futuro",
    "La recuperación de información utiliza vectores para buscar texto"
]

# --- 2. PROCESAMIENTO DE TEXTO ---
def tokenizar(texto):
    """Limpia y divide el texto en palabras individuales."""
    return texto.lower().replace(",", "").split()

def calcular_tf(termino, documento_tokenizado):
    """Frecuencia del Término: Qué tanto aparece la palabra en este documento."""
    if not documento_tokenizado: return 0
    return documento_tokenizado.count(termino) / len(documento_tokenizado)

def calcular_idf(termino, todos_documentos):
    """Frecuencia Inversa de Documento: Qué tan rara/valiosa es la palabra en el corpus."""
    n_documentos_con_termino = sum(1 for doc in todos_documentos if termino in tokenizar(doc))
    if n_documentos_con_termino == 0: return 0
    return math.log(len(todos_documentos) / n_documentos_con_termino)

# --- 3. MOTOR DE BÚSQUEDA ---
def buscar(consulta, corpus):
    tokens_consulta = tokenizar(consulta)
    puntuaciones = []

    for i, doc in enumerate(corpus):
        tokens_doc = tokenizar(doc)
        score_tfidf = 0
        
        for palabra in tokens_consulta:
            tf = calcular_tf(palabra, tokens_doc)
            idf = calcular_idf(palabra, corpus)
            score_tfidf += tf * idf
        
        puntuaciones.append((i, score_tfidf))

    # Ordenar por relevancia (mayor puntuación primero)
    return sorted(puntuaciones, key=lambda x: x[1], reverse=True)

# --- 4. PRUEBA DEL SISTEMA ---
query = "inteligencia artificial y aprendizaje"
resultados = buscar(query, documentos)

print(f"Consulta: '{query}'")
print("-" * 60)
print(f"{'Relevancia':<12} | {'Documento Encontrado'}")
print("-" * 60)

for idx, score in resultados:
    if score > 0:
        print(f"{score:<12.4f} | {documentos[idx]}")

if resultados[0][1] == 0:
    print("No se encontraron documentos relevantes.")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. TF-IDF: Identifica que 'inteligencia' es más importante que 'el' o 'y'.")
print("2. Espacio Vectorial: Cada documento se trata como un punto en un mapa de palabras.")
print("3. Ranking: El sistema ordena los resultados para que el usuario vea lo mejor primero.")