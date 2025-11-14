# Windows で ILD プレーヤーを使用する方法

このガイドでは、Windows 環境で Helios DAC ILD プレーヤーをセットアップして使用する方法を説明します。

## 必要なファイル

### 1. Helios DAC ライブラリ（既にリポジトリに含まれています）

**64-bit Windows の場合:**
```
sdk/cpp/shared_library/HeliosLaserDAC.dll
sdk/cpp/libusb_bin/Windows/x64/Release/dll/libusb-1.0.dll
```

**32-bit Windows の場合:**
```
sdk/cpp/shared_library/HeliosLaserDAC-x86.dll
sdk/cpp/libusb_bin/Windows/Win32/Release/dll/libusb-1.0.dll
```

### 2. Python スクリプト（このリポジトリに含まれています）
```
ild_parser.py           # ILD ファイルパーサー
helios_ild_player.py    # Helios DAC プレーヤー
test_helios.py          # 接続テスト
```

## セットアップ手順

### ステップ 1: Python のインストール

1. [Python 公式サイト](https://www.python.org/downloads/) から Python 3.8 以降をダウンロード
2. インストール時に **"Add Python to PATH"** にチェックを入れる

### ステップ 2: 必要なライブラリのコピー

**64-bit Windows の場合:**

```cmd
REM プロジェクトのルートディレクトリで実行
copy sdk\cpp\shared_library\HeliosLaserDAC.dll .
copy sdk\cpp\libusb_bin\Windows\x64\Release\dll\libusb-1.0.dll .
```

**32-bit Windows の場合:**

```cmd
REM プロジェクトのルートディレクトリで実行
copy sdk\cpp\shared_library\HeliosLaserDAC-x86.dll HeliosLaserDAC.dll
copy sdk\cpp\libusb_bin\Windows\Win32\Release\dll\libusb-1.0.dll .
```

### ステップ 3: Python 仮想環境のセットアップ

```cmd
REM プロジェクトのルートディレクトリで実行
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install numpy
```

### ステップ 4: 接続テスト

Helios DAC が正常に認識されているか確認：

```cmd
python test_helios.py
```

成功すると以下のような出力が表示されます：
```
✓ ライブラリのロードに成功
✓ 検出されたデバイス数: 1
デバイス情報:
  デバイス 0:
    名前: Helios XXXXXXXX
    ファームウェア: X
✓ テスト完了
```

## 使用方法

### ILD ファイルの再生

```cmd
REM 基本的な使用方法（10 ループ）
python helios_ild_player.py your_file.ild

REM PPS とループ回数を指定
python helios_ild_player.py your_file.ild 30000 3

REM 無限ループ
python helios_ild_player.py your_file.ild 30000 -1
```

### パラメータ

1. **ILD ファイル**: 再生する ILD ファイルのパス（必須）
2. **PPS** (Points Per Second): 1秒あたりのポイント数（デフォルト: 30000）
   - 推奨範囲: 20000 ～ 40000
3. **ループ回数**: 繰り返し再生する回数（デフォルト: 10、-1 で無限ループ）

### 停止方法

再生中に **`Ctrl + C`** を押すと停止します。

## ディレクトリ構造（実行時）

```
helios_dac-1/
├── HeliosLaserDAC.dll          # Helios DAC ライブラリ（コピーしたもの）
├── libusb-1.0.dll               # libusb ライブラリ（コピーしたもの）
├── ild_parser.py                # ILD パーサー
├── helios_ild_player.py         # プレーヤー
├── test_helios.py               # テストスクリプト
├── your_file.ild                # 再生する ILD ファイル
├── venv/                        # Python 仮想環境
└── sdk/                         # SDK（元のファイル）
```

## トラブルシューティング

### エラー: "DLL load failed"

**原因:** Visual C++ ランタイムがインストールされていない

**解決策:**
1. [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist) をダウンロード
2. 使用している Windows のアーキテクチャ（x64 または x86）に合わせてインストール

### エラー: "Helios DAC が検出されませんでした"

**確認事項:**
1. Helios DAC が USB で正しく接続されているか
2. デバイスマネージャーで認識されているか
3. 他のアプリケーションが DAC を使用していないか
4. USB ケーブルとポートを変えてみる

### エラー: "ライブラリが見つかりません"

**解決策:**
- `HeliosLaserDAC.dll` と `libusb-1.0.dll` がスクリプトと同じディレクトリにあることを確認
- または、システムの PATH に DLL のディレクトリを追加

## 必要な Windows システム要件

- **OS**: Windows 7 以降（Windows 10/11 推奨）
- **Python**: 3.8 以降
- **アーキテクチャ**: 32-bit または 64-bit（Helios DAC ライブラリに合わせる）
- **追加要件**: Microsoft Visual C++ Redistributable

## バッチファイルの例

セットアップを簡単にするため、以下のバッチファイルを作成できます：

**setup_windows.bat**:
```batch
@echo off
echo Helios DAC ILD Player - Windows セットアップ

REM DLL をコピー（64-bit の場合）
copy sdk\cpp\shared_library\HeliosLaserDAC.dll .
copy sdk\cpp\libusb_bin\Windows\x64\Release\dll\libusb-1.0.dll .

REM Python 仮想環境を作成
python -m venv venv
call venv\Scripts\activate

REM 依存関係をインストール
pip install --upgrade pip
pip install numpy

echo.
echo セットアップ完了！
echo 接続テストを実行するには: python test_helios.py
echo ILD ファイルを再生するには: python helios_ild_player.py your_file.ild
pause
```

**play_ild.bat**:
```batch
@echo off
call venv\Scripts\activate
python helios_ild_player.py %*
pause
```

使用例:
```cmd
play_ild.bat my_animation.ild 30000 5
```

