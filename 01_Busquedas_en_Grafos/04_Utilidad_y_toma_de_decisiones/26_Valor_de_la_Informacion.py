class DecisionNetwork:
    """
    Clase simplificada para redes de decisión (reutilizada del archivo anterior).
    """

    def __init__(self):
        self.nodes = {}
        self.decision_nodes = []
        self.utility_nodes = []

    def add_chance_node(self, name, parents, probabilities):
        self.nodes[name] = {
            'type': 'chance',
            'parents': parents,
            'probabilities': probabilities
        }

    def add_decision_node(self, name, parents, choices):
        self.nodes[name] = {
            'type': 'decision',
            'parents': parents,
            'choices': choices
        }
        self.decision_nodes.append(name)

    def add_utility_node(self, name, parents, utilities):
        self.nodes[name] = {
            'type': 'utility',
            'parents': parents,
            'utilities': utilities
        }
        self.utility_nodes.append(name)

    def evaluate(self, evidence=None):
        if evidence is None:
            evidence = {}

        def get_probability(node, values, evidence):
            if node in evidence:
                return 1.0 if values.get(node) == evidence[node] else 0.0
            node_info = self.nodes[node]
            if node_info['type'] == 'chance':
                parents = node_info['parents']
                parent_values = tuple(values.get(p) for p in parents)
                probs = node_info['probabilities'].get(parent_values, {})
                return probs.get(values.get(node), 0.0)
            return 1.0

        def get_utility(node, values):
            node_info = self.nodes[node]
            parents = node_info['parents']
            parent_values = tuple(values.get(p) for p in parents)
            return node_info['utilities'].get(parent_values, 0.0)

        results = {}
        for decision_node in self.decision_nodes:
            decision_info = self.nodes[decision_node]
            for choice in decision_info['choices']:
                assignment = evidence.copy()
                assignment[decision_node] = choice
                utility = self._expected_utility(assignment, get_probability, get_utility, evidence)
                results[(decision_node, choice)] = utility
        return results

    def _expected_utility(self, assignment, get_prob, get_util, evidence):
        unassigned = [n for n in self.nodes if n not in assignment and self.nodes[n]['type'] == 'chance']
        if not unassigned:
            return sum(get_util(u, assignment) for u in self.utility_nodes)

        node = unassigned[0]
        node_info = self.nodes[node]
        total = 0.0
        for parent_combo in node_info['probabilities']:
            for value, prob in node_info['probabilities'][parent_combo].items():
                assignment[node] = value
                total += prob * self._expected_utility(assignment, get_prob, get_util, evidence)
                del assignment[node]
        return total

def value_of_information(dn, decision_node, info_node, prior_evidence=None):
    """
    Calcula el valor de la información para un nodo de información dado un nodo de decisión.

    Parámetros:
    - dn: instancia de DecisionNetwork
    - decision_node: nombre del nodo de decisión
    - info_node: nombre del nodo de información (chance node)
    - prior_evidence: evidencia previa (dict)

    Retorna: valor de la información (float)
    """
    if prior_evidence is None:
        prior_evidence = {}

    # Utilidad esperada sin información
    utilities_no_info = dn.evaluate(prior_evidence)
    best_no_info = max(utilities_no_info.values())

    # Utilidad esperada con información perfecta
    info_values = list(dn.nodes[info_node]['probabilities'][()].keys())  # Asumiendo sin padres
    expected_utility_with_info = 0.0

    for value in info_values:
        # Probabilidad de este valor
        prob_value = dn.nodes[info_node]['probabilities'][()].get(value, 0.0)

        # Utilidad esperada dado este valor observado
        evidence_with_info = prior_evidence.copy()
        evidence_with_info[info_node] = value
        utilities_with_info = dn.evaluate(evidence_with_info)
        best_with_info = max(utilities_with_info.values())

        expected_utility_with_info += prob_value * best_with_info

    # Valor de la información
    voi = expected_utility_with_info - best_no_info
    return voi

# Ejemplo: Valor de saber si llueve antes de decidir paraguas
print("=== Valor de la Información ===")

dn = DecisionNetwork()

# Nodo de probabilidad: Lluvia
dn.add_chance_node('Lluvia', [], {(): {'Sí': 0.3, 'No': 0.7}})

# Nodo de decisión: Paraguas
dn.add_decision_node('Paraguas', [], ['Sí', 'No'])

# Nodo de utilidad: Comodidad
dn.add_utility_node('Comodidad', ['Lluvia', 'Paraguas'], {
    ('Sí', 'Sí'): 8,
    ('Sí', 'No'): 2,
    ('No', 'Sí'): 6,
    ('No', 'No'): 10
})

# Calcular valor de la información sobre Lluvia
voi = value_of_information(dn, 'Paraguas', 'Lluvia')
print(f"Valor de la información sobre Lluvia: {voi:.2f}")

# Utilidades sin info
utilities_no_info = dn.evaluate()
best_no_info = max(utilities_no_info.values())
print(f"Utilidad esperada sin información: {best_no_info:.2f}")

# Utilidades con info perfecta
expected_with_info = 0.0
for lluvia in ['Sí', 'No']:
    prob = 0.3 if lluvia == 'Sí' else 0.7
    utilities_with_info = dn.evaluate({'Lluvia': lluvia})
    best_with_info = max(utilities_with_info.values())
    expected_with_info += prob * best_with_info
    print(f"  Si Lluvia={lluvia} (prob={prob}): Mejor utilidad = {best_with_info:.2f}")

print(f"Utilidad esperada con información perfecta: {expected_with_info:.2f}")
print(f"Valor de la información: {expected_with_info - best_no_info:.2f}")