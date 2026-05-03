class POMDP:
    """
    Clase para representar un Proceso de Decisión de Markov Parcialmente Observable (POMDP).
    """

    def __init__(self, states, actions, observations, transitions, observations_probs, rewards, gamma=0.9):
        """
        Inicializa el POMDP.

        Parámetros:
        - states: lista de estados
        - actions: lista de acciones
        - observations: lista de observaciones
        - transitions: dict de (estado, acción) -> dict de estado_siguiente -> probabilidad
        - observations_probs: dict de (estado, acción, estado_siguiente) -> dict de observación -> probabilidad
        - rewards: dict de (estado, acción, estado_siguiente) -> recompensa
        - gamma: factor de descuento
        """
        self.states = states
        self.actions = actions
        self.observations = observations
        self.transitions = transitions
        self.observations_probs = observations_probs
        self.rewards = rewards
        self.gamma = gamma

    def get_transition_prob(self, state, action, next_state):
        """Probabilidad de transición P(s'|s,a)."""
        return self.transitions.get((state, action), {}).get(next_state, 0)

    def get_observation_prob(self, state, action, next_state, observation):
        """Probabilidad de observación P(o|s',a)."""
        return self.observations_probs.get((state, action, next_state), {}).get(observation, 0)

    def get_reward(self, state, action, next_state):
        """Recompensa para una transición."""
        return self.rewards.get((state, action, next_state), 0)

    def update_belief(self, belief, action, observation):
        """
        Actualiza el estado de creencia dado una acción y observación.

        Parámetros:
        - belief: dict de estado -> probabilidad (estado de creencia actual)
        - action: acción tomada
        - observation: observación recibida

        Retorna:
        - new_belief: dict de estado -> nueva probabilidad
        """
        new_belief = {s: 0 for s in self.states}

        # Calcular el numerador: sum_s P(o|s',a) * P(s'|s,a) * b(s)
        for next_state in self.states:
            prob_obs = 0
            for state in self.states:
                trans_prob = self.get_transition_prob(state, action, next_state)
                obs_prob = self.get_observation_prob(state, action, next_state, observation)
                prob_obs += obs_prob * trans_prob * belief[state]
            new_belief[next_state] = prob_obs

        # Normalizar
        total = sum(new_belief.values())
        if total > 0:
            for s in new_belief:
                new_belief[s] /= total
        else:
            # Si no hay probabilidad, mantener creencia uniforme
            for s in new_belief:
                new_belief[s] = 1 / len(self.states)

        return new_belief

    def get_expected_reward(self, belief, action):
        """
        Calcula la recompensa esperada para una acción dada la creencia.

        Parámetros:
        - belief: estado de creencia
        - action: acción

        Retorna:
        - expected_reward: float
        """
        expected_reward = 0
        for state in self.states:
            for next_state in self.states:
                trans_prob = self.get_transition_prob(state, action, next_state)
                reward = self.get_reward(state, action, next_state)
                expected_reward += belief[state] * trans_prob * reward
        return expected_reward

    def get_next_belief_distribution(self, belief, action):
        """
        Obtiene la distribución de creencias siguiente para cada observación posible.

        Parámetros:
        - belief: estado de creencia actual
        - action: acción

        Retorna:
        - next_beliefs: dict de observación -> new_belief
        """
        next_beliefs = {}
        for observation in self.observations:
            next_beliefs[observation] = self.update_belief(belief, action, observation)
        return next_beliefs

def pomdp_value_iteration(pomdp, belief_states, epsilon=1e-6, max_iterations=100):
    """
    Iteración de valores aproximada para POMDP usando un conjunto discreto de estados de creencia.

    Parámetros:
    - pomdp: instancia de POMDP
    - belief_states: lista de estados de creencia (cada uno es un dict estado -> prob)
    - epsilon: umbral de convergencia
    - max_iterations: máximo número de iteraciones

    Retorna:
    - V: dict de belief_state -> valor
    - policy: dict de belief_state -> acción óptima
    """
    V = {tuple(sorted(b.items())): 0 for b in belief_states}

    for iteration in range(max_iterations):
        delta = 0
        V_new = {}

        for belief in belief_states:
            belief_key = tuple(sorted(belief.items()))
            best_value = float('-inf')
            best_action = None

            for action in pomdp.actions:
                value = pomdp.get_expected_reward(belief, action)
                next_beliefs = pomdp.get_next_belief_distribution(belief, action)

                expected_future = 0
                for obs, next_belief in next_beliefs.items():
                    next_key = tuple(sorted(next_belief.items()))
                    expected_future += V.get(next_key, 0)  # Asumir uniforme si no está

                value += pomdp.gamma * expected_future
                if value > best_value:
                    best_value = value
                    best_action = action

            V_new[belief_key] = best_value
            delta = max(delta, abs(V_new[belief_key] - V[belief_key]))

        V = V_new

        if delta < epsilon:
            break

    # Extraer política
    policy = {}
    for belief in belief_states:
        belief_key = tuple(sorted(belief.items()))
        best_action = None
        best_value = float('-inf')

        for action in pomdp.actions:
            value = pomdp.get_expected_reward(belief, action)
            next_beliefs = pomdp.get_next_belief_distribution(belief, action)
            expected_future = sum(V.get(tuple(sorted(nb.items())), 0) for nb in next_beliefs.values())
            value += pomdp.gamma * expected_future
            if value > best_value:
                best_value = value
                best_action = action

        policy[belief_key] = best_action

    return V, policy

# Ejemplo: POMDP simple con 2 estados, 2 acciones, 2 observaciones
print("=== MDP Parcialmente Observable (POMDP) ===")

states = ['Soleado', 'Lluvioso']
actions = ['Llevar_paraguas', 'No_llevar_paraguas']
observations = ['Seco', 'Mojado']

transitions = {
    ('Soleado', 'Llevar_paraguas'): {'Soleado': 0.8, 'Lluvioso': 0.2},
    ('Soleado', 'No_llevar_paraguas'): {'Soleado': 0.9, 'Lluvioso': 0.1},
    ('Lluvioso', 'Llevar_paraguas'): {'Soleado': 0.1, 'Lluvioso': 0.9},
    ('Lluvioso', 'No_llevar_paraguas'): {'Soleado': 0.2, 'Lluvioso': 0.8}
}

observations_probs = {
    ('Soleado', 'Llevar_paraguas', 'Soleado'): {'Seco': 0.9, 'Mojado': 0.1},
    ('Soleado', 'Llevar_paraguas', 'Lluvioso'): {'Seco': 0.3, 'Mojado': 0.7},
    ('Soleado', 'No_llevar_paraguas', 'Soleado'): {'Seco': 1.0, 'Mojado': 0.0},
    ('Soleado', 'No_llevar_paraguas', 'Lluvioso'): {'Seco': 0.4, 'Mojado': 0.6},
    ('Lluvioso', 'Llevar_paraguas', 'Soleado'): {'Seco': 0.8, 'Mojado': 0.2},
    ('Lluvioso', 'Llevar_paraguas', 'Lluvioso'): {'Seco': 0.2, 'Mojado': 0.8},
    ('Lluvioso', 'No_llevar_paraguas', 'Soleado'): {'Seco': 0.9, 'Mojado': 0.1},
    ('Lluvioso', 'No_llevar_paraguas', 'Lluvioso'): {'Seco': 0.1, 'Mojado': 0.9}
}

rewards = {
    ('Soleado', 'Llevar_paraguas', 'Soleado'): -1,  # Incomodidad sin necesidad
    ('Soleado', 'Llevar_paraguas', 'Lluvioso'): 9,   # Bueno llevar cuando llueve
    ('Soleado', 'No_llevar_paraguas', 'Soleado'): 10, # Perfecto
    ('Soleado', 'No_llevar_paraguas', 'Lluvioso'): -10, # Malo no llevar cuando llueve
    ('Lluvioso', 'Llevar_paraguas', 'Soleado'): 8,   # Bueno
    ('Lluvioso', 'Llevar_paraguas', 'Lluvioso'): 9,   # Bueno
    ('Lluvioso', 'No_llevar_paraguas', 'Soleado'): 5, # Aceptable
    ('Lluvioso', 'No_llevar_paraguas', 'Lluvioso'): -5 # Malo
}

pomdp = POMDP(states, actions, observations, transitions, observations_probs, rewards, gamma=0.9)

# Estados de creencia de ejemplo
belief_states = [
    {'Soleado': 1.0, 'Lluvioso': 0.0},  # Seguro soleado
    {'Soleado': 0.0, 'Lluvioso': 1.0},  # Seguro lluvioso
    {'Soleado': 0.5, 'Lluvioso': 0.5}   # Incierto
]

# Resolver con iteración de valores
V, policy = pomdp_value_iteration(pomdp, belief_states)

print("Valores para estados de creencia:")
for i, belief in enumerate(belief_states):
    key = tuple(sorted(belief.items()))
    print(f"  Creencia {i+1} {belief}: V = {V[key]:.2f}")

print("\nPolítica óptima:")
for i, belief in enumerate(belief_states):
    key = tuple(sorted(belief.items()))
    print(f"  Creencia {i+1}: {policy[key]}")

# Demostrar actualización de creencia
print("\n=== Actualización de Creencia ===")
initial_belief = {'Soleado': 0.5, 'Lluvioso': 0.5}
print(f"Creencia inicial: {initial_belief}")

action = 'No_llevar_paraguas'
observation = 'Seco'
new_belief = pomdp.update_belief(initial_belief, action, observation)
print(f"Después de acción '{action}' y observación '{observation}': {new_belief}")