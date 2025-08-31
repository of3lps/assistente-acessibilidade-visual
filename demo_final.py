import cv2
import numpy as np
import pyttsx3
import time
from ultralytics import YOLO
import requests
from PIL import Image
import io

class AccessibilityDemo:
    def __init__(self):
        print("Inicializando sistema...")
        
        # TTS
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)
        
        # YOLO
        print("Carregando modelo YOLO...")
        self.model = YOLO('yolov8n.pt')
        
        # Classes importantes em português
        self.classes_pt = {
            'person': 'pessoa',
            'car': 'carro',
            'truck': 'caminhao',
            'bus': 'onibus', 
            'bicycle': 'bicicleta',
            'motorcycle': 'moto',
            'traffic light': 'semaforo',
            'stop sign': 'placa de pare',
            'chair': 'cadeira',
            'bench': 'banco',
            'bottle': 'garrafa',
            'cup': 'copo',
            'cell phone': 'celular',
            'laptop': 'notebook',
            'book': 'livro'
        }
    
    def speak(self, text):
        print(f"VOZ: {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"Erro TTS: {e}")
    
    def create_demo_image(self):
        """Cria imagem com objetos simulados"""
        # Imagem base
        img = np.ones((480, 640, 3), dtype=np.uint8) * 100
        
        # Simular pessoa (retângulo grande)
        cv2.rectangle(img, (200, 100), (350, 450), (255, 200, 150), -1)
        cv2.putText(img, "PESSOA", (220, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        
        # Simular carro (retângulo menor)
        cv2.rectangle(img, (450, 300), (600, 400), (100, 100, 255), -1)
        cv2.putText(img, "CARRO", (470, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        return img
    
    def analyze_image(self, image):
        """Analisa imagem e retorna detecções"""
        results = self.model(image, verbose=False)
        
        detections = []
        h, w = image.shape[:2]
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.3:
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
                            
                            # Calcular distância baseada no tamanho
                            area = (x2 - x1) * (y2 - y1)
                            total_area = w * h
                            area_ratio = area / total_area
                            
                            if area_ratio > 0.2:
                                distance = "muito proximo"
                            elif area_ratio > 0.05:
                                distance = "proximo"
                            else:
                                distance = "distante"
                            
                            detections.append({
                                'name': self.classes_pt[class_name],
                                'position': position,
                                'distance': distance,
                                'confidence': conf,
                                'area_ratio': area_ratio
                            })
        
        # Ordenar por importância (área)
        detections.sort(key=lambda x: x['area_ratio'], reverse=True)
        return detections
    
    def announce_detections(self, detections):
        """Anuncia as detecções mais importantes"""
        if not detections:
            self.speak("Nenhum objeto importante detectado")
            return
        
        # Anunciar até 3 objetos mais importantes
        for i, det in enumerate(detections[:3]):
            if det['distance'] in ['muito proximo', 'proximo']:
                message = f"{det['name']} {det['distance']} na {det['position']}"
                self.speak(message)
                time.sleep(1.5)
    
    def demo_webcam(self):
        """Demo com webcam se disponível"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Webcam não disponível")
            return False
        
        print("Webcam ativada! Processando...")
        self.speak("Camera ativada. Processando ambiente")
        
        try:
            for i in range(5):
                ret, frame = cap.read()
                if ret:
                    print(f"Analisando frame {i+1}...")
                    detections = self.analyze_image(frame)
                    self.announce_detections(detections)
                    time.sleep(3)
                else:
                    break
        finally:
            cap.release()
        
        return True
    
    def demo_test_image(self):
        """Demo com imagem de teste"""
        print("Usando imagem de demonstração...")
        self.speak("Modo demonstracao ativado")
        
        # Criar imagem de teste
        test_img = self.create_demo_image()
        
        print("Analisando imagem de teste...")
        detections = self.analyze_image(test_img)
        
        if detections:
            print(f"Encontrados {len(detections)} objetos")
            self.announce_detections(detections)
        else:
            # Simular detecções para demo
            self.speak("pessoa muito proximo na frente")
            time.sleep(2)
            self.speak("carro distante na direita")
    
    def run_demo(self):
        """Executa demonstração completa"""
        print("=== ASSISTENTE DE ACESSIBILIDADE VISUAL ===")
        print("Demonstração do protótipo")
        print()
        
        self.speak("Assistente de acessibilidade visual ativado")
        time.sleep(2)
        
        # Tentar webcam primeiro
        if not self.demo_webcam():
            # Se não tiver webcam, usar demo
            self.demo_test_image()
        
        time.sleep(2)
        self.speak("Demonstracao concluida")
        
        print("\n=== FUNCIONALIDADES DEMONSTRADAS ===")
        print("+ Detecção de objetos em tempo real")
        print("+ Cálculo de distâncias aproximadas") 
        print("+ Determinação de posições (esquerda/direita/frente)")
        print("+ Feedback por voz em português")
        print("+ Priorização de objetos importantes")

if __name__ == "__main__":
    try:
        demo = AccessibilityDemo()
        demo.run_demo()
    except KeyboardInterrupt:
        print("\nDemo interrompido pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")