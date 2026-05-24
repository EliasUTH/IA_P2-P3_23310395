import random

print("=== COMPUTACIÓN NEURONAL: EL PERCEPTRÓN ===\n")

class Perceptron:
    def __init__(self, n_entradas, tasa_aprendizaje=0.1):
        # Inicializamos los pesos y el sesgo (bias) aleatoriamente
        self.pesos = [random.uniform(-1, 1) for _ in range(n_entradas)]
        self.sesgo = random.uniform(-1, 1)
        self.tasa_aprendizaje = tasa_aprendizaje

    def activar(self, suma):
        """Función de activación escalón (Heaviside)"""
        return 1 if suma >= 0 else 0

    def predecir(self, entradas):
        # Computación neuronal: Suma ponderada + Sesgo
        suma = sum(x * w for x, w in zip(entradas, self.pesos)) + self.sesgo
        return self.activar(suma)

    def entrenar(self, datos_entrenamiento, etiquetas, epocas=100):
        for _ in range(epocas):
            for entradas, etiqueta_real in zip(datos_entrenamiento, etiquetas):
                prediccion = self.predecir(entradas)
                error = etiqueta_real - prediccion
                
                # Regla de aprendizaje del perceptrón (Delta Rule)
                if error != 0:
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self.tasa_aprendizaje * error * entradas[i]
                    self.sesgo += self.tasa_aprendizaje * error

# --- PRUEBA: APRENDER LA FUNCIÓN LÓGICA 'AND' ---
# Solo da 1 si AMBAS entradas son 1
entradas_and = [[0, 0], [0, 1], [1, 0], [1, 1]]
salidas_and = [0, 0, 0, 1]

# Crear y entrenar la neurona
neurona = Perceptron(n_entradas=2)
print("Entrenando la unidad neuronal...")
neurona.entrenar(entradas_and, salidas_and)

print("\n--- RESULTADOS DE LA COMPUTACIÓN ---")
for x in entradas_and:
    resultado = neurona.predecir(x)
    print(f"Entrada: {x} -> Salida Neuronal: {resultado}")

print("\n=== ANÁLISIS DEL MODELO ===")
print("Esta neurona artificial imita a una biológica: suma impulsos eléctricos")
print("(entradas * pesos) y si superan un umbral, 'dispara' una señal (1).")