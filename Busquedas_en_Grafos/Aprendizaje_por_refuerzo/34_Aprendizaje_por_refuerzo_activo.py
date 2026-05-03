import random
import math

class MDP:
    """
    Clase simple para representar un MDP.
    """

    def __init__(self, states, actions, transitions, rewards, gamma=0.9):
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards
        self.gamma = gamma

    def get_reward(self, state, action, next_state):
        return self.rewards.get((state, action, next_state), 0)

    def get_transition_prob(self, state, action, next_state):
        return self.transitions.get((state, action), {}).get(next_state, 0)

    def sample_next_state(self, state, action):
        """Muestrea el siguiente estado dado el estado y acción actuales."""
        probs = self.transitions.get((state, action), {})
        next_states = list(probs.keys())
        probabilities = list(probs.values())
        return random.choices(next_states, probabilities)[0]

    def is_terminal(self, state):
        """Verifica si un estado es terminal."""
        return state not in self.transitions or not any(self.transitions.get((state, a), {}) for a in self.actions)

class QLearningAgent:
    """
    Agente de aprendizaje por refuerzo activo usando Q-Learning.
    """

    def __init__(self, mdp, alpha=0.1, gamma=0.9, epsilon=0.1):
        """
        Inicializa el agente Q-Learning.

        Parámetros:
        - mdp: instancia de MDP
        - alpha: tasa de aprendizaje
        - gamma: factor de descuento
        - epsilon: parámetro de exploración (epsilon-greedy)
        """
        self.mdp = mdp
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = {}  # Tabla Q: (estado, acción) -> valor

        # Inicializar Q con 0
        for state in mdp.states:
            for action in mdp.actions:
                self.Q[(state, action)] = 0

    def choose_action(self, state):
        """
        Selecciona una acción usando política epsilon-greedy.

        Parámetros:
        - state: estado actual

        Retorna:
        - acción seleccionada
        """
        if random.random() < self.epsilon:
            # Exploración: acción aleatoria
            return random.choice(self.mdp.actions)
        else:
            # Explotación: mejor acción según Q
            q_values = {a: self.Q.get((state, a), 0) for a in self.mdp.actions}
            max_q = max(q_values.values())
            best_actions = [a for a, q in q_values.items() if q == max_q]
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        """
        Actualiza la tabla Q usando la regla de Q-Learning.

        Parámetros:
        - state: estado actual
        - action: acción tomada
        - reward: recompensa recibida
        - next_state: siguiente estado
        """
        # Valor Q actual
        current_q = self.Q.get((state, action), 0)

        # Mejor valor Q para el siguiente estado
        if self.mdp.is_terminal(next_state):
            max_next_q = 0
        else:
            next_q_values = [self.Q.get((next_state, a), 0) for a in self.mdp.actions]
            max_next_q = max(next_q_values)

        # Actualización Q-Learning
        target = reward + self.gamma * max_next_q
        self.Q[(state, action)] = current_q + self.alpha * (target - current_q)

    def get_policy(self):
        """
        Extrae la política óptima de la tabla Q.

        Retorna:
        - dict de estado -> acción óptima
        """
        policy = {}
        for state in self.mdp.states:
            if not self.mdp.is_terminal(state):
                q_values = {a: self.Q.get((state, a), 0) for a in self.mdp.actions}
                best_action = max(q_values, key=q_values.get)
                policy[state] = best_action
        return policy

    def get_value_function(self):
        """
        Calcula la función de valor V(s) = max_a Q(s,a).

        Retorna:
        - dict de estado -> valor
        """
        V = {}
        for state in self.mdp.states:
            if not self.mdp.is_terminal(state):
                q_values = [self.Q.get((state, a), 0) for a in self.mdp.actions]
                V[state] = max(q_values)
            else:
                V[state] = 0
        return V

    def train(self, episodes=1000, max_steps=100):
        """
        Entrena el agente por un número de episodios.

        Parámetros:
        - episodes: número de episodios
        - max_steps: máximo número de pasos por episodio
        """
        for episode in range(episodes):
            state = random.choice(self.mdp.states)

            for step in range(max_steps):
                if self.mdp.is_terminal(state):
                    break

                action = self.choose_action(state)
                next_state = self.mdp.sample_next_state(state, action)
                reward = self.mdp.get_reward(state, action, next_state)

                self.learn(state, action, reward, next_state)

                state = next_state

# Ejemplo: MDP simple para Q-Learning
print("=== Aprendizaje por Refuerzo Activo (Q-Learning) ===")

# Definir MDP
states = ['A', 'B', 'C', 'D']  # D es terminal
actions = ['izquierda', 'derecha']

transitions = {
    ('A', 'izquierda'): {'A': 0.9, 'B': 0.1},
    ('A', 'derecha'): {'A': 0.1, 'C': 0.9},
    ('B', 'izquierda'): {'A': 0.8, 'B': 0.2},
    ('B', 'derecha'): {'B': 0.7, 'C': 0.3},
    ('C', 'izquierda'): {'B': 0.6, 'C': 0.4},
    ('C', 'derecha'): {'C': 0.5, 'D': 0.5}  # D es terminal
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
    ('C', 'derecha', 'D'): 4
}

mdp = MDP(states, actions, transitions, rewards, gamma=0.9)

# Agente Q-Learning
agent = QLearningAgent(mdp, alpha=0.1, gamma=0.9, epsilon=0.1)

# Entrenar
agent.train(episodes=10000, max_steps=50)

# Resultados
print("Tabla Q aprendida:")
for state in states:
    if not mdp.is_terminal(state):
        for action in actions:
            q_val = agent.Q.get((state, action), 0)
            print(f"  Q({state}, {action}) = {q_val:.2f}")

print("\nFunción de valor V(s):")
V = agent.get_value_function()
for state in states:
    print(f"  V({state}) = {V[state]:.2f}")

print("\nPolítica óptima:")
policy = agent.get_policy()
for state, action in policy.items():
    print(f"  π({state}) = {action}")