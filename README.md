# Assistente de Acessibilidade Visual

Protótipo de aplicação que ajuda pessoas com deficiência visual a navegar usando IA local.

## Funcionalidades

✅ **Detecção de Objetos em Tempo Real**
- Identifica pessoas, carros, obstáculos
- Calcula distâncias e posições
- Feedback por voz em português

✅ **Leitura de Texto (OCR)**
- Lê placas, sinais, textos
- Ativação manual com tecla 't'

✅ **Processamento Local**
- Funciona offline
- Privacidade total
- Baixa latência

## Instalação Rápida

```bash
# 1. Instalar dependências
python setup.py

# 2. Executar aplicação
python main.py
```

## Controles

- **'q'**: Sair da aplicação
- **'t'**: Ler texto na tela atual

## Demonstração

1. Abra a aplicação
2. Posicione objetos na frente da câmera
3. Escute os anúncios de voz
4. Pressione 't' para ler textos

## Adaptação para Snapdragon X Plus

Para migrar para Snapdragon no hackathon:

1. **Substituir YOLO por ONNX**:
```python
# Trocar ultralytics por onnxruntime-directml
self.session = ort.InferenceSession('yolov8n.onnx', 
                                   providers=['DmlExecutionProvider'])
```

2. **Usar Windows Speech API**:
```python
# Trocar pyttsx3 por Windows Speech Platform
import win32com.client
self.tts = win32com.client.Dispatch("SAPI.SpVoice")
```

3. **Otimizar para NPU**:
- Usar DirectML provider
- Ajustar batch size
- Configurar threads

## Arquitetura

```
main.py              # App principal
├── YOLO Detection   # Detecção de objetos
├── EasyOCR         # Reconhecimento de texto  
├── TTS Engine      # Síntese de voz
└── OpenCV          # Processamento de vídeo
```

## Performance Esperada

- **Latência**: ~200ms (CPU) → ~50ms (Snapdragon NPU)
- **FPS**: 10-15 (CPU) → 30+ (Snapdragon)
- **Consumo**: Alto (CPU) → Baixo (NPU otimizado)

## Próximos Passos

1. Testar o protótipo local
2. Migrar para ONNX Runtime + DirectML
3. Otimizar para Snapdragon X Plus
4. Adicionar mais funcionalidades (navegação GPS, etc.)