@echo off
REM Helios DAC ILD Player - Windows セットアップスクリプト
REM 64-bit Windows 用

echo =====================================
echo Helios DAC ILD Player - Windows Setup
echo =====================================
echo.

REM アーキテクチャの確認
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set ARCH=x64
    echo 検出されたアーキテクチャ: 64-bit
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set ARCH=Win32
    echo 検出されたアーキテクチャ: 32-bit
) else (
    set ARCH=x64
    echo アーキテクチャを特定できません。64-bit として続行します。
)
echo.

REM DLL をコピー
echo [1/4] 必要な DLL をコピー中...

if "%ARCH%"=="x64" (
    copy /Y sdk\cpp\shared_library\HeliosLaserDAC.dll . >nul
    copy /Y sdk\cpp\libusb_bin\Windows\x64\Release\dll\libusb-1.0.dll . >nul
) else (
    copy /Y sdk\cpp\shared_library\HeliosLaserDAC-x86.dll HeliosLaserDAC.dll >nul
    copy /Y sdk\cpp\libusb_bin\Windows\Win32\Release\dll\libusb-1.0.dll . >nul
)

if exist HeliosLaserDAC.dll (
    echo   ✓ HeliosLaserDAC.dll
) else (
    echo   ✗ HeliosLaserDAC.dll のコピーに失敗
)

if exist libusb-1.0.dll (
    echo   ✓ libusb-1.0.dll
) else (
    echo   ✗ libusb-1.0.dll のコピーに失敗
)
echo.

REM Python のバージョン確認
echo [2/4] Python のバージョン確認中...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ✗ Python が見つかりません
    echo.
    echo Python をインストールしてください: https://www.python.org/downloads/
    echo インストール時に "Add Python to PATH" にチェックを入れてください
    pause
    exit /b 1
) else (
    python --version
    echo   ✓ Python が見つかりました
)
echo.

REM 仮想環境の作成
echo [3/4] Python 仮想環境を作成中...
if exist venv (
    echo   仮想環境は既に存在します
) else (
    python -m venv venv
    if errorlevel 1 (
        echo   ✗ 仮想環境の作成に失敗
        pause
        exit /b 1
    ) else (
        echo   ✓ 仮想環境を作成しました
    )
)
echo.

REM 依存関係のインストール
echo [4/4] Python ライブラリをインストール中...
call venv\Scripts\activate
pip install --upgrade pip --quiet
pip install numpy --quiet
if errorlevel 1 (
    echo   ✗ ライブラリのインストールに失敗
    pause
    exit /b 1
) else (
    echo   ✓ numpy をインストールしました
)
echo.

REM 完了メッセージ
echo =====================================
echo セットアップ完了！
echo =====================================
echo.
echo 次のステップ:
echo.
echo 1. 接続テスト:
echo    venv\Scripts\activate
echo    python test_helios.py
echo.
echo 2. ILD ファイルを再生:
echo    venv\Scripts\activate
echo    python helios_ild_player.py your_file.ild
echo.
echo または play_ild.bat を使用:
echo    play_ild.bat your_file.ild 30000 10
echo.
pause

