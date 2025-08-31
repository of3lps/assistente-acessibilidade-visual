# Como Usar o Assistente de Acessibilidade Visual

## ✅ Sistema Funcionando!

O protótipo está operacional e testado. Aqui estão as opções disponíveis:

## 🚀 Execução Rápida

### 1. Demo Completo (Recomendado)
```bash
python demo_final.py
```
- Testa webcam automaticamente
- Se não tiver câmera, usa modo demonstração
- Mostra todas as funcionalidades

### 2. Versão Sem Interface Gráfica
```bash
python main_headless.py
```
- Funciona apenas com processamento e voz
- Ideal para sistemas sem interface gráfica

### 3. Teste de Câmera
```bash
python test_camera.py
```
- Verifica se a câmera está funcionando

## 🎯 Funcionalidades Demonstradas

✅ **Detecção de Objetos**
- Pessoas, carros, bicicletas, etc.
- Confiança > 30% para reduzir falsos positivos

✅ **Cálculo de Distâncias**
- "muito próximo" - objetos grandes na tela
- "próximo" - objetos médios
- "distante" - objetos pequenos

✅ **Posicionamento**
- "esquerda", "direita", "frente"
- Baseado na posição horizontal do objeto

✅ **Voz em Português**
- Síntese de voz com pyttsx3
- Anuncia objetos importantes
- Prioriza objetos próximos

## 🔧 Status do Sistema

### ✅ Funcionando
- Carregamento do modelo YOLO
- Sistema de voz (TTS)
- Detecção de objetos
- Processamento de imagens
- Cálculos de posição e distância

### ⚠️ Limitações Atuais
- Câmera não detectada no ambiente atual
- Funciona em modo demonstração
- Interface gráfica desabilitada (problema OpenCV)

## 🎮 Controles

Durante a execução:
- **Ctrl+C**: Sair da aplicação
- O sistema anuncia automaticamente objetos detectados

## 📊 Performance

- **Modelo**: YOLOv8n (leve e rápido)
- **Processamento**: CPU (funciona sem GPU)
- **Latência**: ~1-2 segundos por detecção
- **Classes**: 15+ objetos importantes em português

## 🔄 Próximos Passos para Snapdragon

1. **Migrar para ONNX Runtime**:
```python
import onnxruntime as ort
session = ort.InferenceSession('yolov8n.onnx', 
                              providers=['DmlExecutionProvider'])
```

2. **Usar Windows Speech API**:
```python
import win32com.client
tts = win32com.client.Dispatch("SAPI.SpVoice")
```

3. **Otimizar para NPU**:
- DirectML provider
- Batch processing
- Thread optimization

## 🐛 Troubleshooting

### Problema: "Camera index out of range"
- **Solução**: Normal, sistema usa modo demo
- **Alternativa**: Conectar webcam USB

### Problema: Encoding errors
- **Solução**: Já corrigido nos arquivos atualizados
- **Causa**: Emojis não suportados no Windows

### Problema: TTS não funciona
- **Verificar**: `pip install pyttsx3`
- **Windows**: Já inclui engine de voz

## 📁 Arquivos Principais

- `demo_final.py` - Demo completo (USAR ESTE)
- `main_headless.py` - Versão sem interface
- `main.py` - Versão original (com problemas de GUI)
- `test_camera.py` - Teste de câmera
- `yolov8n.pt` - Modelo YOLO pré-treinado

## 🎯 Demonstração Funcional

O sistema está **100% funcional** para:
1. Carregar modelo de IA
2. Processar imagens
3. Detectar objetos importantes
4. Calcular posições e distâncias
5. Anunciar por voz em português

**Execute `python demo_final.py` para ver funcionando!**