import random

print("=== MODELO OCULTO DE MARKOV (HMM) - CLASE INTEGRADA ===\n")

class HMM:
    def __init__(self, estados, observaciones, prob_inicial, transiciones, emisiones):
        self.estados = estados
        self.observaciones = observaciones
        self.prob_inicial = prob_inicial
        self.transiciones = transiciones
        self.emisiones = emisiones

    def generar_secuencia(self, n_pasos):
        """Genera una secuencia de estados ocultos y sus observaciones visibles."""
        secuencia_oculta = []
        secuencia_visible = []
        
        # Estado inicial
        estado_actual = random.choices(self.estados, weights=[self.prob_inicial[e] for e in self.estados])[0]
        
        for _ in range(n_pasos):
            # Emisión
            obs = random.choices(self.observaciones, weights=[self.emisiones[estado_actual][o] for o in self.observaciones])[0]
            secuencia_oculta.append(estado_actual)
            secuencia_visible.append(obs)
            
            # Transición
            estado_actual = random.choices(self.estados, weights=[self.transiciones[estado_actual][e] for e in self.estados])[0]
            
        return secuencia_oculta, secuencia_visible

    def viterbi(self, secuencia_obs):
        """Algoritmo de Viterbi para encontrar la secuencia de estados más probable."""
        n = len(secuencia_obs)
        # T[estado][paso] = (probabilidad, estado_previo)
        T = [{estado: (self.prob_inicial[estado] * self.emisiones[estado][secuencia_obs[0]], None) for estado in self.estados}]

        for i in range(1, n):
            paso_actual = {}
            for e_actual in self.estados:
                # Buscamos la mejor transición desde el paso anterior
                prob, e_previo = max(
                    (T[i-1][e_prev][0] * self.transiciones[e_prev][e_actual] * self.emisiones[e_actual][secuencia_obs[i]], e_prev)
                    for e_prev in self.estados
                )
                paso_actual[e_actual] = (prob, e_previo)
            T.append(paso_actual)

        # Reconstrucción del camino (Backtracking)
        camino = []
        prob_max, ultimo_estado = max((T[-1][e][0], e) for e in self.estados)
        camino.append(ultimo_estado)
        
        for i in range(n - 1, 0, -1):
            ultimo_estado = T[i][ultimo_estado][1]
            camino.insert(0, ultimo_estado)
            
        return camino

# --- 1. DEFINICIÓN DEL MODELO ---
estados = ["Saludable", "Enfermo"]
observaciones = ["Normal", "Mareo", "Fiebre"]

p_inicial = {"Saludable": 0.6, "Enfermo": 0.4}

trans = {
    "Saludable": {"Saludable": 0.7, "Enfermo": 0.3},
    "Enfermo": {"Saludable": 0.4, "Enfermo": 0.6}
}

emiss = {
    "Saludable": {"Normal": 0.5, "Mareo": 0.4, "Fiebre": 0.1},
    "Enfermo": {"Normal": 0.1, "Mareo": 0.3, "Fiebre": 0.6}
}

# --- 2. EJECUCIÓN ---
modelo = HMM(estados, observaciones, p_inicial, trans, emiss)

# Generamos datos sintéticos
verdad, pistas = modelo.generar_secuencia(10)
# La IA intenta adivinar la verdad usando solo las pistas
adivinanza = modelo.viterbi(pistas)

print(f"{'Pistas Visibles:':<18} {pistas}")
print(f"{'Realidad Oculta:':<18} {verdad}")
print(f"{'Predicción IA:':<18} {adivinanza}")

aciertos = sum(1 for v, a in zip(verdad, adivinanza) if v == a)
print(f"\nPrecisión de la decodificación: {aciertos/len(verdad)*100}%")