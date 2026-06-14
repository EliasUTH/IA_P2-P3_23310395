import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random

# ==========================================
# 1. BASE DE DATOS (CORPUS DE ENTRENAMIENTO)
# ==========================================
# En lugar de leer un archivo externo, definimos los datos aqui mismo 
# para que tu archivo sea 100% autocontenido y facil de ejecutar.
datos_intenciones = {
    "intents": [
        {
            "tag": "saludos",
            "patterns": ["Hola", "Buenos dias", "Que tal", "Hey", "Saludos"],
            "responses": ["¡Hola! ¿En qué puedo ayudarte?", "¡Buenos días! ¿Qué necesitas hoy?", "¡Hola! Bienvenido al proyecto de IA."]
        },
        {
            "tag": "despedidas",
            "patterns": ["Adios", "Nos vemos", "Hasta luego", "Me voy", "Bye"],
            "responses": ["¡Hasta luego! Que tengas un buen día.", "¡Nos vemos! Éxito con tu proyecto.", "Adiós, vuelve pronto."]
        },
        {
            "tag": "proyecto",
            "patterns": ["De que trata este proyecto", "Que tecnologia usas", "Como funcionas", "Que eres"],
            "responses": ["Soy un modelo de Deep Learning creado con TensorFlow en Python.", "Fui entrenado usando Redes Neuronales para la clase de IA.", "Soy un bot basado en clasificación de intenciones."]
        },
        {
            "tag": "creador",
            "patterns": ["Quien te creo", "Quien es tu programador", "De quien es este proyecto"],
            "responses": ["Fui desarrollado por un estudiante de Mecatrónica del CETI.", "Mi creador es el autor de este reporte de IA."]
        }
    ]
}

# ==========================================
# 2. PREPROCESAMIENTO DE DATOS (NLP)
# ==========================================
oraciones = []
etiquetas = []
respuestas_por_etiqueta = {}
etiquetas_unicas = []

# Extraer informacion del JSON
for intento in datos_intenciones['intents']:
    respuestas_por_etiqueta[intento['tag']] = intento['responses']
    if intento['tag'] not in etiquetas_unicas:
        etiquetas_unicas.append(intento['tag'])
        
    for patron in intento['patterns']:
        oraciones.append(patron)
        etiquetas.append(intento['tag'])

# Convertir etiquetas de texto a numeros (Label Encoding manual)
etiquetas_numericas = [etiquetas_unicas.index(t) for t in etiquetas]
etiquetas_numericas = np.array(etiquetas_numericas)

# Tokenizacion: Convertir palabras a secuencias de numeros
vocabulario_tamano = 1000
longitud_maxima = 20
oov_token = "<OOV>" # Token para palabras fuera del vocabulario

tokenizador = Tokenizer(num_words=vocabulario_tamano, oov_token=oov_token)
tokenizador.fit_on_texts(oraciones)

# Convertir las oraciones a secuencias matematicas y rellenar espacios (Padding)
secuencias = tokenizador.texts_to_sequences(oraciones)
secuencias_pad = pad_sequences(secuencias, truncating='post', maxlen=longitud_maxima)

# ==========================================
# 3. ARQUITECTURA DE LA RED NEURONAL (DEEP LEARNING)
# ==========================================
print("Construyendo y entrenando el modelo de Deep Learning...\n")

modelo = Sequential([
    # Capa de incrustacion: Aprende el significado semantico de las palabras
    Embedding(vocabulario_tamano, 16, input_length=longitud_maxima),
    # Capa de agrupacion: Reduce la dimensionalidad de los datos
    GlobalAveragePooling1D(),
    # Capas densas (Feed-Forward) con activacion ReLU
    Dense(16, activation='relu'),
    Dense(16, activation='relu'),
    # Capa de salida: Distribucion de probabilidad (Softmax) para cada intencion
    Dense(len(etiquetas_unicas), activation='softmax')
])

modelo.compile(loss='sparse_categorical_crossentropy', 
               optimizer='adam', 
               metrics=['accuracy'])

# ==========================================
# 4. ENTRENAMIENTO DEL MODELO
# ==========================================
# Epochs = Iteraciones de aprendizaje
historial = modelo.fit(secuencias_pad, etiquetas_numericas, epochs=500, verbose=0)
print("¡Entrenamiento del modelo completado con exito!\n")

# ==========================================
# 5. FUNCION DE INFERENCIA (EL CHAT)
# ==========================================
def chat():
    print("-----------------------------------------------------")
    print("CHATBOT DE IA INICIADO (Escribe 'salir' para detener)")
    print("-----------------------------------------------------")
    
    while True:
        entrada_usuario = input("Tú: ")
        if entrada_usuario.lower() == "salir":
            print("Bot: ¡Nos vemos!")
            break
            
        # Procesar la entrada del usuario de la misma forma que el entrenamiento
        secuencia_entrada = tokenizador.texts_to_sequences([entrada_usuario])
        secuencia_entrada_pad = pad_sequences(secuencia_entrada, truncating='post', maxlen=longitud_maxima)
        
        # Predecir la intencion (Devuelve un arreglo de probabilidades)
        predicciones = modelo.predict(secuencia_entrada_pad, verbose=0)
        
        # Obtener el indice de la probabilidad mas alta
        indice_etiqueta_ganadora = np.argmax(predicciones)
        etiqueta_ganadora = etiquetas_unicas[indice_etiqueta_ganadora]
        probabilidad = predicciones[0][indice_etiqueta_ganadora]
        
        # Verificar que el modelo este suficientemente seguro
        if probabilidad > 0.6:
            # Elegir una respuesta aleatoria dentro de la categoria ganadora
            respuesta = random.choice(respuestas_por_etiqueta[etiqueta_ganadora])
            print(f"Bot: {respuesta}")
        else:
            print("Bot: Lo siento, no estoy seguro de entender a qué te refieres. ¿Puedes reformularlo?")

# ==========================================
# EJECUCION
# ==========================================
if __name__ == "__main__":
    chat()