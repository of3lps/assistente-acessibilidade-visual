import cv2
import numpy as np
import time

# Versão simplificada sem dependências pesadas
class SimpleAccessibilityAssistant:
    def __init__(self):
        # Classificador de faces (já vem com OpenCV)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.last_announcement = time.time()
        
    def detect_faces(self, frame):
        """Detecta rostos usando Haar Cascades"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces
    
    def get_position(self, x, w, frame_width):
        """Determina posição do objeto"""
        center = x + w // 2
        if center < frame_width * 0.33:
            return "à esquerda"
        elif center > frame_width * 0.66:
            return "à direita"
        else:
            return "à frente"
    
    def announce_console(self, message):
        """Anuncia no console (substitui TTS temporariamente)"""
        current_time = time.time()
        if current_time - self.last_announcement > 2:
            print(f"🔊 {message}")
            self.last_announcement = current_time
    
    def run(self):
        """Loop principal"""
        cap = cv2.VideoCapture(0)
        
        print("Assistente Simples iniciado!")
        print("Detectando pessoas... Pressione 'q' para sair")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detectar rostos
            faces = self.detect_faces(frame)
            
            for (x, y, w, h) in faces:
                # Desenhar retângulo
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Calcular posição
                position = self.get_position(x, w, frame.shape[1])
                
                # Anunciar
                if w > 100:  # Pessoa próxima
                    self.announce_console(f"Pessoa próxima {position}")
                
                # Mostrar texto na tela
                cv2.putText(frame, f"Pessoa {position}", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Assistente de Acessibilidade', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    assistant = SimpleAccessibilityAssistant()
    assistant.run()