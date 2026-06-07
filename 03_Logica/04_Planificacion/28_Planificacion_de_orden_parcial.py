from collections import defaultdict
class PlanOrdenParcial:
    """
    Representa un plan como un conjunto de restricciones temporales y causales,
    sin forzar un orden lineal estricto a menos que sea necesario.
    """
    def __init__(self):
        self.pasos = set()
        self.restricciones_orden = set() # Tuplas (Paso_A, Paso_B) donde A < B
        self.enlaces_causales = set()    # Tuplas (Proveedor, Condicion, Consumidor)



    def agregar_paso(self, nombre_paso):
        """Agrega una accion al plan."""
        self.pasos.add(nombre_paso)



    def agregar_restriccion(self, paso_anterior, paso_posterior):
        """Impone que un paso debe ejecutarse estrictamente antes que otro."""
        self.restricciones_orden.add((paso_anterior, paso_posterior))



    def agregar_enlace_causal(self, proveedor, condicion, consumidor):
        """
        Registra que el 'proveedor' genera el estado 'condicion' que necesita el 'consumidor'.
        Esto añade implicitamente una restriccion de orden temporal.
        """
        self.enlaces_causales.add((proveedor, condicion, consumidor))
        self.agregar_restriccion(proveedor, consumidor)


    def es_plan_valido(self):
        """
        Un plan de orden parcial es invalido si sus restricciones de orden
        forman un ciclo (ej. A debe ir antes que B, y B antes que A).
        """
        # Construimos un grafo dirigido a partir de las restricciones
        grafo = defaultdict(list)
        for antes, despues in self.restricciones_orden:
            grafo[antes].append(despues)
        visitados = set()
        pila_recursion = set()


        def detectar_ciclo(nodo):
            visitados.add(nodo)
            pila_recursion.add(nodo)
            for vecino in grafo.get(nodo, []):
                if vecino not in visitados:
                    if detectar_ciclo(vecino):
                        return True
                elif vecino in pila_recursion:
                    return True
            pila_recursion.remove(nodo)
            return False


        for paso in self.pasos:
            if paso not in visitados:
                if detectar_ciclo(paso):
                    return False # Se detecto un ciclo de dependencia temporal
        return True


    def generar_ordenes_totales(self):
        """
        Genera todas las secuencias de ejecucion lineales (Ordenes Totales)
        que respetan el Plan de Orden Parcial usando Ordenamiento Topologico.
        Demuestra la flexibilidad del Principio de Minimo Compromiso.
        """
        grafo = defaultdict(list)
        grados_entrada = {paso: 0 for paso in self.pasos}


        for antes, despues in self.restricciones_orden:
            grafo[antes].append(despues)
            grados_entrada[despues] += 1
        ordenes_encontrados = []


        def backtracking_topologico(camino_actual, grados):
            # Si el camino tiene todos los pasos, encontramos un orden total valido
            if len(camino_actual) == len(self.pasos):
                ordenes_encontrados.append(list(camino_actual))
                return


            # Buscamos que pasos no tienen dependencias pendientes
            candidatos = [p for p in self.pasos if grados[p] == 0 and p not in camino_actual]


            for candidato in candidatos:
                camino_actual.append(candidato)
                # Al simular que tomamos este paso, reducimos el grado de sus dependientes
                for dependiente in grafo[candidato]:
                    grados[dependiente] -= 1

                backtracking_topologico(camino_actual, grados)


                # Deshacer cambios para probar la siguiente rama (Backtracking)
                camino_actual.pop()
                for dependiente in grafo[candidato]:
                    grados[dependiente] += 1
        backtracking_topologico([], grados_entrada.copy())
        return ordenes_encontrados



# DEMOSTRACION: EL PROBLEMA DE LOS ZAPATOS
if __name__ == "__main__":
    plan = PlanOrdenParcial()
    # 1. Definimos los pasos del plan
    pasos_requeridos = [
        "Inicio",
        "Poner_Calcetin_Izquierdo",
        "Poner_Zapato_Izquierdo",
        "Poner_Calcetin_Derecho",
        "Poner_Zapato_Derecho",
        "Fin"
    ]
    


    for p in pasos_requeridos:
        plan.agregar_paso(p)



    # 2. Definimos las restricciones estructurales basicas
    # Todo debe ocurrir despues de "Inicio" y antes de "Fin"
    for p in pasos_requeridos:
        if p != "Inicio":
            plan.agregar_restriccion("Inicio", p)
        if p != "Fin":
            plan.agregar_restriccion(p, "Fin")



    # 3. Construimos los enlaces causales (El trabajo real del Planificador POP)
    # Logica: No puedo poner el zapato izquierdo sin el calcetin izquierdo.
    plan.agregar_enlace_causal(
        proveedor="Poner_Calcetin_Izquierdo", 
        condicion="pie_izquierdo_cubierto", 
        consumidor="Poner_Zapato_Izquierdo"
    )
    plan.agregar_enlace_causal(
        proveedor="Poner_Calcetin_Derecho", 
        condicion="pie_derecho_cubierto", 
        consumidor="Poner_Zapato_Derecho"
    )



    # 4. Analizamos y mostramos los resultados
    print("___ANALISIS DEL PLAN DE ORDEN PARCIAL___")
    


    if plan.es_plan_valido():
        print("Estado del plan: VALIDO (No hay ciclos causales)")
        ordenes = plan.generar_ordenes_totales()
        print(f"\nSe encontraron {len(ordenes)} ordenes lineales validos para este plan:")
        


        for i, orden in enumerate(ordenes):
            # Omitimos Inicio y Fin para mayor claridad en la impresion
            orden_limpio = [paso for paso in orden if paso not in ("Inicio", "Fin")]
            print(f" Opcion {i+1}: {' -> '.join(orden_limpio)}")
    else:
        print("Estado del plan: INVALIDO (Ciclo temporal detectado)")