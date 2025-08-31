"""
Teste de áudio offline
"""
import win32com.client

def testar_audio():
    print("Testando audio offline...")
    
    try:
        # Windows Speech API
        tts = win32com.client.Dispatch("SAPI.SpVoice")
        tts.Rate = 1
        
        print("Falando...")
        tts.Speak("Teste de audio offline funcionando")
        
        print("Audio OK!")
        return True
        
    except Exception as e:
        print(f"Erro audio: {e}")
        
        # Tentar pyttsx3 como backup
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("Teste com pyttsx3")
            engine.runAndWait()
            print("pyttsx3 funcionando!")
            return True
        except Exception as e2:
            print(f"Erro pyttsx3: {e2}")
            return False

if __name__ == "__main__":
    testar_audio()