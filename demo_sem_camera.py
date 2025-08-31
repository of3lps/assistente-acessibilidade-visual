import cv2
import numpy as np
import pyttsx3
import threading
import time
from ultralytics import YOLO
import math

class DemoSemCamera:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        print("Carregando YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        self.classes = {
            'person': 'pessoa',
            'car': 'carro',
            'bicycle': 'bicicleta'
        }
        
        self.last_speak = 0
        self.speaking = False
    
    def speak(self, text):
        if time.time() - self.last_speak > 3 and not self.speaking:
            self.last_speak = time.time()
            print(f"🔊 {text}")
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        self.speaking = False
    
    def create_realistic_frame(self, frame_num):
        """Cria frame realista com objetos que o YOLO pode detectar"""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Fundo realista
        img[:] = (120, 120, 120)  # Cinza
        
        # Chão
        cv2.rectangle(img, (0, 350), (640, 480), (80, 80, 80), -1)
        
        # Pessoa se movendo
        person_x = 50 + int(50 * math.sin(frame_num * 0.05))
        person_y = 150
        
        # Corpo da pessoa (formato mais realista)
        cv2.ellipse(img, (person_x + 40, person_y + 60), (25, 40), 0, 0, 360, (220, 180, 140), -1)  # Corpo
        cv2.circle(img, (person_x + 40, person_y + 20), 15, (255, 220, 177), -1)  # Cabeça
        cv2.rectangle(img, (person_x + 20, person_y + 100), (person_x + 60, person_y + 180), (100, 100, 200), -1)  # Pernas
        
        # Carro aparecendo periodicamente
        if (frame_num // 30) % 3 == 0:
            car_x = 400
            car_y = 280
            cv2.rectangle(img, (car_x, car_y), (car_x + 120, car_y + 60), (50, 50, 200), -1)  # Corpo do carro
            cv2.rectangle(img, (car_x + 20, car_y - 20), (car_x + 100, car_y), (100, 100, 250), -1)  # Teto
            cv2.circle(img, (car_x + 20, car_y + 50), 15, (30, 30, 30), -1)  # Roda
            cv2.circle(img, (car_x + 100, car_y + 50), 15, (30, 30, 30), -1)  # Roda
        
        # Bicicleta ocasional
        if (frame_num // 20) % 4 == 1:
            bike_x = 200 + int(30 * math.cos(frame_num * 0.03))
            bike_y = 300
            cv2.circle(img, (bike_x, bike_y), 20, (255, 255, 0), 3)  # Roda traseira
            cv2.circle(img, (bike_x + 60, bike_y), 20, (255, 255, 0), 3)  # Roda dianteira
            cv2.line(img, (bike_x, bike_y), (bike_x + 30, bike_y - 30), (200, 200, 200), 3)  # Quadro
            cv2.line(img, (bike_x + 30, bike_y - 30), (bike_x + 60, bike_y), (200, 200, 200), 3)  # Quadro
        
        return img
    
    def run(self):
        print("=== DEMO ASSISTENTE VISUAL (SEM CÂMERA) ===")
        print("Simulando detecções em tempo real...")
        print("Pressione 'q' para sair")
        
        self.speak("Assistente visual ativado em modo demonstração")
        
        frame_count = 0
        
        try:
            while True:
                # Criar frame simulado
                frame = self.create_realistic_frame(frame_count)
                
                # Detectar objetos a cada 15 frames
                if frame_count % 15 == 0:
                    results = self.model(frame, verbose=False)
                    
                    detections = []
                    for result in results:
                        boxes = result.boxes
                        if boxes is not None:
                            for box in boxes:
                                conf = float(box.conf[0])
                                if conf > 0.3:
                                    cls_id = int(box.cls[0])
                                    class_name = self.model.names[cls_id]
                                    
                                    if class_name in self.classes:
                                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                                        
                                        # Desenhar detecção
                                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                                        
                                        label = f"{self.classes[class_name]} {conf:.2f}"
                                        cv2.putText(frame, label, (x1, y1-10), 
                                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                        
                                        # Calcular posição
                                        center_x = (x1 + x2) // 2
                                        w = frame.shape[1]
                                        
                                        if center_x < w // 3:
                                            pos = "esquerda"
                                        elif center_x > 2 * w // 3:
                                            pos = "direita"
                                        else:
                                            pos = "centro"
                                        
                                        # Calcular distância
                                        area = (x2 - x1) * (y2 - y1)
                                        if area > 8000:
                                            dist = "muito próximo"
                                        elif area > 3000:
                                            dist = "próximo"
                                        else:
                                            dist = "distante"
                                        
                                        detections.append(f"{self.classes[class_name]} {dist} no {pos}")
                    
                    # Anunciar primeira detecção
                    if detections:
                        self.speak(detections[0])
                
                # Adicionar informações na tela
                cv2.putText(frame, "DEMO - Assistente de Acessibilidade Visual", 
                          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, "Pressione 'q' para sair", 
                          (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Mostrar frame
                cv2.imshow('Assistente Visual - DEMO', frame)
                
                key = cv2.waitKey(50) & 0xFF  # 20 FPS
                if key == ord('q'):
                    break
                
                frame_count += 1
        
        except KeyboardInterrupt:
            print("Demo interrompido")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            cv2.destroyAllWindows()
            print("Demo finalizado")

if __name__ == "__main__":
    demo = DemoSemCamera()
    demo.run()