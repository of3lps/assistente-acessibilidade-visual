import cv2
import time

def test_camera():
    print("Testando camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERRO: Camera nao encontrada")
        return False
    
    print("Camera encontrada! Capturando frames...")
    
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"Frame {i+1}: {frame.shape}")
        else:
            print(f"Frame {i+1}: ERRO")
        time.sleep(1)
    
    cap.release()
    print("Teste concluido!")
    return True

if __name__ == "__main__":
    test_camera()