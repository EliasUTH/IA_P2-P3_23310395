import math
import random

print("=== RED NEURONAL PROFUNDA (DEEP LEARNING) ===\n")

# --- 1. FUNCIONES DE ACTIVACIÓN ---
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivada(x):
    # Derivada de la función sigmoide para el ajuste de pesos
    s = sigmoid(x)
    return s * (1 - s)

# --- 2. ARQUITECTURA DE LA RED ---
class RedNeuronalProfunda:
    def __init__(self, n_entrada, n_oculto, n_salida):
        # Inicialización de pesos con valores aleatorios pequeños
        self.pesos_h = [[random.uniform(-1, 1) for _ in range(n_oculto)] for _ in range(n_entrada)]
        self.pesos_o = [[random.uniform(-1, 1) for _ in range(n_salida)] for _ in range(n_oculto)]
        self.tasa_aprendizaje = 0.5

    def entrenar(self, entradas, objetivos, epocas=10000):
        for epoca in range(epocas):
            for i in range(len(entradas)):
                # --- FORWARD PASS (Propagación hacia adelante) ---
                capa_entrada = entradas[i]
                
                # Cálculo capa oculta
                suma_oculta = [sum(capa_entrada[j] * self.pesos_h[j][k] for j in range(len(capa_entrada))) for k in range(len(self.pesos_h[0]))]
                activacion_oculta = [sigmoid(s) for s in suma_oculta]
                
                # Cálculo capa salida
                suma_salida = [sum(activacion_oculta[j] * self.pesos_o[j][k] for j in range(len(activacion_oculta))) for k in range(len(self.pesos_o[0]))]
                salida_final = [sigmoid(s) for s in suma_salida]
                
                # --- BACKPROPAGATION (Ajuste de errores) ---
                # Error en salida
                errores_o = [objetivos[i][j] - salida_final[j] for j in range(len(salida_final))]
                gradientes_o = [errores_o[j] * sigmoid_derivada(suma_salida[j]) for j in range(len(errores_o))]
                
                # Error en capa oculta (atribuir culpa a los pesos anteriores)
                errores_h = [sum(gradientes_o[k] * self.pesos_o[j][k] for k in range(len(gradientes_o))) for j in range(len(activacion_oculta))]
                gradientes_h = [errores_h[j] * sigmoid_derivada(suma_oculta[j]) for j in range(len(errores_h))]
                
                # Actualizar pesos Salida -> Oculta
                for j in range(len(activacion_oculta)):
                    for k in range(len(gradientes_o)):
                        self.pesos_o[j][k] += self.tasa_aprendizaje * gradientes_o[k] * activacion_oculta[j]
                
                # Actualizar pesos Oculta -> Entrada
                for j in range(len(capa_entrada)):
                    for k in range(len(gradientes_h)):
                        self.pesos_h[j][k] += self.tasa_aprendizaje * gradientes_h[k] * capa_entrada[j]

    def predecir(self, entrada):
        # Solo la parte Forward del proceso
        act_h = [sigmoid(sum(entrada[j] * self.pesos_h[j][k] for j in range(len(entrada)))) for k in range(len(self.pesos_h[0]))]
        return [sigmoid(sum(act_h[j] * self.pesos_o[j][k] for j in range(len(act_h)))) for k in range(len(self.pesos_o[0]))]

# --- 3. PRUEBA: APRENDER LA COMPUERTA XOR (No linealmente separable) ---
# Un problema que una sola neurona no puede resolver, pero una red profunda sí.
datos_x = [[0,0], [0,1], [1,0], [1,1]]
datos_y = [[0], [1], [1], [0]]

red = RedNeuronalProfunda(n_entrada=2, n_oculto=3, n_salida=1)
print("Entrenando red neuronal... (Esto puede tardar unos segundos)")
red.entrenar(datos_x, datos_y)

print("\n--- RESULTADOS DE PREDICCIÓN ---")
for x in datos_x:
    pred = red.predecir(x)
    print(f"Entrada: {x} -> Predicción: {pred[0]:.4f} (Objetivo: {datos_y[datos_x.index(x)][0]})")