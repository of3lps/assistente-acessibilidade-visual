import cv2
import numpy as np
import pyttsx3
import threading
import time
from ultralytics import YOLO
import easyocr

class AccessibilityAssistant:
    def __init__(self):
        # TTS Engine
        print("Inicializando sistema de voz...")
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        
        # YOLO Model
        print("Carregando modelo YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        # OCR Reader
        print("Inicializando OCR...")
        self.ocr_reader = easyocr.Reader(['pt', 'en'])
        
        # Audio control
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
        
        # Posição horizontal
        if center_x < frame_w * 0.33:
            return "à esquerda"
        elif center_x > frame_w * 0.66:
            return "à direita"
        else:
            return "à frente"
    
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
            print(f"VOZ: {message}")
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
        
        # Processar detecções importantes
        for det in detections:
            distance = self.get_distance_description(det['bbox'], frame.shape)
            position = self.get_position_description(det['bbox'], frame.shape)
            
            if distance in ['muito próximo', 'próximo']:
                message = f"{det['portuguese']} {distance} {position}"
                self.announce(message)
                break  # Apenas o mais importante
    
    def run(self):
        """Loop principal da aplicação"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not cap.isOpened():
            print("ERRO: Nao foi possivel acessar a camera")
            return
        
        print("Assistente de Acessibilidade iniciado!")
        print("Pressione Ctrl+C para sair")
        print("Digite 't' + Enter para ler texto na tela atual")
        
        self.announce("Assistente de acessibilidade ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("ERRO: Erro ao capturar frame da camera")
                    break
                
                # Processar a cada 5 frames para performance
                if frame_count % 5 == 0:
                    self.process_frame(frame)
                
                frame_count += 1
                
                # Pequena pausa para não sobrecarregar
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nAplicacao encerrada pelo usuario")
        finally:
            cap.release()

if __name__ == "__main__":
    try:
        assistant = AccessibilityAssistant()
        assistant.run()
    except Exception as e:
        print(f"ERRO: {e}")