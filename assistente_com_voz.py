"""
Assistente com VOZ funcionando
"""
import cv2
import numpy as np
import time
import threading
from ultralytics import YOLO
import win32com.client

class AssistenteComVoz:
    def __init__(self):
        print("Carregando modelo YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        print("Inicializando voz...")
        # Usar Windows Speech API diretamente
        self.tts = win32com.client.Dispatch("SAPI.SpVoice")
        self.tts.Rate = 1  # Velocidade normal
        
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
        
        print("Sistema pronto!")
    
    def speak(self, text):
        """Fala imediatamente sem delay"""
        if not self.speaking:
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            print(f"🔊 VOZ: {text}")
            self.tts.Speak(text)
        except Exception as e:
            print(f"Erro TTS: {e}")
        finally:
            self.speaking = False
    
    def detect_and_announce(self, frame):
        """Detecta objetos e anuncia imediatamente"""
        results = self.model(frame, verbose=False)
        h, w = frame.shape[:2]
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:  # Confiança alta
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        if class_name in self.classes_pt:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Calcular posição
                            center_x = (x1 + x2) // 2
                            if center_x < w // 3:
                                position = "esquerda"
                            elif center_x > 2 * w // 3:
                                position = "direita"
                            else:
                                position = "frente"
                            
                            # Calcular distância
                            area = (x2 - x1) * (y2 - y1)
                            area_ratio = area / (w * h)
                            
                            if area_ratio > 0.2:
                                distance = "muito proximo"
                            elif area_ratio > 0.1:
                                distance = "proximo"
                            else:
                                distance = "distante"
                            
                            detection = {
                                'name': self.classes_pt[class_name],
                                'position': position,
                                'distance': distance,
                                'bbox': (x1, y1, x2, y2),
                                'confidence': conf,
                                'area_ratio': area_ratio
                            }
                            
                            detections.append(detection)
                            
                            # Desenhar na tela
                            color = (0, 0, 255) if distance == 'muito proximo' else (0, 255, 0)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            
                            label = f"{detection['name']} - {distance}"
                            cv2.putText(frame, label, (x1, y1-10), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Anunciar o objeto mais importante
        if detections:
            # Ordenar por área (mais próximo primeiro)
            detections.sort(key=lambda x: x['area_ratio'], reverse=True)
            
            main_detection = detections[0]
            
            # Anunciar apenas se não estiver falando
            current_time = time.time()
            if current_time - self.last_announcement > 3:  # A cada 3 segundos
                message = f"{main_detection['name']} {main_detection['distance']} na {main_detection['position']}"
                self.speak(message)
                self.last_announcement = current_time
        
        return frame
    
    def run(self):
        """Executa o assistente"""
        # Usar DirectShow para Windows
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("ERRO: Camera nao disponivel")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("🚀 Assistente iniciado!")
        print("Pressione 'q' para sair")
        
        # Anúncio inicial
        self.speak("Assistente de acessibilidade ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Erro ao capturar frame")
                    break
                
                # Processar a cada 10 frames (mais estável)
                if frame_count % 10 == 0:
                    frame = self.detect_and_announce(frame)
                
                # Adicionar informações na tela
                cv2.putText(frame, "Assistente de Acessibilidade Visual", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.putText(frame, "Detectando pessoas e objetos...", 
                           (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Mostrar frame
                cv2.imshow('Assistente com Voz', frame)
                
                # Sair com 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                frame_count += 1
                
        except KeyboardInterrupt:
            print("\nEncerrando...")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.speak("Assistente desativado")

if __name__ == "__main__":
    try:
        assistente = AssistenteComVoz()
        assistente.run()
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para sair...")