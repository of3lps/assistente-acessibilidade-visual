# Solução para Problemas de Câmera

## 🔍 Diagnóstico Atual

A câmera não está sendo detectada pelos seguintes motivos possíveis:

1. **Câmera em uso por outro aplicativo**
2. **Drivers não instalados/atualizados**
3. **Câmera integrada desabilitada**
4. **Permissões de privacidade bloqueadas**

## 🛠️ Soluções Rápidas

### 1. Verificar se câmera está livre
```bash
# Feche todos os apps que podem usar câmera:
# - Teams, Zoom, Skype
# - Navegadores com sites de vídeo
# - Aplicativos de câmera do Windows
```

### 2. Verificar permissões do Windows
1. Vá em **Configurações > Privacidade > Câmera**
2. Ative "Permitir que aplicativos acessem sua câmera"
3. Ative "Permitir que aplicativos da área de trabalho acessem sua câmera"

### 3. Testar câmera no Windows
1. Abra o app **Câmera** do Windows
2. Se funcionar lá, execute nosso app novamente

### 4. Usar webcam USB externa
- Conecte uma webcam USB
- Execute: `python app_camera.py`

## 🚀 Versão que Funciona SEM Câmera

Se a câmera não funcionar, use esta versão que simula detecções:

```bash
python demo_sem_camera.py
```

Esta versão:
- ✅ Abre janela visual
- ✅ Simula objetos se movendo
- ✅ Detecta com YOLO real
- ✅ Anuncia por voz
- ✅ Mostra todas as funcionalidades

## 📋 Checklist de Troubleshooting

- [ ] Fechar outros apps que usam câmera
- [ ] Verificar permissões de privacidade
- [ ] Testar app Câmera do Windows
- [ ] Tentar webcam USB externa
- [ ] Executar como administrador
- [ ] Reiniciar o computador

## 🎯 Próximos Passos

1. **Para demonstração**: Use `demo_sem_camera.py`
2. **Para teste real**: Resolva problema de câmera
3. **Para hackathon**: Migrar para Snapdragon com ONNX

O sistema de IA e voz está **100% funcional** - apenas a câmera precisa ser configurada!