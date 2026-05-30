print("=== AGENTE LÓGICO: EXPLORADOR DEL MUNDO DE WUMPUS ===\n")
# --- 1. EL ENTORNO (MUNDO FÍSICO) ---
# Una cuadrícula de 3x3. El agente empieza en (0,0).
# Hay un pozo mortal en (0,2). Si te acercas a una casilla de un pozo, sientes "Brisa".


mundo_real = {
    (0, 0): {"brisa": False, "pozo": False},
    (1, 0): {"brisa": False, "pozo": False},
    (2, 0): {"brisa": False, "pozo": False},
    (0, 1): {"brisa": True,  "pozo": False}, # Casilla adyacente al pozo
    (1, 1): {"brisa": True,  "pozo": False}, # Casilla adyacente al pozo
    (2, 1): {"brisa": False, "pozo": False},
    (0, 2): {"brisa": False, "pozo": True},  # POZO MORTAL
    (1, 2): {"brisa": True,  "pozo": False}, # Casilla adyacente al pozo
    (2, 2): {"brisa": False, "pozo": False}
}


def obtener_vecinos(x, y):
    """Devuelve las coordenadas adyacentes válidas (arriba, abajo, izq, der)."""
    vecinos = []
    if x > 0: vecinos.append((x - 1, y))
    if x < 2: vecinos.append((x + 1, y))
    if y > 0: vecinos.append((x, y - 1))
    if y < 2: vecinos.append((x, y + 1))
    return vecinos


# --- 2. LA MENTE DEL AGENTE (BASE DE CONOCIMIENTO) ---
class AgenteExplorador:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.kb_seguros = set()       # Hechos: Casillas que sabemos 100% que no tienen pozo
        self.kb_visitados = set()     # Hechos: Casillas donde ya estuvimos
        self.kb_sospechosos = set()   # Hechos: Casillas que PODRÍAN tener un pozo
        self.kb_pozos = set()         # Hechos: Casillas que sabemos 100% que TIENEN pozo
        # El agente sabe axiomáticamente que su punto de partida es seguro
        self.marcar_seguro(0, 0)


    def marcar_seguro(self, x, y):
        if (x, y) not in self.kb_seguros:
            self.kb_seguros.add((x, y))
            if (x, y) in self.kb_sospechosos:
                self.kb_sospechosos.remove((x, y)) # Silogismo Disyuntivo aplicado


    # --- FASE A: PERCEPCIÓN ---
    def percibir(self, entorno):
        """El agente lee los sensores en su celda actual."""
        self.kb_visitados.add((self.x, self.y))
        siente_brisa = entorno[(self.x, self.y)]["brisa"]
        print(f"[{self.x},{self.y}] Percibo Brisa: {siente_brisa}")
        return siente_brisa


    # --- FASE B: INFERENCIA LÓGICA (EL MOTOR DE FOL) ---
    def razonar(self, siente_brisa):
        """
        Aplica reglas lógicas de Primer Orden sobre los vecinos.
        """
        vecinos = obtener_vecinos(self.x, self.y)
        

        # REGLA 1 (Causal Inversa): ∀v (¬Brisa(x,y) ∧ Vecino(v, (x,y)) ⇒ Seguro(v))
        # "Si no siento brisa aquí, absolutamente todos mis vecinos son seguros."
        if not siente_brisa:
            for vx, vy in vecinos:
                self.marcar_seguro(vx, vy)
                

        # REGLA 2 (Diagnóstica): ∀v (Brisa(x,y) ∧ Vecino(v, (x,y)) ⇒ ∃v Pozo(v))
        # "Si siento brisa, al menos un vecino tiene un pozo."
        else:
            for vx, vy in vecinos:
                # Si no sabemos que es seguro, se vuelve sospechoso
                if (vx, vy) not in self.kb_seguros:
                    self.kb_sospechosos.add((vx, vy))


        # REGLA 3 (Resolución / Silogismo Disyuntivo)
        # Si tengo una casilla sospechosa aislada (todas las demás opciones se han vuelto seguras),
        # entonces esa casilla DEBE ser el pozo.
        if siente_brisa:
            posibles_pozos = [v for v in vecinos if v in self.kb_sospechosos]
            if len(posibles_pozos) == 1:
                px, py = posibles_pozos[0]
                self.kb_pozos.add((px, py))
                self.kb_sospechosos.remove((px, py))
                print(f"   => ¡DEDUCCIÓN LÓGICA! He descubierto un POZO MORTAL en {px},{py}. ¡Peligro!")


    # --- FASE C: ACCIÓN ---
    def actuar(self):
        """El agente decide a dónde moverse usando su Base de Conocimiento."""
        # Prioridad 1: Visitar una casilla segura que aún no hayamos explorado
        casillas_seguras_no_visitadas = self.kb_seguros - self.kb_visitados
        

        if casillas_seguras_no_visitadas:
            # Nos movemos a la primera opción disponible
            nx, ny = list(casillas_seguras_no_visitadas)[0]
            print(f"   -> ACCIÓN: Moviendo a casilla 100% segura en [{nx},{ny}]\n")
            self.x, self.y = nx, ny
            return True
        print("   -> ACCIÓN: No hay movimientos seguros disponibles. Misión abortada para sobrevivir.\n")
        return False


# --- 3. CICLO DE VIDA DEL AGENTE ---
explorador = AgenteExplorador()
pasos = 0
max_pasos = 5


print("Iniciando exploración autónoma...\n")
while pasos < max_pasos:
    print("-" * 40)
    print(f"PASO {pasos + 1}: Agente en [{explorador.x},{explorador.y}]")
    # 1. Percibir
    brisa = explorador.percibir(mundo_real)
    # 2. Razonar
    explorador.razonar(brisa)
    # 3. Actuar
    continua = explorador.actuar()
    if not continua:
        break
    pasos += 1


print("-" * 40)
print("=== INFORME FINAL DE LA BASE DE CONOCIMIENTO ===")
print(f"Casillas Seguras Conocidas: {explorador.kb_seguros}")
print(f"Pozos Mortales Evitados: {explorador.kb_pozos}")


print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Arquitectura de Agente: El bucle principal no contiene lógica del juego; es puramente un ciclo 'Sensar -> Pensar -> Actuar'.")
print("2. Monotonicidad Lógica: A medida que el agente avanza, su Base de Conocimiento solo CRECE. Nunca 'desaprende' que una casilla es segura.")
print("3. Instanciación Universal: El código implementa implícitamente la regla universal evaluando un bucle 'for vx, vy in vecinos'. Esto mapea el cuantificador ∀ a variables de iteración en Python.")