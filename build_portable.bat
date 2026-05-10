@echo off
title Compilar TraductorData Launchbox Portable

echo.
echo ===============================================
echo   COMPILANDO VERSION PORTATIL
echo ===============================================
echo.

cd /d "%~dp0"

if not exist venv (
    echo Creando entorno virtual...
    py -m venv venv
)

call venv\Scripts\activate

echo.
echo Instalando dependencias...
pip install --upgrade pip

pip install ^
pyinstaller ^
transformers ^
torch ^
sentencepiece ^
ctranslate2 ^
lxml ^
langdetect ^
psutil

echo.
echo Generando ejecutable portable...
pyinstaller ^
--noconfirm ^
--clean ^
--onedir ^
--windowed ^
--name "TraductorData_Launchbox" ^
--collect-all transformers ^
--collect-all ctranslate2 ^
--collect-all sentencepiece ^
--hidden-import=tkinter ^
--hidden-import=lxml ^
--hidden-import=langdetect ^
main.py

echo.
echo ===============================================
echo   COPIANDO RECURSOS
echo ===============================================
echo.

xcopy /E /I /Y models dist\TraductorData_Launchbox_RC\models
xcopy /E /I /Y cache dist\TraductorData_Launchbox_RC\cache
xcopy /E /I /Y input dist\TraductorData_Launchbox_RC\input
xcopy /E /I /Y output dist\TraductorData_Launchbox_RC\output
xcopy /E /I /Y backups dist\TraductorData_Launchbox_RC\backups
xcopy /E /I /Y logs dist\TraductorData_Launchbox_RC\logs

copy gamer_dictionary.json dist\TraductorData_Launchbox_RC\
copy settings.json dist\TraductorData_Launchbox_RC\

echo.
echo ===============================================
echo   LISTO
echo ===============================================
echo.
echo El ejecutable portable esta en:
echo dist\TraductorData_Launchbox_RC
echo.
pause