class NormalFormGame:
    """
    Clase para representar un juego en forma normal (matriz de pagos).
    """

    def __init__(self, players, strategies, payoffs):
        """
        Inicializa el juego.

        Parámetros:
        - players: lista de nombres de jugadores
        - strategies: dict de jugador -> lista de estrategias
        - payoffs: dict de tupla de estrategias -> tupla de pagos (uno por jugador)
        """
        self.players = players
        self.strategies = strategies
        self.payoffs = payoffs

    def get_payoff(self, strategy_profile):
        """Obtiene los pagos para un perfil de estrategias."""
        return self.payoffs.get(strategy_profile, tuple(0 for _ in self.players))

    def is_nash_equilibrium(self, strategy_profile):
        """
        Verifica si un perfil de estrategias es un equilibrio de Nash.

        Parámetros:
        - strategy_profile: tupla de estrategias (una por jugador)

        Retorna:
        - bool: True si es equilibrio de Nash
        """
        for i, player in enumerate(self.players):
            current_payoff = self.get_payoff(strategy_profile)[i]
            for strategy in self.strategies[player]:
                if strategy == strategy_profile[i]:
                    continue
                alt_profile = list(strategy_profile)
                alt_profile[i] = strategy
                alt_payoff = self.get_payoff(tuple(alt_profile))[i]
                if alt_payoff > current_payoff:
                    return False
        return True

    def find_nash_equilibria(self):
        """
        Encuentra todos los equilibrios de Nash mediante búsqueda exhaustiva.

        Retorna:
        - list: lista de perfiles de estrategias que son equilibrios de Nash
        """
        nash_equilibria = []
        strategy_profiles = self._generate_strategy_profiles()

        for profile in strategy_profiles:
            if self.is_nash_equilibrium(profile):
                nash_equilibria.append(profile)

        return nash_equilibria

    def _generate_strategy_profiles(self):
        """Genera todos los posibles perfiles de estrategias."""
        import itertools
        strategy_lists = [self.strategies[player] for player in self.players]
        return list(itertools.product(*strategy_lists))

class AuctionMechanism:
    """
    Clase para representar mecanismos de subasta.
    """

    def __init__(self, bidders, values):
        """
        Inicializa la subasta.

        Parámetros:
        - bidders: lista de postores
        - values: dict de postor -> valor privado
        """
        self.bidders = bidders
        self.values = values

    def second_price_auction(self, bids):
        """
        Subasta de segundo precio (Vickrey).

        Parámetros:
        - bids: dict de postor -> oferta

        Retorna:
        - winner: postor ganador
        - price: precio pagado
        - payoffs: dict de postor -> utilidad
        """
        if not bids:
            return None, 0, {}

        # Encontrar la oferta más alta y la segunda más alta
        sorted_bids = sorted(bids.items(), key=lambda x: x[1], reverse=True)
        winner = sorted_bids[0][0]
        winning_bid = sorted_bids[0][1]
        second_price = sorted_bids[1][1] if len(sorted_bids) > 1 else 0

        payoffs = {}
        for bidder in self.bidders:
            if bidder == winner:
                payoffs[bidder] = self.values[bidder] - second_price
            else:
                payoffs[bidder] = 0

        return winner, second_price, payoffs

    def vcg_auction(self, bids):
        """
        Subasta VCG (Vickrey-Clarke-Groves) para un ítem.

        Parámetros:
        - bids: dict de postor -> oferta

        Retorna:
        - winner: postor ganador
        - payments: dict de postor -> pago
        - payoffs: dict de postor -> utilidad
        """
        if not bids:
            return None, {}, {}

        # Encontrar el ganador (oferta más alta)
        winner = max(bids, key=bids.get)
        winning_value = self.values[winner]

        payments = {}
        payoffs = {}

        for bidder in self.bidders:
            if bidder == winner:
                # Pago VCG: costo externo sin este postor
                other_bids = {k: v for k, v in bids.items() if k != bidder}
                if other_bids:
                    second_highest = max(other_bids.values())
                else:
                    second_highest = 0
                payments[bidder] = second_highest
                payoffs[bidder] = winning_value - second_highest
            else:
                # Otros pagan 0
                payments[bidder] = 0
                payoffs[bidder] = 0

        return winner, payments, payoffs

# Ejemplo 1: Dilema del Prisionero
print("=== Teoría de Juegos: Equilibrios ===")

players = ['Jugador1', 'Jugador2']
strategies = {
    'Jugador1': ['Confesar', 'Callar'],
    'Jugador2': ['Confesar', 'Callar']
}
payoffs = {
    ('Confesar', 'Confesar'): (-5, -5),
    ('Confesar', 'Callar'): (0, -10),
    ('Callar', 'Confesar'): (-10, 0),
    ('Callar', 'Callar'): (-1, -1)
}

game = NormalFormGame(players, strategies, payoffs)
nash_eq = game.find_nash_equilibria()

print("Juego: Dilema del Prisionero")
print("Equilibrios de Nash:")
for eq in nash_eq:
    print(f"  {eq} -> Pagos: {game.get_payoff(eq)}")

# Ejemplo 2: Subasta de Segundo Precio
print("\n=== Teoría de Juegos: Mecanismos ===")

bidders = ['A', 'B', 'C']
values = {'A': 100, 'B': 80, 'C': 60}
bids = {'A': 90, 'B': 85, 'C': 70}

auction = AuctionMechanism(bidders, values)

print("Subasta de Segundo Precio:")
winner, price, payoffs = auction.second_price_auction(bids)
print(f"  Ganador: {winner}, Precio: {price}")
print(f"  Utilidades: {payoffs}")

print("\nSubasta VCG:")
winner, payments, payoffs = auction.vcg_auction(bids)
print(f"  Ganador: {winner}")
print(f"  Pagos: {payments}")
print(f"  Utilidades: {payoffs}")