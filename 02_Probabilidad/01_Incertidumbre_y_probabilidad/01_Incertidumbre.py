# Sistema Experto Probabilístico simple usando el Teorema de Bayes
# Manejo de la Incertidumbre en diagnósticos médicos

def calcular_probabilidad_bayesiana(prior, sensibilidad, especificidad):
    """
    Calcula la probabilidad real de tener la enfermedad dado un resultado positivo.
    
    :param prior: Probabilidad inicial de tener la enfermedad en la población general.
    :param sensibilidad: Probabilidad de que la prueba dé POSITIVO si estás ENFERMO (Tasa de Verdaderos Positivos).
    :param especificidad: Probabilidad de que la prueba dé NEGATIVO si estás SANO (Tasa de Verdaderos Negativos).
    :return: Probabilidad posterior (Incertidumbre resuelta).
    """
    # 1. Probabilidad de que la prueba dé positivo estando SANO (Falso Positivo)
    # Si la prueba tiene 90% de especificidad, hay un 10% de error.
    prob_falso_positivo = 1.0 - especificidad
    
    # 2. Probabilidad de NO tener la enfermedad en la población general
    prob_sano = 1.0 - prior
    
    # 3. Teorema de Probabilidad Total: Probabilidad absoluta de que la prueba dé Positivo
    # (Enfermos que dan positivo) + (Sanos que dan positivo por error)
    prob_positivo_absoluto = (sensibilidad * prior) + (prob_falso_positivo * prob_sano)
    
    # 4. Teorema de Bayes: Actualizamos nuestra creencia (Posterior)
    # P(Enfermedad | Positivo) = P(Positivo | Enfermedad) * P(Enfermedad) / P(Positivo Absoluto)
    prob_posterior = (sensibilidad * prior) / prob_positivo_absoluto
    
    return prob_posterior

# --- Escenario del Mundo Real ---

print("=== IA MEDICA: MANEJO DE INCERTIDUMBRE ===\n")

# Datos estadísticos (El "conocimiento" de la IA)
enfermedad_rara_prob = 0.01  # Solo el 1% de la población la tiene (Prior)
eficacia_prueba_enfermo = 0.95  # Si estás enfermo, la prueba acierta el 95% de las veces (Sensibilidad)
eficacia_prueba_sano = 0.90     # Si estás sano, la prueba acierta el 90% de las veces dando negativo (Especificidad)

print(f"Población enferma (Prior): {enfermedad_rara_prob * 100}%")
print(f"Eficacia de la prueba (Sensibilidad): {eficacia_prueba_enfermo * 100}%")
print(f"Eficacia de la prueba (Especificidad): {eficacia_prueba_sano * 100}%\n")

print("-> Un paciente llega, se hace la prueba y da POSITIVO.")
print("-> Instinto humano: 'La prueba tiene 95% de eficacia, ¡seguro estoy enfermo!'\n")

# La IA calcula la verdadera probabilidad manejando la incertidumbre
probabilidad_real = calcular_probabilidad_bayesiana(
    prior = enfermedad_rara_prob, 
    sensibilidad = eficacia_prueba_enfermo, 
    especificidad = eficacia_prueba_sano
)

print("=== VEREDICTO DE LA INTELIGENCIA ARTIFICIAL ===")
print(f"Probabilidad real de que el paciente esté enfermo: {round(probabilidad_real * 100, 2)}%\n")

if probabilidad_real < 0.5:
    print("Conclusión de la IA: A pesar del resultado positivo, es MUY IMPROBABLE que tenga la enfermedad.")
    print("Razón: La enfermedad es tan rara que los 'Falsos Positivos' superan a los enfermos reales.")
else:
    print("Conclusión de la IA: Hay alta probabilidad de enfermedad, iniciar tratamiento.")