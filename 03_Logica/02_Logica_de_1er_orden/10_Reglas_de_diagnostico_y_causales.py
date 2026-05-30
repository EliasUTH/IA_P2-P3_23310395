print("=== LÓGICA DE 1ER ORDEN: REGLAS CAUSALES Y DIAGNÓSTICAS ===\n")
# --- 1. EL DOMINIO (El Universo de Pacientes) ---
# Representamos el estado clínico de los pacientes. 
# 'None' significa que esa información aún es Desconocida para el sistema.
pacientes = {
    "Ana":    {"gripe": True,  "infeccion": None,  "fiebre": None}, # Conocemos la causa
    "Luis":   {"gripe": None,  "infeccion": False, "fiebre": True}, # Conocemos el síntoma y descartamos una causa
    "Carlos": {"gripe": None,  "infeccion": None,  "fiebre": True}  # Solo conocemos el síntoma
}



# --- 2. DEFINICIÓN DE REGLAS LÓGICAS EN 1ER ORDEN ---
def aplicar_regla_causal(nombre, estado):
    """
    REGLA CAUSAL: Modelamos la física del cuerpo (Causa -> Efecto).
    ∀x (Gripe(x) v Infeccion(x) => Fiebre(x))
    "Para todo x, si x tiene gripe o infección, entonces x desarrollará fiebre."
    """
    hubo_cambio = False
    # Si detectamos que la premisa (causa) es Verdadera...
    if estado["gripe"] is True or estado["infeccion"] is True:
        # ...y el efecto aún no está registrado o es desconocido:
        if estado["fiebre"] is not True:
            estado["fiebre"] = True
            print(f"  [Causal] PREVISIÓN: Deducimos que {nombre} desarrollará FIEBRE, provocado por su enfermedad.")
            hubo_cambio = True
    return hubo_cambio


def aplicar_regla_diagnostica(nombre, estado):
    """
    REGLA DIAGNÓSTICA: Modelamos el análisis deductivo (Efecto -> Causas Posibles).
    ∀x (Fiebre(x) => Gripe(x) v Infeccion(x))
    "Para todo x, si x tiene fiebre, entonces debe tener gripe o infección."
    """
    hubo_cambio = False
    # Si detectamos que la premisa (efecto/síntoma) es Verdadera...
    if estado["fiebre"] is True:
        # Utilizamos el Silogismo Disyuntivo: Si es A o B, y sabemos que no es B, entonces es A.
        if estado["infeccion"] is False and estado["gripe"] is None:
            estado["gripe"] = True
            print(f"  [Diagnóstico] DEDUCCIÓN: {nombre} tiene fiebre y NO tiene infección. Diagnosticamos GRIPE.")
            hubo_cambio = True
            
        elif estado["gripe"] is False and estado["infeccion"] is None:
            estado["infeccion"] = True
            print(f"  [Diagnóstico] DEDUCCIÓN: {nombre} tiene fiebre y NO tiene gripe. Diagnosticamos INFECCIÓN.")
            hubo_cambio = True
            
        elif estado["gripe"] is None and estado["infeccion"] is None:
            print(f"  [Diagnóstico] AMBIGÜEDAD: {nombre} tiene fiebre, pero podría ser gripe o infección. Faltan pruebas.")
            # No hay cambio en el estado porque no podemos afirmar nada con certeza.
    return hubo_cambio



# --- 3. MOTOR DE INFERENCIA CONTINUO ---
print("Iniciando ronda clínica de evaluación lógica...\n")
for nombre, estado in pacientes.items():
    print(f"Analizando a {nombre}:")
    # Aplicamos ambas reglas secuencialmente
    cambio_c = aplicar_regla_causal(nombre, estado)
    cambio_d = aplicar_regla_diagnostica(nombre, estado)
    # Si ninguna regla arrojó resultados nuevos y tampoco hubo ambigüedad reportada
    if not cambio_c and not cambio_d and estado["fiebre"] is not True:
         print("  No se pudo deducir nueva información.")
    print("-" * 50)



print("\n=== ESTADO FINAL DE LA BASE DE CONOCIMIENTO ===")
for nombre, estado in pacientes.items():
    print(f"{nombre}: {estado}")



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Asimetría de la Lógica: La regla causal predice estados futuros (Ana), mientras que la diagnóstica descubre estados ocultos (Luis).")
print("2. Manejo de Incertidumbre: Las reglas diagnósticas en lógica pura sufren de ambigüedad (Carlos). Si hay múltiples causas, la lógica formal se atasca a menos que se descarten opciones (Silogismo Disyuntivo).")
print("3. Evolución a Redes Bayesianas: Para resolver la ambigüedad de Carlos en la IA moderna, las reglas diagnósticas rígidas se reemplazan por probabilidades (Ej. 80% Gripe, 20% Infección).")