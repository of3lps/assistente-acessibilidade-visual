"""
Assistente que FUNCIONA - Volta ao YOLO original
"""
import cv2
import numpy as np
import pyttsx3
import time
import threading
from ultralytics import YOLO

class AssistenteFuncionando:
    def __init__(self):
        print("Carregando modelo YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        print("Inicializando TTS...")
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        self.speaking = False
        self.last_announcement = 0
        
        # Classes em português
        self.classes_pt = {
            'person': 'pessoa',
            'car': 'carro',
            'truck': 'caminhao',
            'bus': 'onibus',
            'bicycle': 'bicicleta',
            'motorcycle': 'moto',
            'traffic light': 'semaforo',
            'chair': 'cadeira'
        }
    
    def speak(self, text):
        current_time = time.time()
        if current_time - self.last_announcement > 2 and not self.speaking:
            self.last_announcement = current_time
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            print(f"VOZ: {text}")
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        finally:
            self.speaking = False
    
    def detect_objects(self, frame):
        results = self.model(frame, verbose=False)
        detections = []
        h, w = frame.shape[:2]
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.4:
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        if class_name in self.classes_pt:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Posição
                            center_x = (x1 + x2) // 2
                            if center_x < w // 3:
                                position = "esquerda"
                            elif center_x > 2 * w // 3:
                                position = "direita"
                            else:
                                position = "frente"
                            
                            # Distância
                            area = (x2 - x1) * (y2 - y1)
                            area_ratio = area / (w * h)
                            
                            if area_ratio > 0.15:
                                distance = "muito proximo"
                            elif area_ratio > 0.05:
                                distance = "proximo"
                            else:
                                distance = "distante"
                            
                            detections.append({
                                'name': self.classes_pt[class_name],
                                'position': position,
                                'distance': distance,
                                'bbox': (x1, y1, x2, y2),
                                'confidence': conf,
                                'area_ratio': area_ratio
                            })
        
        return sorted(detections, key=lambda x: x['area_ratio'], reverse=True)
    
    def draw_detections(self, frame, detections):
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            
            if det['distance'] == 'muito proximo':
                color = (0, 0, 255)
            elif det['distance'] == 'proximo':
                color = (0, 165, 255)
            else:
                color = (0, 255, 0)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            label = f"{det['name']} ({det['confidence']:.1f})"
            cv2.putText(frame, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return frame
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("ERRO: Camera nao disponivel")
            return
        
        print("Assistente iniciado! Pressione 'q' para sair")
        self.speak("Assistente de acessibilidade ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detectar a cada 5 frames
                if frame_count % 5 == 0:
                    detections = self.detect_objects(frame)
                    
                    # Anunciar objetos próximos
                    for det in detections[:2]:
                        if det['distance'] in ['muito proximo', 'proximo']:
                            message = f"{det['name']} {det['distance']} na {det['position']}"
                            self.speak(message)
                            break
                    
                    # Desenhar detecções
                    frame = self.draw_detections(frame, detections)
                
                # Mostrar
                cv2.imshow('Assistente de Acessibilidade', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\nEncerrando...")
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    assistente = AssistenteFuncionando()
    assistente.run()