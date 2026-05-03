class MDP:
    """
    Clase para representar un Proceso de Decisión de Markov (MDP).
    """

    def __init__(self, states, actions, transitions, rewards, gamma=0.9, terminal_states=None):
        """
        Inicializa el MDP.

        Parámetros:
        - states: lista de estados
        - actions: dict de estado -> lista de acciones posibles
        - transitions: dict de (estado, acción) -> dict de estado_siguiente -> probabilidad
        - rewards: dict de (estado, acción, estado_siguiente) -> recompensa
        - gamma: factor de descuento (0 <= gamma < 1)
        - terminal_states: lista de estados terminales (opcional)
        """
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards
        self.gamma = gamma
        self.terminal_states = terminal_states or []

    def get_reward(self, state, action, next_state):
        """Obtiene la recompensa para una transición."""
        return self.rewards.get((state, action, next_state), 0)

    def get_transition_prob(self, state, action, next_state):
        """Obtiene la probabilidad de transición."""
        return self.transitions.get((state, action), {}).get(next_state, 0)

    def is_terminal(self, state):
        """Verifica si un estado es terminal."""
        return state in self.terminal_states

    def get_expected_reward(self, state, action):
        """Calcula la recompensa esperada para una acción en un estado."""
        expected_reward = 0
        for next_state in self.transitions.get((state, action), {}):
            prob = self.get_transition_prob(state, action, next_state)
            reward = self.get_reward(state, action, next_state)
            expected_reward += prob * reward
        return expected_reward

    def get_transition_probs(self, state, action):
        """Obtiene las probabilidades de transición para una acción."""
        return self.transitions.get((state, action), {})

def value_iteration(mdp, epsilon=1e-6, max_iterations=1000):
    """
    Algoritmo de iteración de valores para resolver el MDP.

    Parámetros:
    - mdp: instancia de MDP
    - epsilon: umbral de convergencia
    - max_iterations: máximo número de iteraciones

    Retorna:
    - V: dict de estado -> valor óptimo
    - policy: dict de estado -> acción óptima
    """
    V = {s: 0 for s in mdp.states}

    for iteration in range(max_iterations):
        delta = 0
        V_new = V.copy()

        for state in mdp.states:
            if mdp.is_terminal(state):
                V_new[state] = 0
                continue

            if state not in mdp.actions:
                continue

            # Calcular el valor máximo sobre acciones
            action_values = []
            for action in mdp.actions[state]:
                value = mdp.get_expected_reward(state, action)
                for next_state, prob in mdp.get_transition_probs(state, action).items():
                    value += prob * mdp.gamma * V[next_state]
                action_values.append(value)

            V_new[state] = max(action_values) if action_values else 0
            delta = max(delta, abs(V_new[state] - V[state]))

        V = V_new

        if delta < epsilon:
            break

    # Extraer política óptima
    policy = {}
    for state in mdp.states:
        if mdp.is_terminal(state) or state not in mdp.actions:
            continue

        best_action = None
        best_value = float('-inf')
        for action in mdp.actions[state]:
            value = mdp.get_expected_reward(state, action)
            for next_state, prob in mdp.get_transition_probs(state, action).items():
                value += prob * mdp.gamma * V[next_state]
            if value > best_value:
                best_value = value
                best_action = action
        policy[state] = best_action

    return V, policy

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
    # Inicializar política
    policy = {}
    for state in mdp.states:
        if not mdp.is_terminal(state) and state in mdp.actions:
            policy[state] = mdp.actions[state][0]

    for iteration in range(max_iterations):
        # Evaluación de política
        V = {s: 0 for s in mdp.states}
        for _ in range(100):  # Iteraciones suficientes para convergencia
            V_new = V.copy()
            for state in mdp.states:
                if mdp.is_terminal(state):
                    V_new[state] = 0
                    continue
                if state not in policy:
                    continue
                action = policy[state]
                value = mdp.get_expected_reward(state, action)
                for next_state, prob in mdp.get_transition_probs(state, action).items():
                    value += prob * mdp.gamma * V[next_state]
                V_new[state] = value
            V = V_new

        # Mejora de política
        policy_stable = True
        for state in mdp.states:
            if mdp.is_terminal(state) or state not in mdp.actions:
                continue

            old_action = policy[state]
            best_action = None
            best_value = float('-inf')
            for action in mdp.actions[state]:
                value = mdp.get_expected_reward(state, action)
                for next_state, prob in mdp.get_transition_probs(state, action).items():
                    value += prob * mdp.gamma * V[next_state]
                if value > best_value:
                    best_value = value
                    best_action = action

            policy[state] = best_action
            if old_action != best_action:
                policy_stable = False

        if policy_stable:
            break

    return V, policy

# Ejemplo: MDP simple con recompensas y transiciones
print("=== Proceso de Decisión de Markov (MDP) ===")

# Definir estados, acciones, transiciones y recompensas
states = ['A', 'B', 'C']
actions = {
    'A': ['izquierda', 'derecha'],
    'B': ['izquierda', 'derecha'],
    'C': ['izquierda', 'derecha']
}

transitions = {
    ('A', 'izquierda'): {'A': 0.9, 'B': 0.1},
    ('A', 'derecha'): {'A': 0.1, 'C': 0.9},
    ('B', 'izquierda'): {'A': 0.8, 'B': 0.2},
    ('B', 'derecha'): {'B': 0.7, 'C': 0.3},
    ('C', 'izquierda'): {'B': 0.6, 'C': 0.4},
    ('C', 'derecha'): {'C': 0.5, 'A': 0.5}
}

rewards = {
    ('A', 'izquierda', 'A'): -1,
    ('A', 'izquierda', 'B'): 5,
    ('A', 'derecha', 'A'): -1,
    ('A', 'derecha', 'C'): 10,
    ('B', 'izquierda', 'A'): 2,
    ('B', 'izquierda', 'B'): -2,
    ('B', 'derecha', 'B'): -2,
    ('B', 'derecha', 'C'): 1,
    ('C', 'izquierda', 'B'): 3,
    ('C', 'izquierda', 'C'): -3,
    ('C', 'derecha', 'C'): -3,
    ('C', 'derecha', 'A'): 4
}

mdp = MDP(states, actions, transitions, rewards, gamma=0.9)

print("Resolviendo con Iteración de Valores:")
V_vi, policy_vi = value_iteration(mdp)
print("Valores óptimos:")
for state in states:
    print(f"  V({state}) = {V_vi[state]:.2f}")
print("Política óptima:")
for state in states:
    if state in policy_vi:
        print(f"  pi({state}) = {policy_vi[state]}")

print("\nResolviendo con Iteración de Políticas:")
V_pi, policy_pi = policy_iteration(mdp)
print("Valores óptimos:")
for state in states:
    print(f"  V({state}) = {V_pi[state]:.2f}")
print("Política óptima:")
for state in states:
    if state in policy_pi:
        print(f"  pi({state}) = {policy_pi[state]}")