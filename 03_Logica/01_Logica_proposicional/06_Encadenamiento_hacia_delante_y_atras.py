print("=== ENCADENAMIENTO: HACIA ADELANTE Y HACIA ATRÁS ===\n")
# --- 1. DEFINICIÓN DE LA BASE DE CONOCIMIENTO (KB) ---
# Formato de las reglas: (Lista de premisas, Conclusión)
reglas = [
    (["Fiebre", "Tos"], "Infeccion_Respiratoria"),
    (["Infeccion_Respiratoria", "Dolor_Muscular"], "Gripe"),
    (["Gripe", "Cansancio_Extremo"], "Reposo_Obligatorio")
]




# Los hechos que observamos en nuestro entorno (o paciente)
hechos_iniciales = {"Fiebre", "Tos", "Dolor_Muscular", "Cansancio_Extremo"}




# --- 2. ENCADENAMIENTO HACIA ADELANTE (Forward Chaining) ---
def encadenamiento_hacia_adelante(reglas, hechos, objetivo):
    """
    Parte de los hechos iniciales y deduce nueva información iterativamente
    hasta encontrar el objetivo o quedarse sin reglas.
    """
    print(f"\n[INICIANDO FORWARD CHAINING] Objetivo: ¿{objetivo}?")
    hechos_conocidos = set(hechos)
    agenda = list(hechos) # Elementos por procesar
    



    while agenda:
        p = agenda.pop(0)
        print(f" -> Procesando hecho: {p}")
        if p == objetivo:
            print("    ¡Objetivo alcanzado durante el procesamiento!")
            return True
        for premisas, conclusion in reglas:
            # Si el hecho actual es parte de las premisas de esta regla
            if p in premisas:
                # Verificamos si ya conocemos TODAS las premisas necesarias
                if all(prem in hechos_conocidos for prem in premisas):
                    if conclusion not in hechos_conocidos:
                        print(f"    * DEDUCCIÓN: Como tenemos {premisas}, inferimos -> {conclusion}")
                        hechos_conocidos.add(conclusion)
                        agenda.append(conclusion)
                        
                        if conclusion == objetivo:
                            return True     
    return False



# --- 3. ENCADENAMIENTO HACIA ATRÁS (Backward Chaining) ---
def encadenamiento_hacia_atras(reglas, hechos, objetivo, nivel=0):
    """
    Parte del objetivo y busca recursivamente si las premisas necesarias
    para cumplirlo son hechos conocidos o pueden deducirse.
    """
    indent = "  " * nivel
    print(f"{indent}[BACKWARD] Verificando objetivo: {objetivo}")
    


    # Caso Base 1: El objetivo ya es un hecho observable
    if objetivo in hechos:
        print(f"{indent} -> ¡Hecho confirmado en la base de datos!")
        return True
        


    # Paso Recursivo: Buscamos qué reglas tienen como conclusión nuestro objetivo
    for premisas, conclusion in reglas:
        if conclusion == objetivo:
            print(f"{indent} -> Encontrada regla que concluye en '{objetivo}'. Requiere: {premisas}")
            # Verificamos si podemos probar TODAS las premisas necesarias
            todas_probadas = True
            for premisa in premisas:
                if not encadenamiento_hacia_atras(reglas, hechos, premisa, nivel + 1):
                    todas_probadas = False
                    break # Si una falla, esta regla no sirve (Cortocircuito lógico)
            if todas_probadas:
                print(f"{indent} -> Todas las premisas para '{objetivo}' fueron probadas.")
                return True
                


    # Caso Base 2: No hay reglas ni hechos que respalden el objetivo
    print(f"{indent} -> No se pudo probar '{objetivo}'.")
    return False




# --- 4. EJECUCIÓN Y COMPARACIÓN ---
meta = "Reposo_Obligatorio"
print("--- PRUEBA 1: HACIA ADELANTE (Data-Driven) ---")
resultado_fwd = encadenamiento_hacia_adelante(reglas, hechos_iniciales, meta)
print(f"Resultado FWD: {'ÉXITO' if resultado_fwd else 'FALLO'}\n")
print("-" * 60)
print("--- PRUEBA 2: HACIA ATRÁS (Goal-Driven) ---")
resultado_bwd = encadenamiento_hacia_atras(reglas, hechos_iniciales, meta)
print(f"\nResultado BWD: {'ÉXITO' if resultado_bwd else 'FALLO'}")



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Forward Chaining: Construye conocimiento ciegamente. Es ideal si hay pocos datos iniciales pero muchas conclusiones posibles (ej. Sistemas de monitoreo de red).")
print("2. Backward Chaining: Es un proceso enfocado. Es ideal cuando el objetivo está claro pero hay demasiados datos irrelevantes (ej. Diagnóstico médico o depuración de código).")
print("3. Estructura de Datos: Usar 'sets' de Python para los hechos garantiza búsquedas O(1), optimizando drásticamente el rendimiento.")