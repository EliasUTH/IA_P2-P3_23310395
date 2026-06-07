import copy
class Operador:
    """
    Representa una Tarea Primitiva.
    Son las unicas acciones que realmente alteran el estado del mundo.
    """
    def __init__(self, nombre, funcion_precondicion, funcion_efecto):
        self.nombre = nombre
        self.verificar_precondicion = funcion_precondicion
        self.aplicar_efecto = funcion_efecto


class Metodo:
    """
    Representa una 'Receta' para descomponer una Tarea Compuesta.
    Una misma tarea compuesta puede tener multiples metodos (ej. viajar en taxi o caminar),
    pero solo se elegira el que cumpla sus precondiciones.
    """
    def __init__(self, nombre, funcion_precondicion, subtareas):
        self.nombre = nombre
        self.verificar_precondicion = funcion_precondicion
        # Lista de nombres de tareas (pueden ser primitivas u otras compuestas)
        self.subtareas = subtareas


class PlanificadorHTN:
    """
    Motor de planificacion que descompone tareas jerarquicamente.
    """
    def __init__(self):
        self.operadores = {}
        # Un diccionario donde la clave es la Tarea Compuesta y el valor es una lista de Metodos
        self.metodos = {}


    def registrar_operador(self, operador):
        self.operadores[operador.nombre] = operador


    def registrar_metodo(self, tarea_compuesta, metodo):
        if tarea_compuesta not in self.metodos:
            self.metodos[tarea_compuesta] = []
        self.metodos[tarea_compuesta].append(metodo)


    def buscar_plan(self, estado, lista_tareas, plan_actual=None, nivel=0):
        """
        Algoritmo principal HTN (recursivo con backtracking).
        """
        if plan_actual is None:
            plan_actual = []
            print("Iniciando planificacion HTN...")
        sangria = "  " * nivel


        # Caso base: Si no quedan tareas en la lista, hemos terminado con exito
        if not lista_tareas:
            return plan_actual



        # Tomamos la primera tarea a procesar
        tarea_actual = lista_tareas[0]
        tareas_restantes = lista_tareas[1:]
        print(f"{sangria}Procesando tarea: '{tarea_actual}'")


        # CASO A: La tarea es Primitiva (Operador)
        if tarea_actual in self.operadores:
            operador = self.operadores[tarea_actual]
            

            # Verificamos si se puede ejecutar en el estado actual
            if operador.verificar_precondicion(estado):
                print(f"{sangria} -> Aplicando operador primitivo: {tarea_actual}")
                

                # Simulamos el cambio en el mundo
                nuevo_estado = copy.deepcopy(estado)
                operador.aplicar_efecto(nuevo_estado)
                

                # Agregamos la accion al plan y procesamos el resto
                nuevo_plan = plan_actual + [tarea_actual]
                resultado = self.buscar_plan(nuevo_estado, tareas_restantes, nuevo_plan, nivel + 1)
                if resultado is not None:
                    return resultado
            else:
                print(f"{sangria} -> FALLO: Precondiciones no cumplidas para {tarea_actual}")


        # CASO B: La tarea es Compuesta (Requiere un Metodo)
        elif tarea_actual in self.metodos:
            # Evaluamos todas las recetas disponibles para esta tarea
            for metodo in self.metodos[tarea_actual]:
                print(f"{sangria} -> Evaluando metodo: '{metodo.nombre}' para resolver '{tarea_actual}'")
                

                if metodo.verificar_precondicion(estado):
                    print(f"{sangria}    Metodo valido. Descomponiendo en: {metodo.subtareas}")
                    

                    # Reemplazamos la tarea actual por las subtareas del metodo
                    nueva_lista_tareas = metodo.subtareas + tareas_restantes
                    

                    # Intentamos resolver esta nueva lista de tareas
                    resultado = self.buscar_plan(estado, nueva_lista_tareas, plan_actual, nivel + 1)
                    

                    # Si la descomposicion tiene exito, devolvemos el plan
                    if resultado is not None:
                        return resultado


                    # Si falla en lo profundo, la recursion retrocede y probara el siguiente metodo
                else:
                    print(f"{sangria}    Metodo invalido por precondiciones del estado.")
        else:
            print(f"{sangria} -> ERROR: Tarea desconocida '{tarea_actual}'")
        # Si agotamos las opciones y no pudimos resolver la tarea, fracasamos en esta rama
        return None


# DEMOSTRACION: DOMINIO DE LOGISTICA Y TRANSPORTE
if __name__ == "__main__":
    planificador = PlanificadorHTN()
    

    # 1. Definimos las funciones de manipulacion del Estado del Mundo
    # Precondiciones y Efectos de Operadores (Tareas Primitivas)
    def pre_llamar_taxi(estado): return True
    def ef_llamar_taxi(estado): estado['taxi_esperando'] = True
    def pre_pagar_y_viajar(estado): return estado['taxi_esperando'] and estado['dinero'] >= 50
    def ef_pagar_y_viajar(estado):
        estado['dinero'] -= 50
        estado['ubicacion'] = 'centro'
        estado['taxi_esperando'] = False   
    def pre_caminar(estado): return True
    def ef_caminar(estado): estado['ubicacion'] = 'centro'


    # Registramos los Operadores
    planificador.registrar_operador(Operador("Accion_Llamar_Taxi", pre_llamar_taxi, ef_llamar_taxi))
    planificador.registrar_operador(Operador("Accion_Pagar_Viajar", pre_pagar_y_viajar, ef_pagar_y_viajar))
    planificador.registrar_operador(Operador("Accion_Caminar", pre_caminar, ef_caminar))



    # 2. Definimos las funciones de precondicion para los Metodos (Recetas de Tareas Compuestas)
    # Solo tomaremos taxi si la distancia es lejana
    def pre_metodo_viaje_largo(estado): return estado['distancia'] > 5 and estado['dinero'] >= 50
    # Solo caminaremos si la distancia es corta
    def pre_metodo_viaje_corto(estado): return estado['distancia'] <= 5



    # Registramos los Metodos para la tarea compuesta "Ir_Al_Centro"
    planificador.registrar_metodo(
        tarea_compuesta="Ir_Al_Centro",
        metodo=Metodo(
            nombre="Metodo_Taxi",
            funcion_precondicion=pre_metodo_viaje_largo,
            subtareas=["Accion_Llamar_Taxi", "Accion_Pagar_Viajar"]
        )
    )
    


    planificador.registrar_metodo(
        tarea_compuesta="Ir_Al_Centro",
        metodo=Metodo(
            nombre="Metodo_Caminata",
            funcion_precondicion=pre_metodo_viaje_corto,
            subtareas=["Accion_Caminar"]
        )
    )



    # 3. Definimos un estado inicial y la tarea de alto nivel a realizar
    estado_mundo = {
        'ubicacion': 'casa',
        'distancia': 10,  # Distancia de 10 kilometros (Viaje largo)
        'dinero': 100,    # Tenemos fondos suficientes
        'taxi_esperando': False
    }
    tareas_objetivo = ["Ir_Al_Centro"]
    print("ESTADO INICIAL:", estado_mundo)
    print("TAREAS A REALIZAR:", tareas_objetivo, "\n")

    
    # 4. Ejecutamos el planificador HTN
    plan_final = planificador.buscar_plan(estado_mundo, tareas_objetivo)
    

    if plan_final:
        print("\nPLAN ENCONTRADO (Solo contiene acciones primitivas ejecutables):")
        for i, accion in enumerate(plan_final, 1):
            print(f" Paso {i}: {accion}")
    else:
        print("No se encontro un plan valido para resolver las tareas.")