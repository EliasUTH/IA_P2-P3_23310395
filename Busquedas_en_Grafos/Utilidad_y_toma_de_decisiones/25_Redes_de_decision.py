class DecisionNetwork:
    """
    Clase para representar y evaluar una red de decisión.
    Incluye nodos de probabilidad, decisión y utilidad.
    """

    def __init__(self):
        self.nodes = {}  # {name: {'type': 'chance'/'decision'/'utility', 'parents': [], 'probabilities': {}, 'utilities': {}}}
        self.decision_nodes = []
        self.utility_nodes = []

    def add_chance_node(self, name, parents, probabilities):
        """
        Agrega un nodo de probabilidad (chance node).
        probabilities: dict {parent_values_tuple: {value: prob}}
        """
        self.nodes[name] = {
            'type': 'chance',
            'parents': parents,
            'probabilities': probabilities
        }

    def add_decision_node(self, name, parents, choices):
        """
        Agrega un nodo de decisión.
        choices: lista de opciones posibles.
        """
        self.nodes[name] = {
            'type': 'decision',
            'parents': parents,
            'choices': choices
        }
        self.decision_nodes.append(name)

    def add_utility_node(self, name, parents, utilities):
        """
        Agrega un nodo de utilidad.
        utilities: dict {parent_values_tuple: utility_value}
        """
        self.nodes[name] = {
            'type': 'utility',
            'parents': parents,
            'utilities': utilities
        }
        self.utility_nodes.append(name)

    def evaluate(self, evidence=None):
        """
        Evalúa la red de decisión y retorna la utilidad esperada para cada decisión.
        evidence: dict {node: value} para nodos observados.
        """
        if evidence is None:
            evidence = {}

        # Para simplificar, asumimos una red pequeña y evaluamos recursivamente
        def get_probability(node, values, evidence):
            if node in evidence:
                return 1.0 if values[node] == evidence[node] else 0.0

            node_info = self.nodes[node]
            if node_info['type'] == 'chance':
                parents = node_info['parents']
                parent_values = tuple(values[p] for p in parents)
                probs = node_info['probabilities'].get(parent_values, {})
                return probs.get(values[node], 0.0)
            elif node_info['type'] == 'decision':
                # Decisiones son determinísticas basadas en evidencia
                return 1.0 if values[node] in node_info['choices'] else 0.0
            return 1.0  # Para utilidad, no aplica

        def get_utility(node, values):
            node_info = self.nodes[node]
            parents = node_info['parents']
            parent_values = tuple(values[p] for p in parents)
            return node_info['utilities'].get(parent_values, 0.0)

        # Para cada decisión posible, calcular utilidad esperada
        results = {}
        for decision_node in self.decision_nodes:
            decision_info = self.nodes[decision_node]
            for choice in decision_info['choices']:
                # Simular asignación con esta decisión
                assignment = evidence.copy()
                assignment[decision_node] = choice

                # Calcular utilidad esperada (simplificado: enumeración)
                utility = self._expected_utility(assignment, get_probability, get_utility)
                results[(decision_node, choice)] = utility

        return results

    def _expected_utility(self, assignment, get_prob, get_util):
        """
        Calcula utilidad esperada dada una asignación parcial.
        (Versión simplificada para redes pequeñas)
        """
        # Encontrar nodos no asignados
        unassigned = [n for n in self.nodes if n not in assignment and self.nodes[n]['type'] == 'chance']

        if not unassigned:
            # Calcular utilidad total
            total_utility = sum(get_util(u, assignment) for u in self.utility_nodes)
            return total_utility

        # Elegir un nodo no asignado
        node = unassigned[0]
        node_info = self.nodes[node]
        total = 0.0

        # Sumar sobre todos los valores posibles
        for value in node_info['probabilities'].values().__iter__().__next__().keys():  # Obtener valores posibles
            assignment[node] = value
            prob = get_prob(node, assignment, {})
            total += prob * self._expected_utility(assignment, get_prob, get_util)
            del assignment[node]

        return total

# Ejemplo: Problema de la lluvia y paraguas
print("=== Red de Decisión: Lluvia y Paraguas ===")

dn = DecisionNetwork()

# Nodo de probabilidad: Lluvia (sin padres)
dn.add_chance_node('Lluvia', [], {(): {'Sí': 0.3, 'No': 0.7}})

# Nodo de decisión: Llevar paraguas
dn.add_decision_node('Paraguas', [], ['Sí', 'No'])

# Nodo de utilidad: Comodidad (depende de Lluvia y Paraguas)
dn.add_utility_node('Comodidad', ['Lluvia', 'Paraguas'], {
    ('Sí', 'Sí'): 8,  # Lluvia y paraguas: cómodo
    ('Sí', 'No'): 2,  # Lluvia sin paraguas: incómodo
    ('No', 'Sí'): 6,  # No lluvia con paraguas: algo incómodo
    ('No', 'No'): 10  # No lluvia sin paraguas: perfecto
})

# Evaluar decisiones
utilities = dn.evaluate()
print("Utilidades esperadas:")
for (node, choice), util in utilities.items():
    print(f"  Decisión {node}={choice}: Utilidad esperada = {util:.2f}")

# Recomendación
best_decision = max(utilities, key=utilities.get)
print(f"\nMejor decisión: {best_decision[0]} = {best_decision[1]} (Utilidad: {utilities[best_decision]:.2f})")