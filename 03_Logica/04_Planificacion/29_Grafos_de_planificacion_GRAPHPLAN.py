class AccionGraphplan:
    """Representa una accion o un No-Op en el Grafo de Planificacion."""
    def __init__(self, nombre, pre, ef_add, ef_del):
        self.nombre = nombre
        self.pre = set(pre)
        self.ef_add = set(ef_add)
        self.ef_del = set(ef_del)



    def __repr__(self):
        return self.nombre



def detectar_mutex_acciones(a1, a2, mutex_props_previos):
    """Evalua las 3 reglas de Exclusion Mutua entre acciones."""
    # Regla 1: Efectos inconsistentes (Uno crea, otro destruye)
    if a1.ef_del.intersection(a2.ef_add) or a2.ef_del.intersection(a1.ef_add):
        return True
        


    # Regla 2: Interferencia (Uno destruye lo que el otro necesita para empezar)
    if a1.ef_del.intersection(a2.pre) or a2.ef_del.intersection(a1.pre):
        return True
        


    # Regla 3: Necesidades competitivas (Sus precondiciones son Mutex entre si)
    for p1 in a1.pre:
        for p2 in a2.pre:
            if (p1, p2) in mutex_props_previos or (p2, p1) in mutex_props_previos:
                return True          
    return False



def detectar_mutex_proposiciones(p1, p2, acciones_nivel, mutex_acciones_nivel):
    """
    Dos proposiciones son Mutex si TODAS las acciones que producen p1 
    son Mutex con TODAS las acciones que producen p2.
    """
    acciones_p1 = [a for a in acciones_nivel if p1 in a.ef_add]
    acciones_p2 = [a for a in acciones_nivel if p2 in a.ef_add]



    for a1 in acciones_p1:
        for a2 in acciones_p2:
            # Si encontramos al menos un par de acciones que producen estos hechos
            # y NO son Mutex, entonces las proposiciones pueden coexistir.
            if (a1, a2) not in mutex_acciones_nivel and (a2, a1) not in mutex_acciones_nivel:
                return False
    return True



class GrafoPlanificacion:
    """Motor de construccion del Grafo de Planificacion (Fase de Expansion)."""
    def __init__(self, acciones_base, estado_inicial):
        self.acciones_base = acciones_base
        self.niveles_p = [set(estado_inicial)] # P0
        self.niveles_a = []
        self.mutex_p = [{}] # Mutex en proposiciones por nivel
        self.mutex_a = []   # Mutex en acciones por nivel



    def expandir_nivel(self):
        """Avanza el grafo un nivel temporal (A_i y P_i+1)."""
        nivel_actual_idx = len(self.niveles_p) - 1
        props_actuales = self.niveles_p[-1]
        mutex_props_actuales = self.mutex_p[-1]



        # 1. Generar Nivel de Acciones (A_i)
        acciones_posibles = []
        


        # 1.1 Agregar acciones reales que cumplen sus precondiciones
        for accion in self.acciones_base:
            if accion.pre.issubset(props_actuales):
                # Verificar que las precondiciones no sean Mutex entre si
                pre_mutex = False
                for p1 in accion.pre:
                    for p2 in accion.pre:
                        if (p1, p2) in mutex_props_actuales:
                            pre_mutex = True
                if not pre_mutex:
                    acciones_posibles.append(accion)



        # 1.2 Agregar Acciones de Mantenimiento (No-Ops)
        for prop in props_actuales:
            acciones_posibles.append(
                AccionGraphplan(f"Mantener({prop})", [prop], [prop], [])
            )
        self.niveles_a.append(acciones_posibles)


        # 2. Calcular Mutex de Acciones en A_i
        mutex_acciones = set()
        for i in range(len(acciones_posibles)):
            for j in range(i + 1, len(acciones_posibles)):
                a1 = acciones_posibles[i]
                a2 = acciones_posibles[j]
                if detectar_mutex_acciones(a1, a2, mutex_props_actuales):
                    mutex_acciones.add((a1, a2))
        self.mutex_a.append(mutex_acciones)



        # 3. Generar Nivel de Proposiciones (P_i+1)
        nuevas_props = set()
        for accion in acciones_posibles:
            nuevas_props.update(accion.ef_add)  
        self.niveles_p.append(nuevas_props)



        # 4. Calcular Mutex de Proposiciones en P_i+1
        mutex_props_nuevas = set()
        props_list = list(nuevas_props)
        for i in range(len(props_list)):
            for j in range(i + 1, len(props_list)):
                p1 = props_list[i]
                p2 = props_list[j]
                if detectar_mutex_proposiciones(p1, p2, acciones_posibles, mutex_acciones):
                    mutex_props_nuevas.add((p1, p2))
        self.mutex_p.append(mutex_props_nuevas)



# DEMOSTRACION: EL PROBLEMA DEL PASTEL
if __name__ == "__main__":
    # Objetivo: Comerse un pastel, pero finalizar con un pastel en la mesa.
    # Pareciera imposible, a menos que horneemos uno nuevo despues (o durante).
    acciones_dominio = [
        AccionGraphplan("Comer_Pastel", 
                        pre=["tiene_pastel"], 
                        ef_add=["comio_pastel"], 
                        ef_del=["tiene_pastel"]),


        AccionGraphplan("Hornear_Pastel", 
                        pre=[], # Hornear no requiere precondiciones en este modelo
                        ef_add=["tiene_pastel"], 
                        ef_del=[])
    ]
    estado_inicial = ["tiene_pastel"]
    metas = {"tiene_pastel", "comio_pastel"}
    grafo = GrafoPlanificacion(acciones_dominio, estado_inicial)
    print("ANALISIS GRAPHPLAN: PROBLEMA DEL PASTEL")



    for paso in range(3):
        print(f"\n--- NIVEL TEMPORAL {paso} ---")
        # Mostramos Proposiciones y sus Mutex
        print(f"Proposiciones (P{paso}): {list(grafo.niveles_p[-1])}")
        mutex_p_format = [f"({p1} <X> {p2})" for p1, p2 in grafo.mutex_p[-1]]
        print(f"Mutex en Proposiciones: {mutex_p_format if mutex_p_format else 'Ninguno'}")



        # Verificamos si alcanzamos la meta
        if metas.issubset(grafo.niveles_p[-1]):
            # Verificamos que las metas no sean Mutex entre si en este nivel
            metas_son_mutex = False
            for m1 in metas:
                for m2 in metas:
                    if (m1, m2) in grafo.mutex_p[-1] or (m2, m1) in grafo.mutex_p[-1]:
                        metas_son_mutex = True
            


            if not metas_son_mutex:
                print("\n[!] CONDICION DE META ALCANZADA SIN CONFLICTOS MUTEX.")
                print("El algoritmo detiene la expansion y comenzaria la extraccion del plan hacia atras.")
                break
            else:
                print("\n[!] Meta presente, pero existe conflicto Mutex. Se requiere expandir el grafo.")



        # Expandimos el grafo si aun no llegamos (o si hay mutex)
        grafo.expandir_nivel()
        


        # Mostramos Acciones del nivel que acabamos de crear
        print(f"\nAcciones Posibles (A{paso}): {grafo.niveles_a[-1]}")
        mutex_a_format = []
        for a1, a2 in grafo.mutex_a[-1]:
            # Filtramos No-Ops triviales para la impresion limpia de la consola
            if not ("Mantener" in a1.nombre and "Mantener" in a2.nombre):
                mutex_a_format.append(f"({a1.nombre} <X> {a2.nombre})")
        print(f"Conflictos Mutex detectados en Acciones: {mutex_a_format}")