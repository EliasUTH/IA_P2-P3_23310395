print("=== IA MEDICA: INDEPENDENCIA CONDICIONAL ===\n")

# Vamos a crear una base de datos de 200 pacientes.
# Cada paciente es un diccionario con 3 datos: ¿Tiene Resfriado?, ¿Tiene Tos?, ¿Tiene Fiebre?
pacientes = []

# --- 1. Pacientes CON Resfriado (100 pacientes) ---
# Diseñados para que P(Tos) = 80% y P(Fiebre) = 50%
pacientes.extend([{"Resfriado": True, "Tos": True, "Fiebre": True}] * 40)
pacientes.extend([{"Resfriado": True, "Tos": True, "Fiebre": False}] * 40)
pacientes.extend([{"Resfriado": True, "Tos": False, "Fiebre": True}] * 10)
pacientes.extend([{"Resfriado": True, "Tos": False, "Fiebre": False}] * 10)

# --- 2. Pacientes SIN Resfriado (100 pacientes) ---
pacientes.extend([{"Resfriado": False, "Tos": True, "Fiebre": True}] * 5)
pacientes.extend([{"Resfriado": False, "Tos": True, "Fiebre": False}] * 5)
pacientes.extend([{"Resfriado": False, "Tos": False, "Fiebre": True}] * 5)
pacientes.extend([{"Resfriado": False, "Tos": False, "Fiebre": False}] * 85)

total_pacientes = len(pacientes)

# Funciones de ayuda para contar probabilidades
def probabilidad(condicion):
    casos_favorables = sum(1 for p in pacientes if condicion(p))
    return casos_favorables / total_pacientes

def probabilidad_dado_que(condicion_A, condicion_B):
    pacientes_B = [p for p in pacientes if condicion_B(p)]
    casos_A_y_B = sum(1 for p in pacientes_B if condicion_A(p))
    return casos_A_y_B / len(pacientes_B)

# --- PRUEBA 1: ¿Son independientes de forma general? (Marginalmente) ---
print("--- PRUEBA 1: DEPENDENCIA GENERAL (Población Total) ---")
# Matemáticamente, A y B son independientes si P(A y B) == P(A) * P(B)

prob_tos = probabilidad(lambda p: p["Tos"] == True)
prob_fiebre = probabilidad(lambda p: p["Fiebre"] == True)
prob_tos_y_fiebre = probabilidad(lambda p: p["Tos"] == True and p["Fiebre"] == True)

print(f"P(Tos): {prob_tos}")
print(f"P(Fiebre): {prob_fiebre}")
print(f"P(Tos) * P(Fiebre) calculado: {prob_tos * prob_fiebre:.3f}")
print(f"P(Tos Y Fiebre) real en los datos: {prob_tos_y_fiebre:.3f}")

if prob_tos * prob_fiebre != prob_tos_y_fiebre:
    print("-> CONCLUSIÓN 1: ¡NO son independientes! En la población general, si tienes tos es más probable que tengas fiebre.\n")

# --- PRUEBA 2: ¿Son independientes DADO QUE tienen resfriado? (Independencia Condicional) ---
print("--- PRUEBA 2: INDEPENDENCIA CONDICIONAL (Solo pacientes con Resfriado) ---")
# Matemáticamente, son independientes dado C si P(A y B | C) == P(A | C) * P(B | C)

prob_tos_dado_resfriado = probabilidad_dado_que(lambda p: p["Tos"] == True, lambda p: p["Resfriado"] == True)
prob_fiebre_dado_resfriado = probabilidad_dado_que(lambda p: p["Fiebre"] == True, lambda p: p["Resfriado"] == True)
prob_ambos_dado_resfriado = probabilidad_dado_que(lambda p: p["Tos"] == True and p["Fiebre"] == True, lambda p: p["Resfriado"] == True)

print(f"P(Tos | Resfriado): {prob_tos_dado_resfriado}")
print(f"P(Fiebre | Resfriado): {prob_fiebre_dado_resfriado}")
print(f"Multiplicación P(Tos|R) * P(Fiebre|R): {prob_tos_dado_resfriado * prob_fiebre_dado_resfriado:.3f}")
print(f"Probabilidad real de (Tos Y Fiebre | Resfriado): {prob_ambos_dado_resfriado:.3f}")

if prob_tos_dado_resfriado * prob_fiebre_dado_resfriado == prob_ambos_dado_resfriado:
    print("-> CONCLUSIÓN 2: ¡SON CONDICIONALMENTE INDEPENDIENTES! Al saber que el paciente tiene resfriado, los síntomas ya no se influyen entre sí.")