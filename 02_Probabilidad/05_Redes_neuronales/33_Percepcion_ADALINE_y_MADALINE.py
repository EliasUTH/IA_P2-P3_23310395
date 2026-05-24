import random

print("=== REDES NEURONALES: ADALINE Y MADALINE ===\n")

# --- 1. MODELO ADALINE ---
class Adaline:
    def __init__(self, n_entradas, tasa_aprendizaje=0.01):
        self.pesos = [random.uniform(-0.5, 0.5) for _ in range(n_entradas)]
        self.sesgo = random.uniform(-0.5, 0.5)
        self.tasa_aprendizaje = tasa_aprendizaje

    def activacion_lineal(self, entradas):
        # En ADALINE el aprendizaje se basa en este valor continuo
        return sum(x * w for x, w in zip(entradas, self.pesos)) + self.sesgo

    def cuantizador(self, valor):
        # Función escalón para la salida final
        return 1 if valor >= 0 else -1

    def entrenar(self, entradas, objetivo):
        # Salida analógica antes de clasificar
        salida_neta = self.activacion_lineal(entradas)
        error = objetivo - salida_neta
        
        # Regla de Aprendizaje Delta (LMS - Least Mean Squares)
        for i in range(len(self.pesos)):
            self.pesos[i] += self.tasa_aprendizaje * error * entradas[i]
        self.sesgo += self.tasa_aprendizaje * error
        return error**2 # Retornamos el error cuadrático

# --- 2. MODELO MADALINE (Simplificado: Regla MRI) ---
class Madaline:
    def __init__(self, n_adalines, n_entradas):
        self.capa_oculta = [Adaline(n_entradas) for _ in range(n_adalines)]
        # La salida de MADALINE suele ser una función lógica (ej. MAYORÍA)

    def predecir(self, entradas):
        # Cada ADALINE procesa la entrada
        resultados = [ada.cuantizador(ada.activacion_lineal(entradas)) for ada in self.capa_oculta]
        # Salida por votación (Regla de la Mayoría)
        return 1 if sum(resultados) >= 0 else -1

# --- PRUEBA DE ADALINE ---
# Vamos a aprender una relación lineal simple
datos = [[1, 2], [2, 1], [-1, -2], [-2, -1]]
objetivos = [1, 1, -1, -1] # Clase 1 o Clase -1

modelo_ada = Adaline(n_entradas=2)
print("Entrenando ADALINE...")
for epoca in range(500):
    error_total = sum(modelo_ada.entrenar(x, y) for x, y in zip(datos, objetivos))

# Resultados
print("\n--- RESULTADOS ADALINE ---")
for x in datos:
    pred = modelo_ada.cuantizador(modelo_ada.activacion_lineal(x))
    print(f"Entrada: {x} -> Predicción: {pred}")

print("\n=== ANÁLISIS TÉCNICO ===")
print("1. ADALINE usa el Error Cuadrático Medio, lo que lo hace más estable.")
print("2. MADALINE combina varios ADALINEs para resolver problemas no lineales.")
print("3. Estas redes fueron el puente entre la neurona simple y el Deep Learning actual.")