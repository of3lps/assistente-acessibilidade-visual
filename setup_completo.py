"""
Setup completo do projeto
"""
import subprocess
import sys
import os

def instalar_dependencias():
    print("Instalando dependencias...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements_final.txt"
        ])
        print("Dependencias instaladas!")
        return True
    except:
        print("Erro ao instalar dependencias")
        return False

def baixar_modelo():
    print("Baixando modelo YOLO...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # Download automático
        print("Modelo YOLO pronto!")
        return True
    except:
        print("Erro ao baixar modelo")
        return False

def testar_sistema():
    print("Testando sistema...")
    try:
        import cv2
        import win32com.client
        
        # Testar TTS
        tts = win32com.client.Dispatch("SAPI.SpVoice")
        tts.Speak("Sistema funcionando")
        
        print("Sistema OK!")
        return True
    except:
        print("Erro no teste")
        return False

def main():
    print("=== SETUP ASSISTENTE DE ACESSIBILIDADE ===")
    
    if not instalar_dependencias():
        return
    
    if not baixar_modelo():
        return
    
    if not testar_sistema():
        return
    
    print("\nSetup concluido!")
    print("Execute: python assistente_com_voz.py")

if __name__ == "__main__":
    main()