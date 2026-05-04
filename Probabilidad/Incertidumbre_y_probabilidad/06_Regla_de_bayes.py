print("=== CLASIFICADOR IA USANDO LA REGLA DE BAYES ===\n")

def regla_de_bayes(prior, verosimilitud, evidencia):
    """
    Calcula la probabilidad a posteriori usando la Regla de Bayes matemática pura.
    Fórmula: P(A|B) = ( P(B|A) * P(A) ) / P(B)
    
    :param prior: P(A) - Probabilidad inicial de la clase (ej. probabilidad de que sea Spam en general)
    :param verosimilitud: P(B|A) - Probabilidad de la evidencia dada la clase
    :param evidencia: P(B) - Probabilidad total de que ocurra la evidencia
    :return: P(A|B) - Probabilidad actualizada (Posterior)
    """
    posterior = (verosimilitud * prior) / evidencia
    return posterior

# --- ESCENARIO: FILTRO DE SPAM DE CORREOS ---
# Supongamos que nuestra IA ha leído miles de correos y extrajo estas estadísticas históricas:

# 1. Priors (Probabilidades iniciales)
prob_spam = 0.30       # P(Spam): El 30% de todos los correos que recibimos son Spam
prob_no_spam = 0.70    # P(No Spam): El 70% son correos legítimos (Ham)

# 2. Verosimilitud (Likelihood) de la palabra "Oferta"
# P(Oferta | Spam): Si sabemos que un correo es Spam, hay un 80% de probabilidad de que contenga la palabra "Oferta"
verosimilitud_oferta_dado_spam = 0.80  

# P(Oferta | No Spam): Si el correo es legítimo, solo hay un 10% de probabilidad de que use la palabra "Oferta"
verosimilitud_oferta_dado_no_spam = 0.10  

# 3. Evidencia (Probabilidad Marginal)
# P(Oferta): ¿Cuál es la probabilidad de que cualquier correo contenga la palabra "Oferta"?
# Se calcula sumando ambos escenarios (Teorema de Probabilidad Total)
evidencia_oferta = (verosimilitud_oferta_dado_spam * prob_spam) + (verosimilitud_oferta_dado_no_spam * prob_no_spam)

print("--- DATOS HISTÓRICOS DE LA IA ---")
print(f"Probabilidad de recibir Spam P(Spam) = {prob_spam * 100}%")
print(f"Probabilidad de que un Spam diga 'Oferta' P(Oferta|Spam) = {verosimilitud_oferta_dado_spam * 100}%")
print(f"Probabilidad general de ver la palabra 'Oferta' P(Oferta) = {evidencia_oferta * 100}%\n")

# --- LLEGA UN NUEVO CORREO ---
print("-> ALERTA: Ha llegado un nuevo correo y contiene la palabra 'OFERTA'.")
print("-> La IA está evaluando si enviarlo a la bandeja de entrada o a la papelera...\n")

# Calculamos P(Spam | Oferta)
posterior_spam = regla_de_bayes(prob_spam, verosimilitud_oferta_dado_spam, evidencia_oferta)

# Calculamos P(No Spam | Oferta)
posterior_no_spam = regla_de_bayes(prob_no_spam, verosimilitud_oferta_dado_no_spam, evidencia_oferta)

print("=== VEREDICTO DE LA REGLA DE BAYES ===")
print(f"Probabilidad de que SEA SPAM dada la palabra: P(Spam | Oferta) = {posterior_spam * 100:.2f}%")
print(f"Probabilidad de que sea LEGÍTIMO dada la palabra: P(No Spam | Oferta) = {posterior_no_spam * 100:.2f}%\n")

# Decisión de la IA
if posterior_spam > posterior_no_spam:
    print("DECISIÓN: Mover a la carpeta de SPAM (Bloqueado).")
else:
    print("DECISIÓN: Mover a la Bandeja de Entrada (Permitido).")