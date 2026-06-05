def mezclar_tramos(run1, run2):
    """Función auxiliar para mezclar dos listas ordenadas."""
    resultado = []
    i, j = 0, 0
    while i < len(run1) and j < len(run2):
        if run1[i] < run2[j]:
            resultado.append(run1[i])
            i += 1
        else:
            resultado.append(run2[j])
            j += 1
    resultado.extend(run1[i:])
    resultado.extend(run2[j:])
    return resultado



def polyphase_sort_corregido(arreglo):
    if len(arreglo) <= 1:
        return arreglo
    tramos = [[x] for x in arreglo]



    # Distribución inicial
    mitad = len(tramos) // 2 + 1
    cinta1 = tramos[:mitad]
    cinta2 = tramos[mitad:]
    cinta3 = []  
    fase = 1



    while len(cinta1) + len(cinta2) + len(cinta3) > 1:
        print(f"Fase {fase}: Cinta1={len(cinta1)} tramos, Cinta2={len(cinta2)} tramos, Cinta3={len(cinta3)} tramos")
        fase += 1      
        # --- SOLUCIÓN AL BUCLE INFINITO ---
        # Si dos cintas se quedan vacías, perdimos la sincronía de Fibonacci.
        # Forzamos la mezcla de los tramos restantes en la única cinta que tiene datos.
        vacios = sum(1 for c in [cinta1, cinta2, cinta3] if not c)
        if vacios == 2:
            print("   -> Sincronización perdida. Mezclando tramos restantes en la misma cinta...")
            # Encontramos la única cinta que no está vacía
            cinta_llena = next(c for c in [cinta1, cinta2, cinta3] if c)
            
            # Mezclamos todos los tramos de esa cinta entre sí
            while len(cinta_llena) > 1:
                run_a = cinta_llena.pop(0)
                run_b = cinta_llena.pop(0)
                cinta_llena.append(mezclar_tramos(run_a, run_b))
            break # Terminamos el algoritmo
        # -----------------------------------



        # Selección de cintas (cuál es la de salida)
        if not cinta3:
            entradas, salida = [cinta1, cinta2], cinta3
        elif not cinta1:
            entradas, salida = [cinta2, cinta3], cinta1
        else:
            entradas, salida = [cinta1, cinta3], cinta2



        # Mezclamos hasta vaciar una de las cintas de entrada
        while entradas[0] and entradas[1]:
            run_a = entradas[0].pop(0)
            run_b = entradas[1].pop(0)
            salida.append(mezclar_tramos(run_a, run_b))



    # Extraemos el resultado final
    for cinta in [cinta1, cinta2, cinta3]:
        if len(cinta) == 1:
            return cinta[0]



# --- Prueba del algoritmo ---
numeros_desordenados = [8, 4, 12, 5, 9, 1, 15, 3, 10, 7]
print(f"Lista original: {numeros_desordenados}\n")



numeros_ordenados = polyphase_sort_corregido(numeros_desordenados.copy())
print(f"\nLista ordenada: {numeros_ordenados}")