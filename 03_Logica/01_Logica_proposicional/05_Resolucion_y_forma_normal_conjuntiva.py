print("=== RESOLUCIÓN Y FORMA NORMAL CONJUNTIVA (CNF) ===\n")



# --- 1. FUNCIONES AUXILIARES ---
def complemento(literal):
    """
    Devuelve el opuesto lógico de un literal.
    Ejemplo: 'P' -> '-P',  '-P' -> 'P'
    """
    return literal[1:] if literal.startswith('-') else '-' + literal



# --- 2. MOTOR DE RESOLUCIÓN ---
def resolver(clausula1, clausula2):
    """
    Aplica la regla de resolución a dos cláusulas.
    Si encuentra un literal y su complemento (ej. 'P' y '-P'), los cancela
    y une el resto de los literales en una nueva cláusula.
    """
    resolventes = []
    


    for literal in clausula1:
        comp = complemento(literal)
        if comp in clausula2:
            # Eliminamos el literal y su complemento
            c1_limpia = clausula1 - {literal}
            c2_limpia = clausula2 - {comp}
            # Unimos el resto con un OR lógico (Unión de conjuntos)
            nueva_clausula = c1_limpia | c2_limpia
            # Descartamos tautologías triviales (ej. si la nueva cláusula tiene 'A' y '-A')
            if not any(complemento(l) in nueva_clausula for l in nueva_clausula):
                resolventes.append(nueva_clausula)   
    return resolventes



# --- 3. ALGORITMO PRINCIPAL DE DEMOSTRACIÓN ---
def demostracion_por_resolucion(kb_cnf, consulta_negada_cnf):
    """
    Demuestra si KB |= Consulta mediante Resolución por Refutación.
    Ambas entradas deben ser listas de conjuntos (representando la CNF).
    """
    # Juntamos la KB y la Consulta Negada
    clausulas = kb_cnf + consulta_negada_cnf
    print("Estado Inicial (KB AND NOT Consulta):")
    for i, c in enumerate(clausulas):
        print(f" C{i+1}: {c}")
    print("-" * 50)
    while True:
        n = len(clausulas)
        nuevos_resolventes = []
        # Comparamos todos los pares posibles de cláusulas
        for i in range(n):
            for j in range(i + 1, n):
                resultados = resolver(clausulas[i], clausulas[j])
                for res in resultados:
                    # Si llegamos a la cláusula vacía, encontramos una contradicción
                    if len(res) == 0:
                        print(f"\n[!] CONTRADICCIÓN ENCONTRADA (Cláusula vacía) [!]")
                        print(f"    Al resolver: {clausulas[i]} y {clausulas[j]}")
                        print("\n-> RESULTADO: La inferencia es VÁLIDA (Entailment comprobado).")
                        return True
                    nuevos_resolventes.append(res)



        # Revisamos si hemos descubierto nueva información
        agregado_nuevo = False
        for res in nuevos_resolventes:
            if res not in clausulas:
                clausulas.append(res)
                agregado_nuevo = True
                print(f"Nueva deducción: {res}")



        # Si tras comparar todo no hay nada nuevo, el ciclo termina
        if not agregado_nuevo:
            print("\nNo se pueden deducir más cláusulas. No hay contradicción.")
            print("-> RESULTADO: La inferencia es INVÁLIDA.")
            return False



# --- 4. EJECUCIÓN DEL ESCENARIO ---
# Escenario: 
# 1. Regla: Si llueve, hay humedad. (L => H)  ->  En CNF: {-L, H}
# 2. Hecho: Llueve. (L)                       ->  En CNF: {L}
# ---
# Queremos demostrar que: Hay humedad (H).
# Por tanto, la Consulta Negada es: No hay humedad (-H) -> En CNF: {-H}



base_conocimiento = [
    {'-L', 'H'}, # Cláusula 1: No llueve OR hay humedad
    {'L'}        # Cláusula 2: Llueve
]
consulta_negada = [
    {'-H'}       # Cláusula 3: Asumimos que NO hay humedad para buscar la contradicción
]



print("Intentando demostrar que 'H' (Hay humedad) es verdadero...\n")
demostracion_por_resolucion(base_conocimiento, consulta_negada)



print("\n=== ANÁLISIS TÉCNICO ===")
print("1. Regla de Inferencia: Basada en cancelar opuestos matemáticos.")
print("2. Cláusula Vacía: Ocurre al resolver, por ejemplo, {'H'} y {'-H'}. Representa lo absurdo.")
print("3. Conversión CNF: En este código asumimos que el texto ya fue convertido a CNF.")
print("   En sistemas reales (como solucionadores SAT), un módulo previo realiza la")
print("   transformación algebraica de las oraciones lógicas a esta forma de conjuntos.")