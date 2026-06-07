from collections import deque
import copy


class Accion:
    """Representa una accion basica del dominio."""
    def __init__(self, nombre, precondiciones, efectos):
        self.nombre = nombre
        self.precondiciones = precondiciones
        self.efectos = efectos


    def precondiciones_cumplidas(self, estado):
        for clave, valor in self.precondiciones.items():
            if estado.get(clave) != valor:
                return False
        return True


def planificador_bfs(estado_inicial, metas, acciones):
    """
    Planificador basico de busqueda en amplitud para encontrar el camino mas corto.
    """
    cola = deque([(estado_inicial, [])])
    visitados = []



    while cola:
        estado_actual, plan_actual = cola.popleft()
        # Comprobar si se alcanzo la meta
        meta_alcanzada = True
        for clave, valor in metas.items():
            if estado_actual.get(clave) != valor:
                meta_alcanzada = False
                break  
        if meta_alcanzada:
            return plan_actual


        # Evitar bucles
        estado_str = str(sorted(estado_actual.items()))
        if estado_str in visitados:
            continue
        visitados.append(estado_str)


        # Generar sucesores
        for accion in acciones:
            if accion.precondiciones_cumplidas(estado_actual):
                nuevo_estado = copy.deepcopy(estado_actual)
                nuevo_estado.update(accion.efectos)      
                nuevo_plan = list(plan_actual)
                nuevo_plan.append(accion)
                cola.append((nuevo_estado, nuevo_plan))     
    return None # No hay plan posible



class EntornoSimulado:
    """
    Representa el mundo real, el cual puede cambiar de forma impredecible.
    """
    def __init__(self, estado_inicial):
        self.estado_fisico = copy.deepcopy(estado_inicial)


    def ejecutar_accion(self, accion):
        """Aplica la accion al mundo fisico real."""
        self.estado_fisico.update(accion.efectos)


    def alterar_entorno(self, alteraciones):
        """Simula un evento externo (ej. alguien cierra una puerta)."""
        self.estado_fisico.update(alteraciones)


    def leer_sensores(self):
        """Devuelve el estado actual del mundo fisico."""
        return copy.deepcopy(self.estado_fisico)



class AgenteAutonomo:
    """
    Agente que planifica, vigila la ejecucion y replanifica si es necesario.
    """
    def __init__(self, acciones, metas):
        self.acciones = acciones
        self.metas = metas
        self.plan_actual = []


    def ejecutar_y_vigilar(self, entorno):
        print("--- INICIANDO OPERACION DEL AGENTE ---")
        


        # 1. Primera lectura de sensores y planificacion inicial
        estado_creencia = entorno.leer_sensores()
        print("Estado inicial percibido:", estado_creencia)
        self.plan_actual = planificador_bfs(estado_creencia, self.metas, self.acciones)
        

        if not self.plan_actual:
            print("Error: No existe un plan inicial posible.")
            return



        paso = 1
        # Bucle principal de ejecucion
        while self.plan_actual:
            # Extraemos la siguiente accion del plan
            accion_siguiente = self.plan_actual.pop(0)
            

            # VIGILANCIA DE EJECUCION: Leemos los sensores ANTES de actuar
            estado_real = entorno.leer_sensores()
            print(f"\n[Paso {paso}] Intentando ejecutar: {accion_siguiente.nombre}")
            

            # Verificamos si la accion sigue siendo valida en el mundo real
            if not accion_siguiente.precondiciones_cumplidas(estado_real):
                print("ALERTA DE VIGILANCIA: El entorno ha cambiado.")
                print("Las precondiciones para la accion ya no se cumplen.")
                print("Estado detectado:", estado_real)
                print("Abortando plan actual. Iniciando REPLANIFICACION...")
                # REPLANIFICACION: Calculamos un nuevo plan desde el estado alterado
                self.plan_actual = planificador_bfs(estado_real, self.metas, self.acciones)
                if self.plan_actual:
                    print("Replanificacion exitosa. Nuevo plan calculado.")
                    # No incrementamos el paso, volvemos a evaluar el bucle con el nuevo plan
                    continue 
                else:
                    print("Fallo critico: Imposible replanificar. Meta inalcanzable.")
                    return
            

            # Si la vigilancia es exitosa, ejecutamos la accion en el mundo fisico
            entorno.ejecutar_accion(accion_siguiente)
            print(f"Accion ejecutada con exito.")
            paso += 1


        # Verificacion final
        estado_final = entorno.leer_sensores()
        meta_cumplida = all(estado_final.get(k) == v for k, v in self.metas.items())
        if meta_cumplida:
            print("\nOPERACION COMPLETADA EXITOSAMENTE. Meta alcanzada.")
        else:
            print("\nOPERACION FINALIZADA CON ERRORES. Meta no alcanzada.")



# DEMOSTRACION: EL ROBOT DE MENSAJERIA
if __name__ == "__main__":
    # Definicion del dominio
    acciones_dominio = [
        Accion("Mover_A_Pasillo", 
               precondiciones={"posicion": "sala_origen", "puerta_abierta": True}, 
               efectos={"posicion": "pasillo"}),


        Accion("Mover_A_Destino", 
               precondiciones={"posicion": "pasillo"}, 
               efectos={"posicion": "sala_destino"}),


        Accion("Abrir_Puerta", 
               precondiciones={"posicion": "sala_origen", "puerta_abierta": False}, 
               efectos={"puerta_abierta": True}),


        Accion("Entregar_Paquete", 
               precondiciones={"posicion": "sala_destino", "tiene_paquete": True}, 
               efectos={"tiene_paquete": False, "paquete_entregado": True})
    ]


    estado_inicial = {
        "posicion": "sala_origen",
        "puerta_abierta": True, # Al principio, la puerta esta abierta
        "tiene_paquete": True,
        "paquete_entregado": False
    }


    metas_objetivo = {
        "paquete_entregado": True
    }



    # Inicializamos los sistemas
    mundo_real = EntornoSimulado(estado_inicial)
    robot = AgenteAutonomo(acciones_dominio, metas_objetivo)



    # Modificamos el codigo ligeramente aqui para simular un evento externo
    # En un entorno de produccion, estos eventos sucederian asincronamente
    print("___SIMULACION DE VIGILANCIA Y REPLANIFICACION___")

    


    # Mostramos el plan inicial que el robot tiene en mente antes de empezar
    plan_teorico = planificador_bfs(estado_inicial, metas_objetivo, acciones_dominio)
    print("Plan original calculado por el agente:")
    for a in plan_teorico:
        print(" -", a.nombre)
    print("\n")



    # Inyectamos una trampa en la simulacion: 
    # Justo antes de que el agente ejecute su bucle, alguien le cierra la puerta.
    # El agente no lo sabe aun, su plan asume que la puerta esta abierta.
    print("[SIMULADOR] Evento externo: Una rafaga de viento cierra la puerta.")
    mundo_real.alterar_entorno({"puerta_abierta": False})
    print("\n")
    # Ejecucion del agente
    robot.ejecutar_y_vigilar(mundo_real)