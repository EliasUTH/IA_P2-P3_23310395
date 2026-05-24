class MDP:
    """
    Clase simple para representar un Proceso de Decisión de Markov (MDP).
    """

    def __init__(self, states, actions, transitions, rewards, gamma=0.9):
        """
        Inicializa el MDP.

        Parámetros:
        - states: lista de estados
        - actions: dict de estado -> lista de acciones posibles
        - transitions: dict de (estado, acción) -> dict de estado_siguiente -> probabilidad
        - rewards: dict de (estado, acción, estado_siguiente) -> recompensa
        - gamma: factor de descuento
        """
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards
        self.gamma = gamma

    def get_reward(self, state, action, next_state):
        return self.rewards.get((state, action, next_state), 0)

    def get_transition_prob(self, state, action, next_state):
        return self.transitions.get((state, action), {}).get(next_state, 0)

def policy_evaluation(mdp, policy, epsilon=1e-6, max_iterations=1000):
    """
    Evalúa una política dada, calculando los valores V(s).

    Parámetros:
    - mdp: instancia de MDP
    - policy: dict de estado -> acción
    - epsilon: umbral de convergencia
    - max_iterations: máximo número de iteraciones

    Retorna:
    - V: dict de estado -> valor
    """
    V = {s: 0 for s in mdp.states}

    for iteration in range(max_iterations):
        delta = 0
        V_new = {}

        for state in mdp.states:
            if state not in policy:
                V_new[state] = 0
                continue

            action = policy[state]
            value = 0
            for next_state in mdp.transitions.get((state, action), {}):
                prob = mdp.get_transition_prob(state, action, next_state)
                reward = mdp.get_reward(state, action, next_state)
                value += prob * (reward + mdp.gamma * V[next_state])

            V_new[state] = value
            delta = max(delta, abs(V_new[state] - V[state]))

        V = V_new

        if delta < epsilon:
            break

    return V

def policy_improvement(mdp, V, old_policy):
    """
    Mejora la política basada en los valores V.

    Parámetros:
    - mdp: instancia de MDP
    - V: dict de estado -> valor
    - old_policy: política anterior

    Retorna:
    - policy: dict de estado -> acción óptima
    - policy_stable: bool
    """
    policy = {}
    policy_stable = True

    for state in mdp.states:
        if state not in mdp.actions:
            continue

        # Encontrar la acción que maximiza el valor
        best_action = None
        best_value = float('-inf')

        for action in mdp.actions[state]:
            value = 0
            for next_state in mdp.transitions.get((state, action), {}):
                prob = mdp.get_transition_prob(state, action, next_state)
                reward = mdp.get_reward(state, action, next_state)
                value += prob * (reward + mdp.gamma * V[next_state])

            if value > best_value:
                best_value = value
                best_action = action

        policy[state] = best_action

        if old_policy.get(state) != best_action:
            policy_stable = False

    return policy, policy_stable

def policy_iteration(mdp, max_iterations=100):
    """
    Algoritmo de iteración de políticas para resolver el MDP.

    Parámetros:
    - mdp: instancia de MDP
    - max_iterations: máximo número de iteraciones

    Retorna:
    - V: dict de estado -> valor óptimo
    - policy: dict de estado -> acción óptima
    """
    # Inicializar política aleatoria
    policy = {}
    for state in mdp.states:
        if state in mdp.actions:
            policy[state] = mdp.actions[state][0]  # Primera acción

    for iteration in range(max_iterations):
        # Evaluación de política
        V = policy_evaluation(mdp, policy)

        # Mejora de política
        new_policy, policy_stable = policy_improvement(mdp, V, policy)

        policy = new_policy

        if policy_stable:
            break

    return V, policy

# Ejemplo: MDP simple con 3 estados
print("=== Iteración de Políticas ===")

# Definir estados y acciones
states = ['A', 'B', 'C']
actions = {
    'A': ['ir_a_B', 'ir_a_C'],
    'B': ['ir_a_A', 'ir_a_C'],
    'C': ['ir_a_A', 'ir_a_B']
}

# Transiciones: (estado, acción) -> {estado_siguiente: prob}
transitions = {
    ('A', 'ir_a_B'): {'B': 1.0},
    ('A', 'ir_a_C'): {'C': 1.0},
    ('B', 'ir_a_A'): {'A': 1.0},
    ('B', 'ir_a_C'): {'C': 1.0},
    ('C', 'ir_a_A'): {'A': 1.0},
    ('C', 'ir_a_B'): {'B': 1.0}
}

# Recompensas: (estado, acción, estado_siguiente) -> recompensa
rewards = {
    ('A', 'ir_a_B', 'B'): 1,
    ('A', 'ir_a_C', 'C'): 10,
    ('B', 'ir_a_A', 'A'): 0,
    ('B', 'ir_a_C', 'C'): 5,
    ('C', 'ir_a_A', 'A'): 2,
    ('C', 'ir_a_B', 'B'): 3
}

# Crear MDP
mdp = MDP(states, actions, transitions, rewards, gamma=0.9)

# Ejecutar iteración de políticas
V, policy = policy_iteration(mdp)

print("Valores óptimos:")
for state in states:
    print(f"  V({state}) = {V[state]:.2f}")

print("\nPolítica óptima:")
for state in states:
    if state in policy:
        print(f"  pi({state}) = {policy[state]}")
    else:
        print(f"  {state} es estado terminal")