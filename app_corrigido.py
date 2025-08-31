import cv2
import pyttsx3
import threading
import time
from ultralytics import YOLO
import logging

class AssistenteCorrigido:
    # Constantes configuráveis
    CONFIDENCE_THRESHOLD = 0.5
    DETECTION_INTERVAL = 10  # Processar a cada N frames
    SPEECH_COOLDOWN = 3  # Segundos entre anúncios
    LEFT_BOUNDARY = 0.33
    RIGHT_BOUNDARY = 0.66
    
    def __init__(self):
        self.setup_logging()
        self.init_tts()
        self.init_yolo()
        
        self.classes = {
            'person': 'pessoa',
            'car': 'carro',
            'truck': 'caminhao',
            'bus': 'onibus',
            'bicycle': 'bicicleta'
        }
        
        self.last_speak = 0
        self.speaking = False
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def init_tts(self):
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 150)
            self.logger.info("TTS inicializado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar TTS: {e}")
            self.tts = None
    
    def init_yolo(self):
        try:
            self.logger.info("Carregando modelo YOLO...")
            self.model = YOLO('yolov8n.pt')
            self.logger.info("YOLO carregado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao carregar YOLO: {e}")
            self.model = None
    
    def find_camera(self):
        """Procura câmera com diferentes backends"""
        backends = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Media Foundation"),
            (cv2.CAP_ANY, "Padrão")
        ]
        
        for backend, name in backends:
            self.logger.info(f"Tentando backend {name}...")
            for i in range(3):
                try:
                    cap = cv2.VideoCapture(i, backend)
                    if cap.isOpened():
                        # Configurar câmera
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv2.CAP_PROP_FPS, 15)
                        
                        # Testar captura
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            self.logger.info(f"Câmera {i} encontrada com {name}")
                            return cap
                    cap.release()
                except Exception as e:
                    self.logger.debug(f"Erro câmera {i}: {e}")
        
        return None
    
    def speak(self, text):
        if not self.tts:
            print(f"FALA: {text}")
            return
            
        current_time = time.time()
        if current_time - self.last_speak > self.SPEECH_COOLDOWN and not self.speaking:
            self.last_speak = current_time
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            self.logger.info(f"Falando: {text}")
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            self.logger.error(f"Erro TTS: {e}")
        finally:
            self.speaking = False
    
    def detect_objects(self, frame):
        if not self.model:
            return []
        
        try:
            results = self.model(frame, verbose=False)
            detections = []
            
            for result in results:
                if result.boxes is None:
                    continue
                    
                for box in result.boxes:
                    # Verificar se dados existem
                    if len(box.conf) == 0 or len(box.cls) == 0 or len(box.xyxy) == 0:
                        continue
                        
                    conf = float(box.conf[0])
                    if conf > self.CONFIDENCE_THRESHOLD:
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        if class_name in self.classes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            detections.append({
                                'class': class_name,
                                'portuguese': self.classes[class_name],
                                'bbox': (x1, y1, x2, y2),
                                'confidence': conf
                            })
            
            return detections
            
        except Exception as e:
            self.logger.error(f"Erro na detecção: {e}")
            return []
    
    def get_position(self, bbox, frame_width):
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) // 2
        
        if center_x < frame_width * self.LEFT_BOUNDARY:
            return "esquerda"
        elif center_x > frame_width * self.RIGHT_BOUNDARY:
            return "direita"
        else:
            return "frente"
    
    def run(self):
        self.logger.info("=== ASSISTENTE DE ACESSIBILIDADE VISUAL ===")
        
        # Procurar câmera
        cap = self.find_camera()
        if not cap:
            self.logger.error("ERRO: Nenhuma câmera encontrada!")
            self.logger.info("Verifique se:")
            self.logger.info("1. Câmera está conectada")
            self.logger.info("2. Nenhum outro app está usando a câmera")
            self.logger.info("3. Drivers estão instalados")
            return False
        
        if not self.model:
            self.logger.error("ERRO: Modelo YOLO não carregado!")
            cap.release()
            return False
        
        self.logger.info("Sistema iniciado com sucesso!")
        self.logger.info("Pressione 'q' para sair")
        
        self.speak("Assistente de acessibilidade ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    self.logger.warning("Falha ao capturar frame")
                    break
                
                # Processar detecção periodicamente
                if frame_count % self.DETECTION_INTERVAL == 0:
                    detections = self.detect_objects(frame)
                    
                    for detection in detections:
                        # Desenhar detecção
                        x1, y1, x2, y2 = detection['bbox']
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        label = f"{detection['portuguese']} {detection['confidence']:.1f}"
                        cv2.putText(frame, label, (x1, y1-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Anunciar posição
                        position = self.get_position(detection['bbox'], frame.shape[1])
                        message = f"{detection['portuguese']} na {position}"
                        self.speak(message)
                        break  # Apenas primeiro objeto
                
                # Mostrar frame
                cv2.imshow('Assistente Visual - Pressione Q para sair', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                frame_count += 1
        
        except KeyboardInterrupt:
            self.logger.info("Interrompido pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro durante execução: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.logger.info("Câmera desconectada")
        
        return True

if __name__ == "__main__":
    app = AssistenteCorrigido()
    app.run()