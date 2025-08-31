"""
Script de instalação para o Assistente de Acessibilidade Visual
"""
import subprocess
import sys
import os

def install_requirements():
    """Instala todas as dependências necessárias"""
    print("Instalando dependências...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def download_yolo_model():
    """Baixa o modelo YOLO se necessário"""
    print("Verificando modelo YOLO...")
    
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # Baixa automaticamente se não existir
        print("✅ Modelo YOLO pronto!")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar modelo YOLO: {e}")
        return False

def test_camera():
    """Testa se a câmera está funcionando"""
    print("Testando câmera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            print("✅ Câmera funcionando!")
            return True
        else:
            print("❌ Câmera não detectada")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar câmera: {e}")
        return False

def main():
    """Função principal de setup"""
    print("=== Setup do Assistente de Acessibilidade Visual ===\n")
    
    # Verificar se está no diretório correto
    if not os.path.exists("requirements.txt"):
        print("❌ Arquivo requirements.txt não encontrado!")
        print("Execute este script no diretório do projeto.")
        return
    
    # Instalar dependências
    if not install_requirements():
        return
    
    print()
    
    # Baixar modelo YOLO
    if not download_yolo_model():
        return
    
    print()
    
    # Testar câmera
    test_camera()
    
    print("\n=== Setup Concluído ===")
    print("Execute: python main.py")
    print("\nControles:")
    print("- 'q': Sair")
    print("- 't': Ler texto na tela")

if __name__ == "__main__":
    main()