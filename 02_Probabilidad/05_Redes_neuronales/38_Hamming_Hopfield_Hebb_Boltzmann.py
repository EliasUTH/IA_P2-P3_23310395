# 39_Aprendizaje_Hebb.py
print("=== APRENDIZAJE HEBBIANO ===")

class Hebb:
    def __init__(self, n_entradas):
        self.pesos = [0.0] * n_entradas

    def entrenar(self, patrones):
        for p in patrones:
            for i in range(len(self.pesos)):
                # Regla de Hebb: w = w + x_i * y
                # (Aquí asumimos que la salida deseada es el mismo patrón para autoasociación)
                self.pesos[i] += p[i] * 1 # Simplificado

patron = [1, -1, 1]
modelo = Hebb(3)
modelo.entrenar([patron])
print(f"Pesos aprendidos: {modelo.pesos}")