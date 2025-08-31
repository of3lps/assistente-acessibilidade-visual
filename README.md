# 🦾 Assistente de Acessibilidade Visual

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Snapdragon](https://img.shields.io/badge/Optimized%20for-Snapdragon-red.svg)](https://www.qualcomm.com/products/mobile/snapdragon)

Sistema de **inteligência artificial** que detecta objetos em tempo real e os anuncia em português para pessoas com deficiência visual. Desenvolvido para dispositivos **Snapdragon** com foco em **acessibilidade** e **independência**.

## 🎯 Descrição

O **Assistente de Acessibilidade Visual** é uma solução inovadora que combina visão computacional e síntese de voz para criar "olhos digitais" que descrevem o ambiente ao usuário. O sistema detecta pessoas, veículos e objetos, calculando sua posição e distância, e anuncia essas informações em português brasileiro.

### ✨ Funcionalidades

- 🎯 **Detecção em tempo real** de pessoas, carros, ônibus, bicicletas, semáforos e objetos
- 🗣️ **Síntese de voz em português** com anúncios contextuais
- 📍 **Cálculo de posição** (esquerda, direita, frente) e distância (próximo, distante)
- 🖥️ **Interface visual** com caixas de detecção coloridas
- 🔒 **100% offline** - funciona sem conexão com internet
- ⚡ **Otimizado para Snapdragon** - preparado para NPU

### 🛠️ Tecnologias Utilizadas

- **YOLO v8** (Ultralytics) - Detecção de objetos
- **OpenCV** - Processamento de vídeo e interface
- **pyttsx3** - Síntese de voz em português
- **NumPy** - Processamento numérico
- **Threading** - Processamento paralelo
- **Python 3.8+** - Linguagem principal

## 👥 Equipe

| Nome | E-mail |
|------|--------|
| **Luiz Felipe** | luizfmc12@gmail.com |
| **Giovanni Ghiotto** | giovannighiotto10@gmail.com |
| **Daniela Oliveira** | danyela7519@gmail.com |
| **Flavio Diniz Fontanesi** | flavio.d.fontanesi@gmail.com |
| **Guilherme Soares Leite Coelho** | guilhermeslcoelho@gmail.com |
| **Arlen Ricardo Pereira** | arlen.ricardo@gmail.com |

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Webcam conectada
- Windows (para síntese de voz nativa)
- 4GB RAM mínimo

### 1. Clone o repositório

```bash
git clone https://github.com/of3lps/assistente-acessibilidade-visual.git
cd assistente-acessibilidade-visual
```

### 2. Instale as dependências

```bash
pip install -r requirements_final.txt
```

### 3. Execute o sistema

```bash
python assistente_com_voz.py
```

## 📖 Como Usar

1. **Inicie o programa** executando `python assistente_com_voz.py`
2. **Posicione a câmera** para capturar o ambiente desejado
3. **Escute os anúncios** em português sobre objetos detectados
4. **Pressione 'q'** para encerrar o programa

### Exemplos de Anúncios

- *"pessoa muito próximo na frente"*
- *"carro próximo na direita"*
- *"ônibus distante na esquerda"*
- *"semáforo na frente"*

## 🏗️ Arquitetura do Sistema

```
assistente_com_voz.py
├── YOLO v8 (Detecção)
├── OpenCV (Vídeo/Interface)
├── Algoritmos Proprietários
│   ├── Cálculo de Posição
│   └── Estimativa de Distância
├── pyttsx3 (Síntese de Voz)
└── Threading (Processamento Paralelo)
```

## 📊 Performance

- **Latência**: ~200ms por detecção
- **FPS**: 30 (câmera) + 6 (processamento)
- **Precisão**: 85%+ em condições normais
- **Consumo**: CPU moderado, otimizado para mobile

## 🔧 Configuração Avançada

### Ajustar Sensibilidade
```python
# No arquivo assistente_com_voz.py, linha 45
if conf > 0.4:  # Altere para 0.3 (mais sensível) ou 0.6 (menos sensível)
```

### Modificar Frequência de Processamento
```python
# Linha 140
if frame_count % 5 == 0:  # Altere 5 para processar mais/menos frames
```

### Personalizar Velocidade da Voz
```python
# Linha 18
self.tts.setProperty('rate', 150)  # Altere para 100-200
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrão de Commits (Conventional Commits)

- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` tarefas de build/config

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🏆 Edge AI Developer Hackathon

Projeto desenvolvido para o **Edge AI Developer Hackathon** com foco em **acessibilidade** e **inclusão digital**.

### Objetivos Alcançados

- ✅ Sistema funcional de acessibilidade visual
- ✅ Detecção de objetos em tempo real
- ✅ Síntese de voz em português
- ✅ Interface intuitiva e responsiva
- ✅ Código otimizado para Snapdragon
- ✅ Solução 100% offline

## 📞 Suporte

Para dúvidas, sugestões ou problemas:

- 📧 E-mail: luizfmc12@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/of3lps/assistente-acessibilidade-visual/issues)
- 📖 Wiki: [Documentação Completa](https://github.com/of3lps/assistente-acessibilidade-visual/wiki)

---

**"Transformando visão artificial em independência real"** 🦾

Desenvolvido com ❤️ para a comunidade de pessoas com deficiência visual.