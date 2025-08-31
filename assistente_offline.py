"""
Assistente 100% Offline com áudio garantido
"""
import cv2
import numpy as np
import time
import threading
from ultralytics import YOLO
import win32com.client

class AssistenteOffline:
    def __init__(self):
        print("Inicializando sistema offline...")
        
        # Modelo YOLO local
        self.model = YOLO('yolov8n.pt')
        
        # TTS offline garantido
        self.init_tts()
        
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
            'chair': 'cadeira',
            'bottle': 'garrafa',
            'cup': 'copo',
            'cell phone': 'celular'
        }
        
        print("Sistema offline pronto!")
    
    def init_tts(self):
        """Inicializa TTS com fallback"""
        try:
            # Tentar Windows Speech API primeiro
            self.tts = win32com.client.Dispatch("SAPI.SpVoice")
            self.tts.Rate = 1
            self.tts_type = "windows"
            print("TTS Windows ativado")
        except:
            try:
                # Fallback para pyttsx3
                import pyttsx3
                self.tts = pyttsx3.init()
                self.tts.setProperty('rate', 150)
                self.tts_type = "pyttsx3"
                print("TTS pyttsx3 ativado")
            except:
                self.tts = None
                self.tts_type = "none"
                print("AVISO: TTS não disponível")
    
    def speak(self, text):
        """Fala com fallback garantido"""
        if not self.speaking and self.tts:
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            print(f"VOZ: {text}")
            
            if self.tts_type == "windows":
                self.tts.Speak(text)
            elif self.tts_type == "pyttsx3":
                self.tts.say(text)
                self.tts.runAndWait()
            else:
                # Fallback: apenas print
                print(f"[AUDIO INDISPONIVEL] {text}")
                
        except Exception as e:
            print(f"Erro TTS: {e}")
        finally:
            self.speaking = False
    
    def detect_objects(self, frame):
        """Detecção offline"""
        results = self.model(frame, verbose=False)
        h, w = frame.shape[:2]
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:
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
                            
                            if area_ratio > 0.2:
                                distance = "muito proximo"
                            elif area_ratio > 0.1:
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
                            
                            # Desenhar
                            color = (0, 0, 255) if distance == 'muito proximo' else (0, 255, 0)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            cv2.putText(frame, f"{self.classes_pt[class_name]}", 
                                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        return detections, frame
    
    def run(self):
        """Executa assistente offline"""
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("ERRO: Camera offline")
            return
        
        print("Assistente offline iniciado!")
        self.speak("Assistente offline ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Processar
                if frame_count % 15 == 0:  # Menos frequente para estabilidade
                    detections, frame = self.detect_objects(frame)
                    
                    # Anunciar
                    if detections:
                        main_obj = max(detections, key=lambda x: x['area_ratio'])
                        
                        current_time = time.time()
                        if current_time - self.last_announcement > 4:  # Mais espaçado
                            message = f"{main_obj['name']} {main_obj['distance']} na {main_obj['position']}"
                            self.speak(message)
                            self.last_announcement = current_time
                
                # Interface
                cv2.putText(frame, "SISTEMA OFFLINE", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                cv2.putText(frame, f"TTS: {self.tts_type.upper()}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
                cv2.imshow('Assistente Offline', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\nEncerrando...")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.speak("Sistema desativado")

if __name__ == "__main__":
    assistente = AssistenteOffline()
    assistente.run()