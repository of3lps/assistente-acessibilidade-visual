import cv2
import numpy as np
import pyttsx3
import threading
import time
from ultralytics import YOLO
import easyocr
from collections import deque

class AccessibilityAssistant:
    def __init__(self):
        # TTS Engine
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        
        # YOLO Model (lightweight)
        print("Carregando modelo YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        # OCR Reader
        print("Inicializando OCR...")
        self.ocr_reader = easyocr.Reader(['pt', 'en'])
        
        # Audio control
        self.audio_queue = deque(maxlen=3)
        self.last_announcement = time.time()
        self.speaking = False
        
        # Important classes for accessibility
        self.important_classes = {
            'person': 'pessoa',
            'car': 'carro',
            'truck': 'caminhão',
            'bus': 'ônibus',
            'bicycle': 'bicicleta',
            'motorcycle': 'moto',
            'traffic light': 'semáforo',
            'stop sign': 'placa de pare',
            'chair': 'cadeira',
            'bench': 'banco'
        }
        
    def get_distance_description(self, bbox, frame_shape):
        """Calcula descrição de distância baseada no tamanho"""
        _, _, w, h = bbox
        frame_h, frame_w = frame_shape[:2]
        
        area_ratio = (w * h) / (frame_w * frame_h)
        
        if area_ratio > 0.3:
            return "muito próximo"
        elif area_ratio > 0.1:
            return "próximo"
        elif area_ratio > 0.02:
            return "médio"
        else:
            return "distante"
    
    def get_position_description(self, bbox, frame_shape):
        """Determina posição relativa do objeto"""
        x, y, w, h = bbox
        frame_h, frame_w = frame_shape[:2]
        
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Posição horizontal
        if center_x < frame_w * 0.33:
            h_pos = "à esquerda"
        elif center_x > frame_w * 0.66:
            h_pos = "à direita"
        else:
            h_pos = "à frente"
            
        # Posição vertical
        if center_y < frame_h * 0.33:
            v_pos = "acima"
        elif center_y > frame_h * 0.66:
            v_pos = "abaixo"
        else:
            v_pos = ""
            
        return f"{h_pos} {v_pos}".strip()
    
    def detect_objects(self, frame):
        """Detecta objetos usando YOLO"""
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        if class_name in self.important_classes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            detections.append({
                                'class': class_name,
                                'portuguese': self.important_classes[class_name],
                                'confidence': conf,
                                'bbox': (x1, y1, x2-x1, y2-y1)
                            })
        
        return detections
    
    def read_text(self, frame):
        """Lê texto na imagem usando OCR"""
        try:
            results = self.ocr_reader.readtext(frame)
            texts = []
            for (bbox, text, conf) in results:
                if conf > 0.7 and len(text.strip()) > 2:
                    texts.append(text.strip())
            return texts
        except:
            return []
    
    def announce(self, message):
        """Anuncia mensagem por voz"""
        current_time = time.time()
        if current_time - self.last_announcement > 3 and not self.speaking:
            self.last_announcement = current_time
            threading.Thread(target=self._speak, args=(message,), daemon=True).start()
    
    def _speak(self, message):
        """Executa TTS em thread separada"""
        self.speaking = True
        try:
            self.tts.say(message)
            self.tts.runAndWait()
        except:
            pass
        finally:
            self.speaking = False
    
    def process_frame(self, frame):
        """Processa um frame completo"""
        # Detectar objetos
        detections = self.detect_objects(frame)
        
        # Preparar anúncios
        announcements = []
        
        # Processar detecções importantes
        for det in detections:
            distance = self.get_distance_description(det['bbox'], frame.shape)
            position = self.get_position_description(det['bbox'], frame.shape)
            
            if distance in ['muito próximo', 'próximo']:
                message = f"{det['portuguese']} {distance} {position}"
                announcements.append(message)
                
                # Desenhar na tela
                x, y, w, h = det['bbox']
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{det['portuguese']} {distance}", 
                          (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Anunciar objetos mais importantes
        if announcements:
            main_announcement = announcements[0]  # Mais importante
            self.announce(main_announcement)
        
        return frame
    
    def run(self):
        """Loop principal da aplicação"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Assistente de Acessibilidade iniciado!")
        print("Pressione 'q' para sair, 't' para ler texto na tela")
        
        self.announce("Assistente de acessibilidade ativado")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Processar a cada 3 frames para performance
            if frame_count % 3 == 0:
                frame = self.process_frame(frame)
            
            # Mostrar frame
            cv2.imshow('Assistente de Acessibilidade Visual', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                # Ler texto na tela
                texts = self.read_text(frame)
                if texts:
                    text_message = "Texto detectado: " + ", ".join(texts[:2])
                    self.announce(text_message)
                else:
                    self.announce("Nenhum texto detectado")
            
            frame_count += 1
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        assistant = AccessibilityAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")