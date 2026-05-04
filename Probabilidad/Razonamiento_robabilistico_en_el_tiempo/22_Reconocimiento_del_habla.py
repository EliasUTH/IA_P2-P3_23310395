import speech_recognition as sr

def reconocer_voz():
    # 1. Inicializar el "entrenador" de reconocimiento
    recogedor = sr.Recognizer()

    # Ajustar sensibilidad al ruido ambiental
    recogedor.dynamic_energy_threshold = True 

    with sr.Microphone() as fuente:
        print("\n[IA] Silencio, por favor... Ajustando ruido de fondo.")
        recogedor.adjust_for_ambient_noise(fuente, duration=1)
        
        print("[IA] ¡Listo! Di algo (estoy escuchando)...")
        
        try:
            # 2. Escuchar el audio
            audio = recogedor.listen(fuente, timeout=5, phrase_time_limit=10)
            print("[IA] Procesando señales de audio...")

            # 3. Traducir audio a texto usando Google Speech Recognition (basado en HMM/Redes Neuronales)
            # El lenguaje es 'es-ES' para español
            texto = recogedor.recognize_google(audio, language="es-ES")
            
            print(f"\n--- RESULTADO DEL RECONOCIMIENTO ---")
            print(f"Has dicho: \"{texto}\"")
            print(f"------------------------------------")

        except sr.WaitTimeoutError:
            print("[Error] No se escuchó nada en el tiempo límite.")
        except sr.UnknownValueError:
            print("[Error] La IA no pudo entender el audio (señal muy ruidosa).")
        except sr.RequestError as e:
            print(f"[Error] No se pudo conectar al servicio; {e}")

if __name__ == "__main__":
    reconocer_voz()