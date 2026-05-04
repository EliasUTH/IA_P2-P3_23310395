import math

print("=== FUNCIONES DE ACTIVACIÓN PARA REDES NEURONALES ===\n")

# --- 1. FUNCIÓN SIGMOIDE (Logistic) ---
# Ideal para probabilidad en la capa de salida (entre 0 y 1).
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# --- 2. TANGENTE HIPERBÓLICA (Tanh) ---
# Centrada en cero, suele converger más rápido que la sigmoide (entre -1 y 1).
def tanh(x):
    return math.tanh(x)

# --- 3. RELU (Rectified Linear Unit) ---
# La más usada en Deep Learning por ser computacionalmente eficiente.
def relu(x):
    return max(0, x)

# --- 4. LEAKY RELU ---
# Soluciona el problema de las "neuronas muertas" dejando pasar una pequeña señal negativa.
def leaky_relu(x, alpha=0.01):
    return x if x > 0 else alpha * x

# --- 5. SOFTMAX (Simplificada para 1D) ---
# Convierte un vector de números en probabilidades que suman 1.0.
def softmax(vector):
    exps = [math.exp(v) for v in vector]
    suma_exps = sum(exps)
    return [e / suma_exps for e in exps]

# --- PRUEBA DE FUNCIONAMIENTO ---

valores_test = [-2.0, -0.5, 0.0, 0.5, 2.0]

print(f"{'Valor x':<10} | {'Sigmoid':<10} | {'Tanh':<10} | {'ReLU':<10}")
print("-" * 45)

for x in valores_test:
    s = sigmoid(x)
    t = tanh(x)
    r = relu(x)
    print(f"{x:<10.1f} | {s:<10.4f} | {t:<10.4f} | {r:<10.4f}")

# Ejemplo de Softmax (Clasificación Multiclase)
puntuaciones = [2.0, 1.0, 0.1]
probabilidades = softmax(puntuaciones)
print(f"\nSoftmax de {puntuaciones}:")
print(f"Probabilidades: {[round(p, 4) for p in probabilidades]} (Suma: {sum(probabilidades)})")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. ReLU es la opción por defecto para capas ocultas.")
print("2. Sigmoid y Softmax se reservan usualmente para la capa de salida.")
print("3. Tanh es útil cuando los datos de entrada tienen valores negativos.")