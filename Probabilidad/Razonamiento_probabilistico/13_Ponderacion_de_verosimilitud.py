import random

print("=== INFERENCIA AVANZADA: PONDERACIÓN DE VEROSIMILITUD ===\n")

# 1. Definimos las probabilidades de la Red Bayesiana
# Nublado -> Lluvia
# Nublado -> Aspersor
# Lluvia, Aspersor -> Pasto_Mojado

def prob_nublado(): 
    return 0.50

def prob_lluvia(nublado): 
    return 0.80 if nublado else 0.20

def prob_aspersor(nublado): 
    return 0.10 if nublado else 0.50

def prob_pasto_mojado(lluvia, aspersor):
    if lluvia and aspersor: return 0.99
    elif lluvia and not aspersor: return 0.90
    elif not lluvia and aspersor: return 0.90
    else: return 0.01 # Casi nunca se moja si no llueve y no hay aspersor

# 2. Motor de Simulación Ponderada
def generar_muestra_ponderada(evidencia):
    """
    Genera un universo donde la EVIDENCIA ES FORZADA a ocurrir.
    A cambio, calcula un 'Peso' para indicar qué tan realista fue este universo.
    """
    muestra = {}
    peso = 1.0  # Todos los universos inician con un peso del 100% (1.0)
    
    # Nodo 1: Nublado
    if 'Nublado' in evidencia:
        muestra['Nublado'] = evidencia['Nublado'] # Forzamos el valor
        prob = prob_nublado()
        # Multiplicamos el peso por la probabilidad de que esto hubiera pasado naturalmente
        peso *= prob if muestra['Nublado'] else (1 - prob)
    else:
        # Si no es evidencia, tiramos los dados normalmente
        muestra['Nublado'] = random.random() < prob_nublado()

    # Nodo 2: Lluvia
    if 'Lluvia' in evidencia:
        muestra['Lluvia'] = evidencia['Lluvia']
        prob = prob_lluvia(muestra['Nublado'])
        peso *= prob if muestra['Lluvia'] else (1 - prob)
    else:
        muestra['Lluvia'] = random.random() < prob_lluvia(muestra['Nublado'])

    # Nodo 3: Aspersor
    if 'Aspersor' in evidencia:
        muestra['Aspersor'] = evidencia['Aspersor']
        prob = prob_aspersor(muestra['Nublado'])
        peso *= prob if muestra['Aspersor'] else (1 - prob)
    else:
        muestra['Aspersor'] = random.random() < prob_aspersor(muestra['Nublado'])

    # Nodo 4: Pasto Mojado
    if 'Pasto_Mojado' in evidencia:
        muestra['Pasto_Mojado'] = evidencia['Pasto_Mojado']
        prob = prob_pasto_mojado(muestra['Lluvia'], muestra['Aspersor'])
        peso *= prob if muestra['Pasto_Mojado'] else (1 - prob)
    else:
        muestra['Pasto_Mojado'] = random.random() < prob_pasto_mojado(muestra['Lluvia'], muestra['Aspersor'])

    return muestra, peso

# 3. Algoritmo principal de consulta
def ponderacion_verosimilitud(consulta, evidencia, num_simulaciones):
    suma_pesos_totales = 0.0
    suma_pesos_consulta_cumplida = 0.0
    
    for _ in range(num_simulaciones):
        muestra, peso_universo = generar_muestra_ponderada(evidencia)
        
        # Como NINGÚN universo se tira a la basura, sumamos el peso de todos
        suma_pesos_totales += peso_universo
        
        # Si la consulta se cumplió en este universo, sumamos su peso a la balanza del "Sí"
        if muestra[consulta[0]] == consulta[1]:
            suma_pesos_consulta_cumplida += peso_universo
            
    # Probabilidad final = (Suma de pesos donde la consulta es verdad) / (Suma de todos los pesos)
    return suma_pesos_consulta_cumplida / suma_pesos_totales

# --- SIMULACIÓN DE LA IA ---

# Evidencia: El pasto está mojado, pero vemos que el aspersor está APAGADO
evidencia_ia = {'Pasto_Mojado': True, 'Aspersor': False}

# Consulta: ¿Cuál es la probabilidad de que haya Llovido?
consulta_ia = ('Lluvia', True)
simulaciones = 10000

print("ESCENARIO: Sales de tu casa, ves el Pasto Mojado y el Aspersor apagado.")
print("La IA está calculando la probabilidad de que haya Llovido.\n")

print(f"Ejecutando {simulaciones} simulaciones PONDERADAS (Ninguna se rechaza)...")

probabilidad_final = ponderacion_verosimilitud(consulta_ia, evidencia_ia, simulaciones)

print("\n=== VEREDICTO DE LA INTELIGENCIA ARTIFICIAL ===")
print(f"-> P(Lluvia | Pasto_Mojado=V, Aspersor=F) = {probabilidad_final * 100:.2f}%\n")

print("Conclusión de la IA:")
print("- A diferencia del Muestreo por Rechazo, esta vez NO SE DESPERDICIÓ RAM.")
print("- La IA 'obligó' a todas sus simulaciones a tener el pasto mojado y aspersor apagado.")
print("- Al pesar los resultados, descubrió que la única explicación lógica para que")
print("- el pasto esté mojado sin el aspersor, es que la probabilidad de lluvia sea altísima.")