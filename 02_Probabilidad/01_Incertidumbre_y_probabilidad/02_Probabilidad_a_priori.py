# Cálculo de Probabilidad A Priori (Prior Probability)
# En IA, esto es la base para enseñar a un modelo a partir de datos históricos.

def calcular_probabilidades_priori(dataset):
    """
    Toma un conjunto de datos históricos y calcula la probabilidad a priori de cada clase.
    """
    total_observaciones = len(dataset)
    conteo_clases = {}
    
    # 1. Contar la frecuencia absoluta de cada evento
    for evento in dataset:
        if evento in conteo_clases:
            conteo_clases[evento] += 1
        else:
            conteo_clases[evento] = 1
            
    # 2. Calcular la probabilidad a priori (frecuencia relativa)
    probabilidades_priori = {}
    for evento, conteo in conteo_clases.items():
        # P(A) = Casos favorables / Casos totales
        probabilidades_priori[evento] = conteo / total_observaciones
        
    return conteo_clases, probabilidades_priori


# --- Escenario del Mundo Real ---
print("=== IA METEOROLÓGICA: PROBABILIDAD A PRIORI ===\n")

# Imaginemos que la IA tiene una base de datos con el clima de los últimos 20 días en una ciudad
historial_clima = [
    "Soleado", "Lluvia", "Nublado", "Soleado", "Soleado",
    "Lluvia", "Lluvia", "Soleado", "Nublado", "Soleado",
    "Soleado", "Nublado", "Lluvia", "Soleado", "Soleado",
    "Tormenta", "Soleado", "Nublado", "Soleado", "Lluvia"
]

print(f"Total de datos históricos procesados: {len(historial_clima)} días.\n")

# La IA procesa los datos
frecuencias, priors = calcular_probabilidades_priori(historial_clima)

print("1. Frecuencias Históricas (Lo que la IA contó):")
for clima, conteo in frecuencias.items():
    print(f"   - {clima}: {conteo} días")

print("\n2. Probabilidades A Priori calculadas P(Estado):")
for clima, prob in priors.items():
    print(f"   - P({clima}) = {prob:.2f} ({prob * 100:.1f}%)")

# La IA toma una decisión puramente basada en la historia
clima_mas_probable = max(priors, key=priors.get)

print("\n=== CONCLUSIÓN DE LA IA ===")
print("Si me encierras en un cuarto sin ventanas y me preguntas qué clima hace hoy,")
print(f"mi respuesta inicial (A PRIORI) será: '{clima_mas_probable}'.")
print(f"Razón: Históricamente tiene un {priors[clima_mas_probable] * 100}% de probabilidad de ocurrir,")
print("antes de que yo pueda revisar sensores o ver nubes en el cielo (nueva evidencia).")