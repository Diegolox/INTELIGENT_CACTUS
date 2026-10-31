@echo off
setlocal
rem Todo se resuelve desde la carpeta del BAT, incluso si contiene espacios.
set "RAIZ=%~dp0"
set "SALIDA=%RAIZ%INTELIGENT_CACTUS"
set "TEMPORALES=%TEMP%\InteligentCactus-build-%RANDOM%-%RANDOM%"
set "PYTHON_BUILD=%TEMPORALES%\venv\Scripts\python.exe"

if not exist "%RAIZ%CODE\main.py" goto :faltan_archivos
if not exist "%RAIZ%CODE\network\receiver.py" goto :faltan_archivos
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: instala Python y activa la opcion de agregarlo al PATH.
    goto :error
)

echo [1/4] Preparando herramientas fuera de CODE...
python -m venv "%TEMPORALES%\venv"
if errorlevel 1 goto :error
"%PYTHON_BUILD%" -m pip install pyinstaller -r "%RAIZ%CODE\requirements.txt"
if errorlevel 1 goto :error

echo [2/4] Compilando la aplicacion...
"%PYTHON_BUILD%" -m PyInstaller ^
    --noconfirm --clean --onedir --console ^
    --name INTELIGENT_CACTUS ^
    --contents-directory _internal ^
    --distpath "%TEMPORALES%\dist" ^
    --workpath "%TEMPORALES%\build" ^
    --specpath "%TEMPORALES%" ^
    --paths "%RAIZ%CODE" ^
    --collect-all customtkinter ^
    --hidden-import socket ^
    --add-data "%RAIZ%CODE\ui\theme.json;ui" ^
    --icon "%RAIZ%assets\cactus-smooth.ico" ^
    "%RAIZ%CODE\main.py"
if errorlevel 1 goto :error

echo [3/4] Copiando el ejecutable y los recursos...
rem /E actualiza archivos sin borrar medidas ni otros archivos del usuario.
robocopy "%TEMPORALES%\dist\INTELIGENT_CACTUS" "%SALIDA%" /E /R:1 /W:1 /NFL /NDL /NJH /NJS
if errorlevel 8 goto :error
robocopy "%RAIZ%assets" "%SALIDA%\assets" /E /R:1 /W:1 /NFL /NDL /NJH /NJS
if errorlevel 8 goto :error

rem El receptor ahora esta integrado en el ejecutable.
if exist "%SALIDA%\recibir.py" del /Q "%SALIDA%\recibir.py"

echo [4/4] Terminado.
echo Ejecutable: "%SALIDA%\INTELIGENT_CACTUS.exe"
echo Para compartirlo, copia la carpeta INTELIGENT_CACTUS completa.
echo Los temporales estan en: "%TEMPORALES%"
if /I not "%~1"=="/sin-pausa" pause
exit /b 0

:faltan_archivos
echo ERROR: coloca este BAT junto a CODE y assets.
:error
echo No se pudo crear el ejecutable. Revisa el mensaje anterior.
if /I not "%~1"=="/sin-pausa" pause
exit /b 1
