import numpy as np
import random

# 1. Definición del Entorno
# Imaginemos un pasillo con 6 casillas. El inicio es 0 y la meta es 5.
n_estados = 6  
n_acciones = 2 # Acción 0: Mover a la izquierda, Acción 1: Mover a la derecha

# Inicializamos la Tabla Q con ceros
# Las filas son los estados (0 al 5) y las columnas las acciones (izq, der)
q_table = np.zeros((n_estados, n_acciones))

# 2. Hiperparámetros del Algoritmo
alpha = 0.1      # Tasa de aprendizaje (qué tanto acepta la nueva información)
gamma = 0.9      # Factor de descuento (qué tanto le importan las recompensas futuras)
epsilon = 0.2    # Probabilidad de exploración (20% de las veces tomará un paso al azar)
episodios = 100  # Número de veces que el agente intentará llegar a la meta

# 3. Lógica del Entorno (Simulador)
def tomar_accion(estado, accion):
    # Calcular el nuevo estado basado en la acción
    if accion == 1: # Derecha
        siguiente_estado = min(estado + 1, n_estados - 1)
    else:           # Izquierda
        siguiente_estado = max(estado - 1, 0)
    
    # Asignar recompensas
    if siguiente_estado == n_estados - 1:
        return siguiente_estado, 10, True # Recompensa de +10 por llegar a la meta
    else:
        return siguiente_estado, 0, False # Recompensa de 0 por cualquier otro paso

# 4. Bucle de Entrenamiento de Q-Learning
for episodio in range(episodios):
    estado = 0 # El agente siempre empieza en la casilla 0
    completado = False
    
    while not completado:
        # Estrategia Epsilon-Greedy: ¿Explorar o Explotar?
        if random.uniform(0, 1) < epsilon:
            accion = random.randint(0, n_acciones - 1) # Explorar: Acción aleatoria
        else:
            accion = np.argmax(q_table[estado]) # Explotar: Mejor acción según la Tabla Q
        
        # El agente da el paso en el entorno
        siguiente_estado, recompensa, completado = tomar_accion(estado, accion)
        
        # 5. La magia matemática: Actualización usando la Ecuación de Bellman
        valor_antiguo = q_table[estado, accion]
        max_q_siguiente = np.max(q_table[siguiente_estado])
        
        # Fórmula central de Q-Learning
        nuevo_valor = valor_antiguo + alpha * (recompensa + gamma * max_q_siguiente - valor_antiguo)
        q_table[estado, accion] = nuevo_valor
        
        # Avanzar al siguiente estado
        estado = siguiente_estado

# 6. Resultados
print("Entrenamiento finalizado. Esta es la Tabla Q aprendida:\n")
print("               [Izquierda, Derecha]")
for i, fila in enumerate(q_table):
    print(f"Estado {i}: {fila}")