import cv2
import pyttsx3
import threading
import time
from ultralytics import YOLO

class CameraAssistant:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        print("Carregando YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        self.classes = {
            'person': 'pessoa',
            'car': 'carro',
            'bicycle': 'bicicleta',
            'motorcycle': 'moto',
            'truck': 'caminhao',
            'bus': 'onibus'
        }
        
        self.last_speak = 0
        self.speaking = False
    
    def speak(self, text):
        if time.time() - self.last_speak > 3 and not self.speaking:
            self.last_speak = time.time()
            print(f"FALANDO: {text}")
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()
    
    def _do_speak(self, text):
        self.speaking = True
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
        self.speaking = False
    
    def find_camera(self):
        """Procura camera disponivel"""
        print("Procurando cameras...")
        
        # Tentar diferentes backends
        backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
        
        for backend in backends:
            for i in range(5):  # Tenta indices 0-4
                try:
                    print(f"Testando camera {i} com backend {backend}...")
                    cap = cv2.VideoCapture(i, backend)
                    
                    if cap.isOpened():
                        # Configurar camera
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                        cap.set(cv2.CAP_PROP_FPS, 15)
                        
                        # Testar captura
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            print(f"Camera {i} funcionando! Resolucao: {frame.shape}")
                            return cap
                    
                    cap.release()
                except Exception as e:
                    print(f"Erro camera {i}: {e}")
        
        return None
    
    def run(self):
        print("=== ASSISTENTE DE ACESSIBILIDADE VISUAL ===")
        
        # Procurar camera
        cap = self.find_camera()
        
        if cap is None:
            print("ERRO: Nenhuma camera encontrada!")
            print("Verifique se:")
            print("1. Camera esta conectada")
            print("2. Nenhum outro app esta usando a camera")
            print("3. Drivers estao instalados")
            return
        
        print("Camera conectada com sucesso!")
        print("Pressione 'q' para sair")
        
        self.speak("Assistente ativado")
        
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Erro ao capturar frame")
                    break
                
                # Processar deteccao a cada 10 frames
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
                                        
                                        # Desenhar deteccao
                                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                                        
                                        label = f"{self.classes[class_name]} {conf:.1f}"
                                        cv2.putText(frame, label, (x1, y1-10), 
                                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                        
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
                                        message = f"{self.classes[class_name]} na {pos}"
                                        self.speak(message)
                
                # Mostrar video
                cv2.imshow('Assistente Visual - Pressione Q para sair', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                
                frame_count += 1
        
        except KeyboardInterrupt:
            print("Interrompido pelo usuario")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Camera desconectada")

if __name__ == "__main__":
    app = CameraAssistant()
    app.run()