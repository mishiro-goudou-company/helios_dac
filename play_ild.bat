@echo off
REM Helios DAC ILD Player - 簡易実行スクリプト
REM 使用例: play_ild.bat my_animation.ild 30000 10

if "%1"=="" (
    echo 使用方法: play_ild.bat ^<ILDファイル^> [PPS] [ループ回数]
    echo.
    echo 例:
    echo   play_ild.bat animation.ild
    echo   play_ild.bat animation.ild 30000 5
    echo   play_ild.bat animation.ild 30000 -1    ^(無限ループ^)
    echo.
    pause
    exit /b 1
)

REM 仮想環境をアクティベート
call venv\Scripts\activate

REM Python スクリプトを実行
python helios_ild_player.py %*

REM エラーコードをチェック
if errorlevel 1 (
    echo.
    echo エラーが発生しました
    pause
)

