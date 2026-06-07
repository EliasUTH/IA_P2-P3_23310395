import copy
class AccionNormal:
    """
    Accion estandar que altera fisicamente el estado del mundo.
    Representa los nodos OR en el arbol de busqueda.
    """
    def __init__(self, nombre, precondiciones, efectos):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.efectos = efectos
    def es_aplicable(self, estado):
        for var, valor in self.precondiciones.items():
            if estado.get(var) != valor:
                return False
        return True
    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        nuevo_estado.update(self.efectos)
        return nuevo_estado



class AccionObservacion:
    """
    Accion que no cambia el mundo, sino que cambia el "Estado de Creencia" del agente.
    Representa los nodos AND en el arbol de busqueda. Obliga a crear ramas condicionales.
    """
    def __init__(self, nombre, precondiciones, variable_observada):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.variable_observada = variable_observada



    def es_aplicable(self, estado):
        for var, valor in self.precondiciones.items():
            if estado.get(var) != valor:
                return False
        # Solo tiene sentido gastar tiempo observando si la variable es desconocida
        return estado.get(self.variable_observada) == "desconocido"



    def observar(self, estado):
        """
        Al observar una variable desconocida, la realidad colapsa en dos posibles 
        estados de creencia mutuamente excluyentes.
        """
        estado_verdadero = copy.deepcopy(estado)
        estado_verdadero[self.variable_observada] = True
        
        estado_falso = copy.deepcopy(estado)
        estado_falso[self.variable_observada] = False
        
        return estado_verdadero, estado_falso



class PlanificadorCondicional:
    def __init__(self, acciones, observaciones):
        self.acciones = acciones
        self.observaciones = observaciones



    def estado_es_meta(self, estado, metas):
        for var, valor in metas.items():
            if estado.get(var) != valor:
                return False
        return True



    def congelar_estado(self, estado):
        """Convierte el diccionario en un string inmutable para guardar historiales."""
        return str(sorted(estado.items()))



    def buscar_plan(self, estado_creencia, metas, historial=None):
        """
        Algoritmo recursivo de busqueda AND-OR.
        Busca un plan garantizado que alcance la meta sin importar lo que dicten los sensores.
        """
        if historial is None:
            historial = set()


        # Condicion de victoria para esta rama
        if self.estado_es_meta(estado_creencia, metas):
            return "Meta_Alcanzada"


        # Deteccion de ciclos para evitar bucles infinitos
        hash_estado = self.congelar_estado(estado_creencia)
        if hash_estado in historial:
            return None
        historial.add(hash_estado)



        # 1. EXPANSION DE NODOS OR (Probar acciones fisicas normales)
        for accion in self.acciones:
            if accion.es_aplicable(estado_creencia):
                nuevo_estado = accion.aplicar(estado_creencia)
                sub_plan = self.buscar_plan(nuevo_estado, metas, copy.deepcopy(historial))
                

                # Si la accion conduce a la meta, devolvemos este paso
                if sub_plan is not None:
                    return {"tipo": "accion", "nombre": accion.nombre, "siguiente": sub_plan}



        # 2. EXPANSION DE NODOS AND (Probar acciones de sensor)
        for observacion in self.observaciones:
            if observacion.es_aplicable(estado_creencia):
                # Generamos los dos mundos posibles
                estado_v, estado_f = observacion.observar(estado_creencia)
                

                # REQUISITO AND: El plan DEBE resolver ambos universos posibles
                plan_rama_verdadera = self.buscar_plan(estado_v, metas, copy.deepcopy(historial))
                

                if plan_rama_verdadera is not None:
                    plan_rama_falsa = self.buscar_plan(estado_f, metas, copy.deepcopy(historial))
                    

                    if plan_rama_falsa is not None:
                        # Si ambas ramas son resolubles, construimos el bloque condicional
                        return {
                            "tipo": "condicion",
                            "accion_sensor": observacion.nombre,
                            "variable": observacion.variable_observada,
                            "caso_verdadero": plan_rama_verdadera,
                            "caso_falso": plan_rama_falsa
                        }
        # Si llegamos aqui, significa que es un callejon sin salida absoluto
        return None



def imprimir_arbol_plan(plan, nivel=0):
    """Funcion auxiliar para imprimir el diccionario del plan como un codigo legible."""
    sangria = "    " * nivel
    if plan == "Meta_Alcanzada":
        print(f"{sangria}[Exito: Objetivo Cumplido]")
    elif plan["tipo"] == "accion":
        print(f"{sangria}EJECUTAR: {plan['nombre']}")
        imprimir_arbol_plan(plan["siguiente"], nivel)
    elif plan["tipo"] == "condicion":
        print(f"{sangria}OBSERVAR SENSOR: {plan['accion_sensor']} -> ¿'{plan['variable']}' es True?")
        print(f"{sangria}SI ES VERDADERO:")
        imprimir_arbol_plan(plan["caso_verdadero"], nivel + 1)
        print(f"{sangria}SI ES FALSO:")
        imprimir_arbol_plan(plan["caso_falso"], nivel + 1)



# DEMOSTRACION: EL ROBOT EXPLORADOR Y LA PUERTA
if __name__ == "__main__":
    # PROBLEMA: Un robot debe llegar a la sala de control.
    # En el medio hay una puerta. El robot no sabe si esta cerrada con llave o no.
    # Tiene una llave que puede usar si es necesario.
    acciones_dominio = [
        AccionNormal("Avanzar_hacia_Puerta", 
                     precondiciones={"posicion": "inicio"}, 
                     efectos={"posicion": "frente_a_puerta"}),                 
        AccionNormal("Cruzar_Puerta", 
                     precondiciones={"posicion": "frente_a_puerta", "puerta_bloqueada": False}, 
                     efectos={"posicion": "sala_control"}),                
        AccionNormal("Usar_Llave_Maestra", 
                     precondiciones={"posicion": "frente_a_puerta", "puerta_bloqueada": True}, 
                     efectos={"puerta_bloqueada": False})
    ]
    


    sensores_dominio = [
        AccionObservacion("Escanear_Cerradura", 
                          precondiciones={"posicion": "frente_a_puerta"}, 
                          variable_observada="puerta_bloqueada")
    ]
    


    # El estado inicial dicta que la posicion actual es el inicio, 
    # pero el estado de la puerta es estrictamente "desconocido".
    estado_creencia_inicial = {
        "posicion": "inicio",
        "puerta_bloqueada": "desconocido"
    }
    metas_objetivo = {
        "posicion": "sala_control"
    }
    


    planificador = PlanificadorCondicional(acciones_dominio, sensores_dominio)
    print("GENERANDO PLAN CONDICIONAL DE CONTINGENCIA")
    plan_resultante = planificador.buscar_plan(estado_creencia_inicial, metas_objetivo)
    if plan_resultante:
        print("Plan Garantizado Encontrado. Arbol de ejecucion:")
        imprimir_arbol_plan(plan_resultante)
    else:
        print("No se encontro ningun plan que garantice el exito bajo toda contingencia.")