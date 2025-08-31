@echo off
echo Instalando dependencias com --user...
python -m pip install --user --upgrade pip
python -m pip install --user opencv-python==4.8.1.78
python -m pip install --user ultralytics==8.0.196
python -m pip install --user torch==2.0.1
python -m pip install --user torchvision==0.15.2
python -m pip install --user pyttsx3==2.90
python -m pip install --user numpy==1.24.3
python -m pip install --user pillow==10.0.1
python -m pip install --user easyocr==1.7.0
echo.
echo Instalacao concluida!
echo Execute: python main.py
pause