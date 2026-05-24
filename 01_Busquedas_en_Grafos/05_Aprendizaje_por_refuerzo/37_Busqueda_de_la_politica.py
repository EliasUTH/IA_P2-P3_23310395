import numpy as np

# 1. Configuración del Entorno (Un mapa de 3x3)
# 0  1  2 (Meta 🏆)
# 3  4  5
# 6  7  8 (Trampa 💀)
n_estados = 9
n_acciones = 4 # 0: Arriba, 1: Abajo, 2: Izquierda, 3: Derecha

# Definir recompensas del mapa
recompensas = np.zeros(n_estados)
recompensas[2] = 10   # Llegar a la meta da +10
recompensas[8] = -10  # Caer en la trampa da -10

estados_terminales = [2, 8] # El juego termina si caes en uno de estos

# 2. Las "Reglas del Juego" (El modelo del entorno)
def predecir_transicion(estado, accion):
    # Si ya estamos en la meta o la trampa, no nos movemos
    if estado in estados_terminales:
        return estado, 0
    
    # Matemáticas para saber en qué fila y columna de la matriz 3x3 estamos
    fila = estado // 3
    columna = estado % 3
    
    if accion == 0: fila = max(0, fila - 1)        # Arriba
    elif accion == 1: fila = min(2, fila + 1)      # Abajo
    elif accion == 2: columna = max(0, columna - 1)# Izquierda
    elif accion == 3: columna = min(2, columna + 1)# Derecha
    
    nuevo_estado = fila * 3 + columna
    return nuevo_estado, recompensas[nuevo_estado]

# 3. Paso A: Encontrar el "Valor" de cada casilla (Iteración de Valor)
valores = np.zeros(n_estados)
gamma = 0.9 # Factor de descuento (importancia del futuro)

# Hacemos 100 barridos matemáticos por el mapa
for _ in range(100):
    nuevos_valores = np.copy(valores)
    for estado in range(n_estados):
        if estado in estados_terminales:
            continue
        
        # Calcular qué pasaría con cada acción posible usando Bellman
        valores_acciones = []
        for accion in range(n_acciones):
            nuevo_estado, recompensa = predecir_transicion(estado, accion)
            # Valor = Recompensa inmediata + (Gamma * Valor futuro)
            valor_calculado = recompensa + gamma * valores[nuevo_estado]
            valores_acciones.append(valor_calculado)
        
        # El valor de este estado es el máximo que podemos lograr
        nuevos_valores[estado] = max(valores_acciones)
    valores = nuevos_valores

# 4. Paso B: BÚSQUEDA / EXTRACCIÓN DE LA POLÍTICA
# Ahora que sabemos cuánto "vale" cada casilla, sacamos la política óptima
politica_visual = []
iconos_acciones = ['↑', '↓', '←', '→']

for estado in range(n_estados):
    if estado == 2:
        politica_visual.append('🏆')
    elif estado == 8:
        politica_visual.append('💀')
    else:
        valores_acciones = []
        for accion in range(n_acciones):
            nuevo_estado, recompensa = predecir_transicion(estado, accion)
            valores_acciones.append(recompensa + gamma * valores[nuevo_estado])
        
        # La Política se define eligiendo la acción que da el mayor valor
        mejor_accion = np.argmax(valores_acciones)
        politica_visual.append(iconos_acciones[mejor_accion])

# 5. Resultados
print("=== LA POLÍTICA ÓPTIMA (EL MAPA MAESTRO) ===\n")
print("Si el agente cae en cualquier casilla, la flecha le dice qué hacer:\n")
for i in range(0, 9, 3):
    print(f"  {politica_visual[i]}  |  {politica_visual[i+1]}  |  {politica_visual[i+2]}")
print("\nNota: Fíjate cómo las casillas cercanas al 💀 lo evitan activamente.")