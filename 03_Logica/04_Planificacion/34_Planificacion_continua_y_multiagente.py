class EntornoCompartido:
    """
    Representa el mundo donde operan los agentes.
    Gestiona los recursos compartidos para evitar colisiones.
    """
    def __init__(self):
        # Simulamos un pasillo estrecho o zona de carga donde solo cabe un agente
        self.zona_carga_ocupada_por = None


    def solicitar_acceso_zona_carga(self, id_agente):
        """Intento de adquirir un bloqueo (lock) sobre el recurso compartido."""
        if self.zona_carga_ocupada_por is None:
            self.zona_carga_ocupada_por = id_agente
            return True
        elif self.zona_carga_ocupada_por == id_agente:
            return True # El agente ya tiene el control
        return False


    def liberar_zona_carga(self, id_agente):
        """Libera el recurso para que otros agentes puedan usarlo."""
        if self.zona_carga_ocupada_por == id_agente:
            self.zona_carga_ocupada_por = None



class AgenteContinuo:
    """
    Un agente autonomo que opera en un bucle infinito.
    Puede recibir metas dinamicamente y lidiar con interferencia de otros agentes.
    """
    def __init__(self, id_agente, entorno):
        self.id = id_agente
        self.entorno = entorno
        self.metas_pendientes = []
        self.plan_actual = []
        self.estado_interno = "INACTIVO"


    def recibir_nueva_meta(self, tarea):
        """Permite inyectar metas en tiempo de ejecucion (Planificacion Continua)."""
        self.metas_pendientes.append(tarea)
        print(f"[Agente {self.id}] Nueva meta recibida: '{tarea}'. Total en cola: {len(self.metas_pendientes)}")


    def planificar(self):
        """Genera un plan simple para la meta actual."""
        if not self.metas_pendientes:
            return


        meta_actual = self.metas_pendientes[0]
        print(f"[Agente {self.id}] Calculando plan para: '{meta_actual}'")
        

        # Un plan es una cola de acciones
        self.plan_actual = [
            {"accion": "navegar", "destino": "entrada_zona_carga"},
            {"accion": "solicitar_recurso"},
            {"accion": "cargar_paquete", "item": meta_actual},
            {"accion": "liberar_recurso"},
            {"accion": "entregar", "destino": "zona_descarga"}
        ]
        self.estado_interno = "EJECUTANDO"


    def ejecutar_ciclo(self):
        """
        Representa un 'tick' de tiempo para este agente.
        Entrelaza la planificacion, la vigilancia y la ejecucion.
        """
        # 1. Si no hay plan pero hay metas, debemos planificar
        if not self.plan_actual and self.metas_pendientes:
            self.planificar()


        # 2. Si despues de intentar planificar seguimos sin plan, no hay nada que hacer
        if not self.plan_actual:
            if self.estado_interno != "INACTIVO":
                self.estado_interno = "INACTIVO"
                print(f"[Agente {self.id}] En espera de nuevas ordenes.")
            return


        # 3. Extraemos la siguiente accion (Vigilancia de Ejecucion)
        paso_actual = self.plan_actual[0]
        tipo_accion = paso_actual["accion"]


        # 4. Evaluacion y Ejecucion de la accion
        if tipo_accion == "navegar" or tipo_accion == "entregar":
            print(f"[Agente {self.id}] Moviendose a {paso_actual['destino']}...")
            self.plan_actual.pop(0)


        elif tipo_accion == "solicitar_recurso":
            # Resolucion Multiagente: Intentamos adquirir el recurso exclusivo
            if self.entorno.solicitar_acceso_zona_carga(self.id):
                print(f"[Agente {self.id}] Acceso CONCEDIDO a la zona de carga.")
                self.plan_actual.pop(0)
            else:
                # El agente se detiene y espera (podria replanificar otra ruta en un sistema mas complejo)
                print(f"[Agente {self.id}] DENEGADO. Zona de carga ocupada. Esperando...")
                # No hacemos pop(), asi en el siguiente ciclo volvera a intentar


        elif tipo_accion == "cargar_paquete":
            print(f"[Agente {self.id}] Cargando {paso_actual['item']}...")
            self.plan_actual.pop(0)


        elif tipo_accion == "liberar_recurso":
            self.entorno.liberar_zona_carga(self.id)
            print(f"[Agente {self.id}] Zona de carga liberada para otros agentes.")
            self.plan_actual.pop(0)
            

            # Si esta era la ultima accion sustancial de la meta, la marcamos terminada
            if len(self.plan_actual) == 1 and self.plan_actual[0]["accion"] == "entregar":
                meta_cumplida = self.metas_pendientes.pop(0)
                print(f"[Agente {self.id}] Meta intermedia alcanzada: Recoleccion de '{meta_cumplida}' completada.")



# SIMULADOR DEL MUNDO (ORQUESTADOR)
def simular_entorno():
    print("___INICIANDO SISTEMA CONTINUO MULTIAGENTE___\n")
    entorno_compartido = EntornoCompartido()
    

    # Creamos dos agentes independientes operando en el mismo entorno
    agente_a = AgenteContinuo("A", entorno_compartido)
    agente_b = AgenteContinuo("B", entorno_compartido)


    # Inyectamos las metas iniciales
    agente_a.recibir_nueva_meta("Paquete_Urgente_1")
    agente_b.recibir_nueva_meta("Caja_Herramientas_2")
    print("\n___INICIANDO CICLOS DE RELOJ (TICKS)___")
    


    # Simulamos el bucle continuo del servidor central
    for tick in range(1, 10):
        print(f"\n[RELOJ] Tick de tiempo: {tick}")
        # En el tick 4, ocurre un evento inesperado: Entra un nuevo pedido urgente para el Agente A
        # Esto demuestra la capacidad de Planificacion Continua
        if tick == 4:
            print(">>> EVENTO EXTERNO: Ingresa nuevo pedido al sistema.")
            agente_a.recibir_nueva_meta("Suministros_Medicos_3")


        # Cada agente ejecuta su porcion de computo y accion fisica
        agente_a.ejecutar_ciclo()
        agente_b.ejecutar_ciclo()


if __name__ == "__main__":
    simular_entorno()