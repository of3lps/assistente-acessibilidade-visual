"""
Reinicia e testa câmera
"""
import cv2
import time

def reiniciar_camera():
    print("Reiniciando camera...")
    
    # Liberar todos os recursos
    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            cap.release()
        except:
            pass
    
    cv2.destroyAllWindows()
    time.sleep(2)
    
    print("Testando camera com DirectShow...")
    
    # Tentar com DirectShow (melhor para Windows)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Tentando sem DirectShow...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERRO: Camera nao disponivel")
        return
    
    # Configurar camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("Camera iniciada! Pressione ESC para sair")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Erro ao capturar frame")
            break
        
        # Adicionar texto na imagem
        cv2.putText(frame, "CAMERA FUNCIONANDO", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.putText(frame, "Pressione ESC para sair", (10, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Mostrar frame
        cv2.imshow('Camera Reiniciada', frame)
        
        # ESC para sair
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Camera fechada")

if __name__ == "__main__":
    reiniciar_camera()