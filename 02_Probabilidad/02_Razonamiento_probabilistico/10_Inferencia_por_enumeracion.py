print("=== MOTOR DE INFERENCIA POR ENUMERACIÓN ===\n")

# 1. Base de Conocimiento de la Red Bayesiana (El mismo problema de la Alarma)
P_Robo = {True: 0.001, False: 0.999}
P_Terremoto = {True: 0.002, False: 0.998}

# P(Alarma | Robo, Terremoto)
P_Alarma = {
    (True, True): 0.95,
    (True, False): 0.94,
    (False, True): 0.29,
    (False, False): 0.001
}

# P(Llamada | Alarma)
P_Juan = {True: 0.90, False: 0.05}
P_Maria = {True: 0.70, False: 0.01}

# Lista de variables en orden topológico (causas primero, efectos después)
variables_red = ['Robo', 'Terremoto', 'Alarma', 'Juan', 'Maria']

# 2. Función que extrae la probabilidad condicional de un nodo
def probabilidad_nodo(variable, valor, estado_actual):
    if variable == 'Robo': return P_Robo[valor]
    if variable == 'Terremoto': return P_Terremoto[valor]
    if variable == 'Alarma': 
        prob = P_Alarma[(estado_actual['Robo'], estado_actual['Terremoto'])]
        return prob if valor else (1 - prob)
    if variable == 'Juan': 
        return P_Juan[estado_actual['Alarma']] if valor else (1 - P_Juan[estado_actual['Alarma']])
    if variable == 'Maria': 
        return P_Maria[estado_actual['Alarma']] if valor else (1 - P_Maria[estado_actual['Alarma']])

# 3. El núcleo del algoritmo: La Inferencia Recursiva
def enumerate_all(variables, evidencia):
    # Si ya no hay variables por evaluar, la probabilidad del final de esta rama es 1.0
    if not variables:
        return 1.0
    
    Y = variables[0]
    resto_variables = variables[1:]
    
    # Si la variable 'Y' ya es parte de nuestra evidencia (ej. sabemos que Juan llamó)
    if Y in evidencia:
        valor_Y = evidencia[Y]
        return probabilidad_nodo(Y, valor_Y, evidencia) * enumerate_all(resto_variables, evidencia)
    
    # Si 'Y' es una VARIABLE OCULTA (no sabemos qué pasó)
    else:
        suma_probabilidades = 0
        # "Enumeramos" sumando los dos mundos posibles: donde Y fue True y donde Y fue False
        for valor_Y in [True, False]:
            evidencia_extendida = evidencia.copy()
            evidencia_extendida[Y] = valor_Y
            # Regla de la cadena sumada
            suma_probabilidades += probabilidad_nodo(Y, valor_Y, evidencia_extendida) * enumerate_all(resto_variables, evidencia_extendida)
        return suma_probabilidades

# 4. Función Principal de Consulta
def inferencia_enumeracion(consulta, evidencia, variables):
    """
    Calcula P(Consulta | Evidencia)
    """
    distribucion_Q = {}
    
    # Evaluamos tanto para Consulta = True como para Consulta = False
    for valor_consulta in [True, False]:
        evidencia_extendida = evidencia.copy()
        evidencia_extendida[consulta] = valor_consulta
        distribucion_Q[valor_consulta] = enumerate_all(variables, evidencia_extendida)
        
    # NORMALIZACIÓN (Alpha): Asegurar que las probabilidades sumen 100% (1.0)
    suma_total = sum(distribucion_Q.values())
    for valor in distribucion_Q:
        distribucion_Q[valor] = distribucion_Q[valor] / suma_total
        
    return distribucion_Q

# --- PRUEBA DEL MOTOR DE INFERENCIA ---

print("ESCENARIO: Llegas a tu trabajo y ves en tu celular que tus dos vecinos")
print("(Juan y María) te acaban de llamar por teléfono (Esta es nuestra EVIDENCIA).\n")
print("No sabes si sonó la alarma, ni si tembló, ni si te robaron (Variables Ocultas).\n")

# Evidencia: Lo que sabemos que ocurrió con certeza
evidencia_actual = {'Juan': True, 'Maria': True}

# Consulta: Lo que le preguntamos a la IA
variable_consulta = 'Robo'

print(f"-> IA, procesando consulta: ¿Cuál es la probabilidad de que haya un {variable_consulta}?")
print("-> Calculando todos los universos posibles (Enumerando)...\n")

resultado = inferencia_enumeracion(variable_consulta, evidencia_actual, variables_red)

print("=== RESULTADO DE LA INFERENCIA ===")
print(f"Probabilidad de que SÍ haya un Robo: {resultado[True] * 100:.2f}%")
print(f"Probabilidad de que NO haya un Robo: {resultado[False] * 100:.2f}%")


if resultado[True] > 0.20:
    print("\nConclusión: ¡Un 28.4% es una probabilidad de robo gigante!")
    print("(Recuerda que la probabilidad normal de un robo cualquier día era de apenas 0.1%).")
    print("La IA recomienda llamar a la policía inmediatamente.")