import cv2
import pyttsx3
import threading
import time
from ultralytics import YOLO

class VisualAssistant:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        self.model = YOLO('yolov8n.pt')
        
        self.classes = {
            'person': 'pessoa',
            'car': 'carro',
            'truck': 'caminhao',
            'bus': 'onibus',
            'bicycle': 'bicicleta',
            'motorcycle': 'moto'
        }
        
        self.last_speak = 0
        self.speaking = False
    
    def speak(self, text):
        if time.time() - self.last_speak > 3 and not self.speaking:
            self.last_speak = time.time()
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        self.speaking = False
    
    def run(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Erro: Camera nao encontrada")
            return
        
        print("Pressione 'q' para sair")
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Processar a cada 10 frames
            if frame_count % 10 == 0:
                results = self.model(frame, verbose=False)
                
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            conf = float(box.conf[0])
                            if conf > 0.5:
                                cls_id = int(box.cls[0])
                                class_name = self.model.names[cls_id]
                                
                                if class_name in self.classes:
                                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                                    
                                    # Desenhar retangulo
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"{self.classes[class_name]}", 
                                              (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                                    
                                    # Calcular posicao
                                    center_x = (x1 + x2) // 2
                                    w = frame.shape[1]
                                    
                                    if center_x < w // 3:
                                        pos = "esquerda"
                                    elif center_x > 2 * w // 3:
                                        pos = "direita"
                                    else:
                                        pos = "frente"
                                    
                                    # Anunciar
                                    self.speak(f"{self.classes[class_name]} na {pos}")
            
            cv2.imshow('Assistente Visual', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = VisualAssistant()
    app.run()