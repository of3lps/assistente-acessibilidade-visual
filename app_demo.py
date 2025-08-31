import cv2
import numpy as np
import pyttsx3
import threading
import time
from ultralytics import YOLO

class DemoAssistant:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        print("Carregando YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        self.classes = {
            'person': 'pessoa',
            'car': 'carro', 
            'truck': 'caminhao',
            'bus': 'onibus',
            'bicycle': 'bicicleta'
        }
        
        self.last_speak = 0
        self.speaking = False
    
    def speak(self, text):
        if time.time() - self.last_speak > 2 and not self.speaking:
            self.last_speak = time.time()
            print(f"VOZ: {text}")
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        self.speaking = False
    
    def create_test_frame(self, frame_num):
        """Cria frames de teste com objetos simulados"""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Fundo
        img[:] = (50, 50, 50)
        
        # Simular pessoa se movendo
        x = 100 + (frame_num * 2) % 400
        cv2.rectangle(img, (x, 150), (x+80, 350), (255, 200, 150), -1)
        cv2.putText(img, "PESSOA", (x+10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        
        # Simular carro
        if frame_num % 60 < 30:
            cv2.rectangle(img, (450, 300), (580, 380), (100, 100, 255), -1)
            cv2.putText(img, "CARRO", (470, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        
        return img
    
    def try_camera(self):
        """Tenta usar câmera real"""
        for i in range(3):  # Tenta indices 0, 1, 2
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    print(f"Camera encontrada no indice {i}")
                    return cap
                cap.release()
        return None
    
    def run(self):
        print("Tentando conectar camera...")
        cap = self.try_camera()
        
        if cap is None:
            print("Camera nao encontrada. Usando simulacao...")
            use_simulation = True
        else:
            print("Camera conectada!")
            use_simulation = False
        
        print("Pressione 'q' para sair")
        print("Janela abrindo...")
        
        frame_count = 0
        
        try:
            while True:
                if use_simulation:
                    frame = self.create_test_frame(frame_count)
                    time.sleep(0.1)  # Simular FPS
                else:
                    ret, frame = cap.read()
                    if not ret:
                        break
                
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
                                        
                                        # Desenhar
                                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                        cv2.putText(frame, f"{self.classes[class_name]}", 
                                                  (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                        
                                        # Posicao
                                        center_x = (x1 + x2) // 2
                                        w = frame.shape[1]
                                        
                                        if center_x < w // 3:
                                            pos = "esquerda"
                                        elif center_x > 2 * w // 3:
                                            pos = "direita"
                                        else:
                                            pos = "centro"
                                        
                                        detections.append(f"{self.classes[class_name]} no {pos}")
                    
                    # Anunciar primeira deteccao
                    if detections:
                        self.speak(detections[0])
                
                # Mostrar frame
                cv2.imshow('Assistente de Acessibilidade Visual', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                frame_count += 1
        
        except Exception as e:
            print(f"Erro: {e}")
        
        finally:
            if cap:
                cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    app = DemoAssistant()
    app.run()