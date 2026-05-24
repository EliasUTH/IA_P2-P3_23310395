import math

print("=== CLASIFICADOR NAIVE BAYES (Filtro de Spam) ===\n")

# --- 1. DATOS DE ENTRENAMIENTO ---
# Un pequeño conjunto de datos para "enseñar" a nuestra IA
entrenamiento = [
    ("oferta dinero gratis ahora", "Spam"),
    ("ganaste un premio clic aquí", "Spam"),
    ("reunión de trabajo mañana", "Ham"),
    ("pago de factura pendiente", "Ham"),
    ("gratis hoy oferta exclusiva", "Spam"),
    ("confirmación de cita médica", "Ham")
]

# --- 2. EL ALGORITMO ---

class ClasificadorNaiveBayes:
    def __init__(self):
        self.vocabulario = set()
        self.conteo_palabras = {"Spam": {}, "Ham": {}}
        self.total_mensajes = {"Spam": 0, "Ham": 0}

    def entrenar(self, datos):
        for texto, categoria in datos:
            self.total_mensajes[categoria] += 1
            palabras = texto.lower().split()
            for p in palabras:
                self.vocabulario.add(p)
                self.conteo_palabras[categoria][p] = self.conteo_palabras[categoria].get(p, 0) + 1

    def calcular_probabilidad(self, texto, categoria):
        """Aplica el Teorema de Bayes: P(C|D) proporcional a P(C) * producto de P(palabra|C)"""
        prob_categoria = self.total_mensajes[categoria] / sum(self.total_mensajes.values())
        
        # Usamos logaritmos para evitar que el número se vuelva 0 (Underflow)
        log_prob = math.log(prob_categoria)
        
        palabras = texto.lower().split()
        for p in palabras:
            # Suavizado de Laplace (+1) para evitar multiplicar por cero si la palabra es nueva
            veces_palabra = self.conteo_palabras[categoria].get(p, 0) + 1
            total_palabras_cat = sum(self.conteo_palabras[categoria].values()) + len(self.vocabulario)
            log_prob += math.log(veces_palabra / total_palabras_cat)
            
        return log_prob

    def clasificar(self, texto):
        prob_spam = self.calcular_probabilidad(texto, "Spam")
        prob_ham = self.calcular_probabilidad(texto, "Ham")
        
        return "Spam" if prob_spam > prob_ham else "Ham"

# --- 3. PRUEBA DEL MODELO ---

ia = ClasificadorNaiveBayes()
ia.entrenar(entrenamiento)

# Probemos con mensajes nuevos que la IA nunca ha visto
mensajes_prueba = [
    "oferta gratis de dinero",
    "mañana tenemos reunión",
    "clic para ganar premio ahora"
]

print(f"{'Mensaje':<35} | {'Clasificación IA'}")
print("-" * 55)

for m in mensajes_prueba:
    resultado = ia.clasificar(m)
    print(f"{m:<35} | {resultado}")

print("\n=== ANÁLISIS DEL EXPERTO ===")
print("La IA aprendió que palabras como 'gratis' y 'oferta' aparecen más en Spam.")
print("Aunque el mensaje 'oferta gratis de dinero' es nuevo, Naive Bayes suma las")
print("probabilidades individuales de cada palabra para tomar una decisión final.")