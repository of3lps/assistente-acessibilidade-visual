import cv2
import numpy as np
import pyttsx3
import time
from ultralytics import YOLO

class SimpleDemo:
    def __init__(self):
        print("Inicializando TTS...")
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        print("Carregando YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        self.classes_pt = {
            'person': 'pessoa',
            'car': 'carro', 
            'truck': 'caminhao',
            'bus': 'onibus',
            'bicycle': 'bicicleta'
        }
    
    def speak(self, text):
        print(f"FALANDO: {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
    
    def create_test_image(self):
        """Cria uma imagem de teste com formas simples"""
        img = np.ones((480, 640, 3), dtype=np.uint8) * 50
        
        # Desenhar algumas formas para simular objetos
        cv2.rectangle(img, (100, 200), (200, 400), (0, 255, 0), -1)  # Retângulo verde
        cv2.circle(img, (400, 300), 50, (255, 0, 0), -1)  # Círculo azul
        cv2.rectangle(img, (500, 100), (600, 200), (0, 0, 255), -1)  # Retângulo vermelho
        
        return img
    
    def detect_and_announce(self, image):
        """Detecta objetos e anuncia"""
        results = self.model(image, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.3:
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        if class_name in self.classes_pt:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            w, h = x2-x1, y2-y1
                            
                            # Calcular posição
                            center_x = x1 + w//2
                            if center_x < 213:
                                pos = "esquerda"
                            elif center_x > 426:
                                pos = "direita"
                            else:
                                pos = "centro"
                            
                            # Calcular distância aproximada
                            area = w * h
                            if area > 50000:
                                dist = "muito proximo"
                            elif area > 20000:
                                dist = "proximo"
                            else:
                                dist = "distante"
                            
                            detections.append({
                                'name': self.classes_pt[class_name],
                                'position': pos,
                                'distance': dist,
                                'confidence': conf
                            })
        
        # Anunciar detecções
        if detections:
            for det in detections[:2]:  # Máximo 2 objetos
                msg = f"{det['name']} {det['distance']} na {det['position']}"
                self.speak(msg)
                time.sleep(1)
        else:
            self.speak("Nenhum objeto detectado")
    
    def demo_with_webcam(self):
        """Tenta usar webcam, senão usa imagem de teste"""
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("Webcam encontrada! Usando camera real...")
            self.speak("Camera ativada")
            
            for i in range(10):  # 10 detecções
                ret, frame = cap.read()
                if ret:
                    print(f"Processando frame {i+1}...")
                    self.detect_and_announce(frame)
                    time.sleep(3)
                else:
                    break
            cap.release()
        else:
            print("Webcam nao encontrada. Usando imagem de teste...")
            self.speak("Usando modo demonstracao")
            
            test_img = self.create_test_image()
            self.detect_and_announce(test_img)
    
    def demo_simple(self):
        """Demo básico apenas com TTS"""
        print("=== DEMO ASSISTENTE DE ACESSIBILIDADE ===")
        
        self.speak("Assistente de acessibilidade ativado")
        time.sleep(2)
        
        # Simular detecções
        detections = [
            "pessoa proxima na frente",
            "carro distante na direita", 
            "bicicleta na esquerda"
        ]
        
        for detection in detections:
            self.speak(detection)
            time.sleep(2)
        
        self.speak("Demonstracao concluida")

if __name__ == "__main__":
    demo = SimpleDemo()
    
    print("Escolha o modo:")
    print("1 - Demo simples (apenas voz)")
    print("2 - Demo com detecção (webcam ou teste)")
    
    try:
        choice = input("Digite 1 ou 2: ").strip()
        
        if choice == "1":
            demo.demo_simple()
        else:
            demo.demo_with_webcam()
            
    except KeyboardInterrupt:
        print("\nDemo encerrado")
    except Exception as e:
        print(f"Erro: {e}")