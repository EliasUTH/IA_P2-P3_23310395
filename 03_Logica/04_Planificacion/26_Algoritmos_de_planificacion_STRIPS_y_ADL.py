from collections import deque
class Accion:
    """
    Define una accion que el agente puede realizar.
    Soporta la estructura basica de STRIPS y la extension de precondiciones negativas de ADL.
    """
    def __init__(self, nombre, pre_pos=None, pre_neg=None, ef_add=None, ef_del=None):
        self.nombre = nombre
        # Precondiciones positivas (STRIPS/ADL): Deben estar en el estado actual
        self.pre_pos = set(pre_pos) if pre_pos else set()
        # Precondiciones negativas (Solo ADL): NO deben estar en el estado actual
        self.pre_neg = set(pre_neg) if pre_neg else set()
        # Efectos de Adicion: Hechos que se vuelven verdaderos
        self.ef_add = set(ef_add) if ef_add else set()
        # Efectos de Eliminacion: Hechos que se vuelven falsos
        self.ef_del = set(ef_del) if ef_del else set()



    def es_aplicable(self, estado_actual):
        """Verifica si la accion se puede ejecutar en el estado dado."""
        # Verificacion STRIPS: Todas las precondiciones positivas deben cumplirse
        if not self.pre_pos.issubset(estado_actual):
            return False


        # Verificacion ADL: Ninguna precondicion negativa debe estar en el estado
        if len(self.pre_neg.intersection(estado_actual)) > 0:
            return False  
        return True



    def aplicar(self, estado_actual):
        """Devuelve un nuevo estado tras aplicar los efectos de la accion."""
        nuevo_estado = set(estado_actual)
        # Primero se eliminan los efectos negativos (Lista Delete)
        nuevo_estado.difference_update(self.ef_del)
        # Luego se agregan los efectos positivos (Lista Add)
        nuevo_estado.update(self.ef_add)
        return nuevo_estado


class Planificador:
    """
    Busca una secuencia de acciones para llegar del estado inicial a la meta.
    """
    def __init__(self, acciones):
        self.acciones = acciones


    def buscar_plan(self, estado_inicial, metas_pos, metas_neg=None):
        """
        Algoritmo de busqueda en amplitud (BFS) para garantizar el plan mas corto.
        """
        metas_pos = set(metas_pos)
        metas_neg = set(metas_neg) if metas_neg else set()
        


        # La cola almacena tuplas: (estado_actual, camino_de_acciones_para_llegar)
        cola = deque([(set(estado_inicial), [])])
        estados_visitados = []


        print(f"Buscando plan...")
        print(f"Estado Inicial: {estado_inicial}")
        print(f"Metas a cumplir: Positivas {list(metas_pos)} | Negativas {list(metas_neg)}")


        while cola:
            estado_actual, plan_actual = cola.popleft()
            # Verificamos si el estado actual cumple con todas las metas
            cumple_metas_pos = metas_pos.issubset(estado_actual)
            cumple_metas_neg = len(metas_neg.intersection(estado_actual)) == 0
            if cumple_metas_pos and cumple_metas_neg:
                return plan_actual


            # Evitar ciclos infinitos ignorando estados ya evaluados
            # Convertimos el set a frozenset para poder buscarlo en la lista de visitados
            estado_congelado = frozenset(estado_actual)
            if estado_congelado in estados_visitados:
                continue
            estados_visitados.append(estado_congelado)


            # Generar nuevos estados aplicando todas las acciones posibles
            for accion in self.acciones:
                if accion.es_aplicable(estado_actual):
                    nuevo_estado = accion.aplicar(estado_actual)
                    nuevo_plan = list(plan_actual)
                    nuevo_plan.append(accion.nombre)
                    cola.append((nuevo_estado, nuevo_plan))
        return None # No se encontro ningun plan


# DEMOSTRACION DEL SISTEMA
if __name__ == "__main__":
    # --- ESCENARIO 1: PLANIFICACION STRIPS PURO ---
    # Problema: Un robot en la habitacion A debe ir a la habitacion B y tomar una caja.
    print("___DEMOSTRACION 1: MODELO STRIPS (Sin negaciones)___")
    

    acciones_strips = [
        Accion(nombre="Mover_A_B", 
               pre_pos=["robot_en_A"], 
               ef_add=["robot_en_B"], 
               ef_del=["robot_en_A"]),


        Accion(nombre="Tomar_Caja_B", 
               pre_pos=["robot_en_B", "caja_en_B"], 
               ef_add=["caja_tomada"], 
               ef_del=["caja_en_B"])
    ]
    

    planificador_1 = Planificador(acciones_strips)
    estado_inicio_1 = ["robot_en_A", "caja_en_B"]
    metas_1 = ["caja_tomada"] # Solo requiere proposiciones positivas
    plan_resultado_1 = planificador_1.buscar_plan(estado_inicio_1, metas_pos=metas_1)
    

    if plan_resultado_1:
        print("\nPlan encontrado (STRIPS):")
        for i, paso in enumerate(plan_resultado_1):
            print(f" Paso {i+1}: {paso}")
    else:
        print("\nNo se encontro solucion.")



    # --- ESCENARIO 2: PLANIFICACION ADL ---
    # Problema: El robot necesita desarmar una bomba. 
    # Solo puede hacerlo SI NO esta lloviendo (porque el circuito se daña).
    # STRIPS no podria modelar "si no llueve" facilmente sin crear variables extrañas. ADL si.
    print("___DEMOSTRACION 2: MODELO ADL (Uso de precondiciones negativas)___")

    

    acciones_adl = [
        Accion(nombre="Abrir_Paraguas",
               pre_pos=["tiene_paraguas"],
               ef_add=["paraguas_abierto"],
               ef_del=["tiene_paraguas"]),


        Accion(nombre="Desarmar_Bomba",
               pre_pos=["frente_a_bomba"],
               # AQUI ESTA ADL: Exigimos explicitamente que la proposicion 'lloviendo' sea falsa
               pre_neg=["lloviendo"], 
               ef_add=["bomba_desarmada"],
               ef_del=["frente_a_bomba"]),


        # Accion para cubrir la bomba y aislarla de la lluvia
        Accion(nombre="Cubrir_Bomba_Con_Paraguas",
               pre_pos=["frente_a_bomba", "paraguas_abierto"],
               ef_add=[],
               ef_del=["lloviendo"]) # El efecto hace que "lloviendo" (sobre la bomba) deje de ser cierto
    ]
    planificador_2 = Planificador(acciones_adl)
    

    # El estado inicial dicta que SI esta lloviendo
    estado_inicio_2 = ["frente_a_bomba", "lloviendo", "tiene_paraguas"]
    metas_2_pos = ["bomba_desarmada"]
    

    plan_resultado_2 = planificador_2.buscar_plan(
        estado_inicio_2, 
        metas_pos=metas_2_pos
    )
    

    if plan_resultado_2:
        print("\nPlan encontrado (ADL):")
        for i, paso in enumerate(plan_resultado_2):
            print(f" Paso {i+1}: {paso}")
    else:
        print("\nNo se encontro solucion.")