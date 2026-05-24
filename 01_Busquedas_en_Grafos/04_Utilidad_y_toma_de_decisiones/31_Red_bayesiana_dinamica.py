class DynamicBayesianNetwork:
    """
    Clase para representar una Red Bayesiana Dinámica (DBN).
    Modela procesos temporales con variables ocultas y observadas.
    """

    def __init__(self, hidden_states, observations, transition_probs, emission_probs, initial_probs):
        """
        Inicializa la DBN.

        Parámetros:
        - hidden_states: lista de estados ocultos
        - observations: lista de observaciones posibles
        - transition_probs: dict de (estado_t, estado_t+1) -> probabilidad
        - emission_probs: dict de (estado_oculto, observacion) -> probabilidad
        - initial_probs: dict de estado_oculto -> probabilidad inicial
        """
        self.hidden_states = hidden_states
        self.observations = observations
        self.transition_probs = transition_probs
        self.emission_probs = emission_probs
        self.initial_probs = initial_probs

    def get_transition_prob(self, state_t, state_t1):
        """Probabilidad de transición P(state_t+1 | state_t)."""
        return self.transition_probs.get((state_t, state_t1), 0)

    def get_emission_prob(self, state, observation):
        """Probabilidad de emisión P(observation | state)."""
        return self.emission_probs.get((state, observation), 0)

    def get_initial_prob(self, state):
        """Probabilidad inicial P(state_0)."""
        return self.initial_probs.get(state, 0)

    def forward_algorithm(self, observations):
        """
        Algoritmo forward para filtrado: calcula P(state_t | observations_0:t).

        Parámetros:
        - observations: lista de observaciones [obs_0, obs_1, ..., obs_T]

        Retorna:
        - forward_probs: lista de dicts, cada uno con P(state_t | obs_0:t)
        """
        T = len(observations)
        forward_probs = []

        # Inicialización t=0
        alpha_0 = {}
        for state in self.hidden_states:
            alpha_0[state] = self.get_initial_prob(state) * self.get_emission_prob(state, observations[0])
        forward_probs.append(alpha_0)

        # Normalizar
        total = sum(alpha_0.values())
        if total > 0:
            for s in alpha_0:
                alpha_0[s] /= total

        # Recursión para t=1 a T
        for t in range(1, T):
            alpha_t = {}
            for state_t1 in self.hidden_states:
                prob = 0
                for state_t in self.hidden_states:
                    prob += forward_probs[t-1][state_t] * self.get_transition_prob(state_t, state_t1)
                alpha_t[state_t1] = prob * self.get_emission_prob(state_t1, observations[t])

            # Normalizar
            total = sum(alpha_t.values())
            if total > 0:
                for s in alpha_t:
                    alpha_t[s] /= total

            forward_probs.append(alpha_t)

        return forward_probs

    def viterbi_algorithm(self, observations):
        """
        Algoritmo de Viterbi para encontrar la secuencia más probable de estados ocultos.

        Parámetros:
        - observations: lista de observaciones

        Retorna:
        - best_path: lista de estados ocultos más probables
        - best_prob: probabilidad de la mejor secuencia
        """
        T = len(observations)
        V = [{} for _ in range(T)]
        backpointer = [{} for _ in range(T)]

        # Inicialización
        for state in self.hidden_states:
            V[0][state] = self.get_initial_prob(state) * self.get_emission_prob(state, observations[0])
            backpointer[0][state] = None

        # Recursión
        for t in range(1, T):
            for state_t1 in self.hidden_states:
                max_prob = 0
                max_state = None
                for state_t in self.hidden_states:
                    prob = V[t-1][state_t] * self.get_transition_prob(state_t, state_t1)
                    if prob > max_prob:
                        max_prob = prob
                        max_state = state_t
                V[t][state_t1] = max_prob * self.get_emission_prob(state_t1, observations[t])
                backpointer[t][state_t1] = max_state

        # Terminación
        best_prob = 0
        best_state = None
        for state in self.hidden_states:
            if V[T-1][state] > best_prob:
                best_prob = V[T-1][state]
                best_state = state

        # Backtrack
        best_path = [best_state]
        for t in range(T-1, 0, -1):
            best_state = backpointer[t][best_state]
            best_path.insert(0, best_state)

        return best_path, best_prob

    def predict_next_state(self, current_belief):
        """
        Predice la distribución del siguiente estado oculto dado la creencia actual.

        Parámetros:
        - current_belief: dict de estado -> probabilidad

        Retorna:
        - next_belief: dict de estado -> probabilidad
        """
        next_belief = {}
        for state_t1 in self.hidden_states:
            prob = 0
            for state_t in self.hidden_states:
                prob += current_belief[state_t] * self.get_transition_prob(state_t, state_t1)
            next_belief[state_t1] = prob
        return next_belief

# Ejemplo: DBN para modelar el clima (oculto) basado en si lleva paraguas (observación)
print("=== Red Bayesiana Dinámica (DBN) ===")

hidden_states = ['Soleado', 'Lluvioso']
observations = ['Con_paraguas', 'Sin_paraguas']

# Probabilidades de transición: P(state_t+1 | state_t)
transition_probs = {
    ('Soleado', 'Soleado'): 0.8,
    ('Soleado', 'Lluvioso'): 0.2,
    ('Lluvioso', 'Soleado'): 0.3,
    ('Lluvioso', 'Lluvioso'): 0.7
}

# Probabilidades de emisión: P(observation | state)
emission_probs = {
    ('Soleado', 'Con_paraguas'): 0.1,  # Poco probable llevar paraguas cuando soleado
    ('Soleado', 'Sin_paraguas'): 0.9,
    ('Lluvioso', 'Con_paraguas'): 0.8,  # Muy probable llevar paraguas cuando lluvioso
    ('Lluvioso', 'Sin_paraguas'): 0.2
}

# Probabilidades iniciales
initial_probs = {
    'Soleado': 0.6,
    'Lluvioso': 0.4
}

dbn = DynamicBayesianNetwork(hidden_states, observations, transition_probs, emission_probs, initial_probs)

# Secuencia de observaciones
observations_seq = ['Sin_paraguas', 'Con_paraguas', 'Sin_paraguas', 'Con_paraguas']

print("Secuencia de observaciones:", observations_seq)

# Filtrado forward
forward_probs = dbn.forward_algorithm(observations_seq)
print("\nProbabilidades de filtrado (P(state_t | obs_0:t)):")
for t, probs in enumerate(forward_probs):
    print(f"  t={t}: {probs}")

# Viterbi para la secuencia más probable
best_path, best_prob = dbn.viterbi_algorithm(observations_seq)
print(f"\nSecuencia más probable de estados ocultos: {best_path}")
print(f"Probabilidad: {best_prob:.6f}")

# Predicción del siguiente estado
current_belief = forward_probs[-1]  # Creencia en t=3
next_belief = dbn.predict_next_state(current_belief)
print(f"\nPredicción del estado en t=4 dado creencia actual: {next_belief}")