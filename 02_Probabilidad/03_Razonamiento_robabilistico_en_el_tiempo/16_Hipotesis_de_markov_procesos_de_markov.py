print("=== PROCESOS DE MARKOV Y LA HIPÓTESIS DE MARKOV ===\n")

# 1. Definimos el "Espacio de Estados" del Proceso
estados = ["Dormir", "Estudiar", "Jugar"]

# 2. Distribución de Probabilidad Inicial P(X_0)
# (¿Qué probabilidad hay de que el estudiante inicie su día en cada estado?)
prob_inicial = {
    "Dormir": 0.50, 
    "Estudiar": 0.30, 
    "Jugar": 0.20
}

# 3. Matriz de Transición (El núcleo del Proceso de Markov) P(X_t+1 | X_t)
# Aquí vive la HIPÓTESIS DE MARKOV: Las probabilidades de a dónde ir después
# SOLO dependen del estado actual de la fila, sin importar de dónde veníamos antes.
transiciones = {
    # Estado Actual -> {Probabilidades del Estado Siguiente}
    "Dormir":   {"Dormir": 0.20, "Estudiar": 0.60, "Jugar": 0.20},
    "Estudiar": {"Dormir": 0.30, "Estudiar": 0.40, "Jugar": 0.30},
    "Jugar":    {"Dormir": 0.60, "Estudiar": 0.10, "Jugar": 0.30}
}

# 4. Motor de Cálculo de Probabilidad de Secuencias
def calcular_probabilidad_historia(secuencia):
    """
    Calcula la probabilidad conjunta de una historia entera ocurriendo en ese orden exacto,
    usando la regla de la cadena simplificada por la Hipótesis de Markov.
    """
    if not secuencia:
        return 0.0
        
    print(f"Calculando probabilidad para la línea de tiempo: {' -> '.join(secuencia)}\n")
    
    # El primer evento usa la probabilidad inicial
    estado_actual = secuencia[0]
    prob_acumulada = prob_inicial[estado_actual]
    print(f"P({estado_actual} en t=0) = {prob_acumulada}")
    
    # Para el resto de la historia, aplicamos la Hipótesis de Markov
    for i in range(1, len(secuencia)):
        estado_anterior = secuencia[i-1]
        estado_nuevo = secuencia[i]
        
        # P(X_t+1 | X_t)
        prob_paso = transiciones[estado_anterior][estado_nuevo]
        
        # Multiplicamos la probabilidad acumulada por este nuevo salto
        prob_acumulada *= prob_paso
        
        print(f" * P({estado_nuevo} en t={i} | {estado_anterior} en t={i-1}) = {prob_paso}")
        
    return prob_acumulada

# --- EJECUCIÓN Y ANÁLISIS ---

# Escenario: Queremos saber qué tan probable es que el estudiante haga exactamente esto:
# Despierta (Estaba durmiendo) -> Se pone a Estudiar -> Termina y se va a Jugar -> Vuelve a Dormir
historia_a_evaluar = ["Dormir", "Estudiar", "Jugar", "Dormir"]

probabilidad_final = calcular_probabilidad_historia(historia_a_evaluar)

print("\n=== RESULTADO MATEMÁTICO ===")
print(f"Probabilidad de que ocurra esta secuencia exacta: {probabilidad_final:.4f} (¡{probabilidad_final * 100:.2f}%!)")

print("\n=== LA MAGIA DE LA HIPÓTESIS DE MARKOV ===")
print("Nota cómo en el paso t=3 (ir a Dormir), la IA SOLO multiplicó la probabilidad de")
print("estar 'Jugando' en t=2 (0.60). La IA ignoró por completo que en t=1 estaba 'Estudiando'.")
print("Al asumir que el pasado no importa dado el presente, reducimos un problema de memoria")
print("infinita a simples multiplicaciones en cadena.")