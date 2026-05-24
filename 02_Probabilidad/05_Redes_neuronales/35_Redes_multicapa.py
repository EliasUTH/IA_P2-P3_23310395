import math
import random

print("=== RED NEURONAL MULTICAPA (MLP) ===\n")

# --- 1. BLOQUES MATEMÁTICOS ---
def sigmoide(x):
    return 1 / (1 + math.exp(-x))

def sigmoide_derivada(x):
    # Derivada necesaria para el ajuste de pesos (Backpropagation)
    return x * (1 - x)

# --- 2. CLASE DE LA RED ---
class MLP:
    def __init__(self, n_entrada, n_ocultas, n_salida):
        # Inicializamos pesos de forma aleatoria entre -1 y 1
        # Pesos entre entrada y capa oculta
        self.pesos_entrada_oculta = [[random.uniform(-1, 1) for _ in range(n_ocultas)] for _ in range(n_entrada)]
        # Pesos entre capa oculta y salida
        self.pesos_oculta_salida = [[random.uniform(-1, 1) for _ in range(n_salida)] for _ in range(n_ocultas)]
        
        self.tasa_aprendizaje = 0.5

    def pensar(self, entradas):
        """Propagación hacia adelante (Forward Pass)"""
        # Calcular señales en capa oculta
        self.activacion_oculta = [sigmoide(sum(entradas[i] * self.pesos_entrada_oculta[i][j] for i in range(len(entradas)))) 
                                  for j in range(len(self.pesos_entrada_oculta[0]))]
        
        # Calcular señales en capa de salida
        self.salida_final = [sigmoide(sum(self.activacion_oculta[i] * self.pesos_oculta_salida[i][j] for i in range(len(self.activacion_oculta)))) 
                             for j in range(len(self.pesos_oculta_salida[0]))]
        
        return self.salida_final

    def entrenar(self, entradas, objetivos, epocas=20000):
        """Ajuste de pesos mediante Retropropagación (Backpropagation)"""
        for epoca in range(epocas):
            for e, o in zip(entradas, objetivos):
                # 1. Forward Pass
                prediccion = self.pensar(e)
                
                # 2. Calcular error en salida
                errores_salida = [o[i] - prediccion[i] for i in range(len(o))]
                delta_salida = [errores_salida[i] * sigmoide_derivada(prediccion[i]) for i in range(len(errores_salida))]
                
                # 3. Calcular error en capa oculta (propagando el delta hacia atrás)
                errores_ocultos = [sum(delta_salida[k] * self.pesos_oculta_salida[j][k] for k in range(len(delta_salida))) 
                                   for j in range(len(self.activacion_oculta))]
                delta_oculto = [errores_ocultos[j] * sigmoide_derivada(self.activacion_oculta[j]) for j in range(len(errores_ocultos))]
                
                # 4. Actualizar pesos Oculta -> Salida
                for j in range(len(self.activacion_oculta)):
                    for k in range(len(delta_salida)):
                        self.pesos_oculta_salida[j][k] += self.tasa_aprendizaje * delta_salida[k] * self.activacion_oculta[j]
                
                # 5. Actualizar pesos Entrada -> Oculta
                for j in range(len(e)):
                    for k in range(len(delta_oculto)):
                        self.pesos_entrada_oculta[j][k] += self.tasa_aprendizaje * delta_oculto[k] * e[j]

# --- 3. PRUEBA: EL PROBLEMA XOR ---
# (0,0)->0, (0,1)->1, (1,0)->1, (1,1)->0
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [[0], [1], [1], [0]]

red = MLP(n_entrada=2, n_ocultas=3, n_salida=1)

print("Entrenando Red Multicapa para resolver XOR...")
red.entrenar(X, y)

print("\n--- RESULTADOS FINALES ---")
for entrada in X:
    resultado = red.pensar(entrada)
    print(f"Entrada: {entrada} -> Predicción: {resultado[0]:.4f}")

print("\n=== ANÁLISIS DE LA RED ===")
print("1. El MLP ha logrado lo que el Perceptrón simple no podía: resolver XOR.")
print("2. Las neuronas ocultas han aprendido a detectar combinaciones de características.")
print("3. Backpropagation permitió que la red supiera exactamente cuánto cambiar cada peso.")