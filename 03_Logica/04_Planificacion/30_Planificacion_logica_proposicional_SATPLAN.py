import itertools
class SolverSATFuerzaBruta:
    """
    Un solucionador SAT basico.
    Evalua todas las combinaciones posibles de Verdadero/Falso para las variables
    buscando una que satisfaga todas las clausulas (Forma Normal Conjuntiva).
    """
    def resolver(self, variables, clausulas):
        n = len(variables)
        


        # itertools.product genera todas las combinaciones booleanas posibles (2^n)
        for combinacion in itertools.product([False, True], repeat=n):
            modelo = dict(zip(variables, combinacion))      
            todas_clausulas_satisfechas = True



            for clausula in clausulas:
                # Una clausula es una lista de literales unidos por OR
                # Un literal es una tupla: (nombre_variable, debe_ser_verdadera)
                clausula_satisfecha = False           
                for var, es_positiva in clausula:
                    valor_actual = modelo[var]
                    # Si el literal es positivo y la variable es True -> Satisfecho
                    # Si el literal es negativo y la variable es False -> Satisfecho
                    if (es_positiva and valor_actual) or (not es_positiva and not valor_actual):
                        clausula_satisfecha = True
                        break # Con un literal verdadero, todo el OR es verdadero              
                if not clausula_satisfecha:
                    todas_clausulas_satisfechas = False
                    break # Esta combinacion fallo, pasamos a la siguiente       
            if todas_clausulas_satisfechas:
                return modelo # Encontramos la interpretacion que hace cierta la formula 
        return None # Inconsistente (UNSAT)



class TraductorSATPLAN:
    """
    Traduce un problema de planificacion de 1 paso a Logica Proposicional (CNF).
    Problema: El robot empieza en R1. La meta es llegar a R2 en el instante 1.
    Accion disponible: Mover (de R1 a R2).
    """
    def __init__(self):
        # Definimos el diccionario de variables booleanas del sistema
        self.variables = ["R1_0", "R2_0", "Mover_0", "R1_1", "R2_1"]
        self.clausulas = []



    def generar_clausulas(self):
        # 1. ESTADO INICIAL (Tiempo 0)
        # El robot esta en R1 y no esta en R2.
        self.clausulas.append([("R1_0", True)])
        self.clausulas.append([("R2_0", False)])


        # 2. ESTADO META (Tiempo 1)
        # Queremos que el robot este en R2 en el instante 1.
        self.clausulas.append([("R2_1", True)])


        # 3. AXIOMAS DE ACCION
        # Regla: Si Mover_0 ocurre, requiere que R1_0 sea cierto.
        # Logica: Mover_0 -> R1_0  (CNF: NO Mover_0 O R1_0)
        self.clausulas.append([("Mover_0", False), ("R1_0", True)])
        

        # Regla: Si Mover_0 ocurre, el efecto es R2_1 cierto y R1_1 falso.
        # CNF: Mover_0 -> R2_1 => (NO Mover_0 O R2_1)
        self.clausulas.append([("Mover_0", False), ("R2_1", True)])
        # CNF: Mover_0 -> NO R1_1 => (NO Mover_0 O NO R1_1)
        self.clausulas.append([("Mover_0", False), ("R1_1", False)])


        # 4. AXIOMAS DE MARCO EXPLICATIVOS (Explanatory Frame Axioms)
        # Esto es vital en SATPLAN. Le dice a la logica por que cambian las cosas.
        # Sin esto, el motor SAT podria hacer trampa y cambiar variables por arte de magia.
        # Regla de R2: R2 en el instante 1 SOLO puede ser cierto si ya era cierto en 0, 
        # o si la accion Mover_0 lo hizo cierto.
        # CNF Derivado de: R2_1 -> (R2_0 O Mover_0)
        self.clausulas.append([("R2_1", False), ("R2_0", True), ("Mover_0", True)])
        

        # Regla de R1: R1 en el instante 1 SOLO puede ser cierto si era cierto en 0 
        # Y la accion Mover_0 NO ocurrio (porque Mover_0 elimina R1).
        # CNF Derivado de: R1_1 -> R1_0
        self.clausulas.append([("R1_1", False), ("R1_0", True)])
        # CNF Derivado de: R1_1 -> NO Mover_0
        self.clausulas.append([("R1_1", False), ("Mover_0", False)])
        return self.clausulas


# EJECUCION DE LA DEMOSTRACION
if __name__ == "__main__":
    print("___INICIANDO SATPLAN (Planificacion mediante Logica SAT)___")
    traductor = TraductorSATPLAN()
    clausulas_problema = traductor.generar_clausulas()
    


    print(f"Traduccion completa. Se generaron {len(clausulas_problema)} clausulas logicas.")
    print("Enviando formula CNF al Solver SAT...")
    solver = SolverSATFuerzaBruta()
    modelo_satisfactible = solver.resolver(traductor.variables, clausulas_problema)
    


    if modelo_satisfactible:
        print("RESULTADO SAT: ¡Formula Satisfactible!")
        print("\nExtrayendo plan de las variables verdaderas...")
        plan_encontrado = False
        for variable, valor in modelo_satisfactible.items():
            # Si es una variable de accion y es verdadera, es parte del plan
            if "Mover" in variable and valor is True:
                print(f" -> Ejecutar accion: {variable}")
                plan_encontrado = True
                


        if not plan_encontrado:
            print(" -> El plan es hacer nada (No-Op).")    
        print("\nEstado completo del universo en este modelo:")
        for var in sorted(modelo_satisfactible.keys()):
            estado_texto = "Verdadero" if modelo_satisfactible[var] else "Falso"
            print(f"  [{var}]: {estado_texto}")



    else:
        print("RESULTADO UNSAT: Formula Inconsistente.")
        print("El problema no se puede resolver en este horizonte de tiempo.")