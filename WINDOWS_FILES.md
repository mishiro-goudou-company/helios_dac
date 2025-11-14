# Windows で必要なファイル一覧

このドキュメントでは、Windows 環境で Helios DAC ILD Player を使用するために必要なすべてのファイルをリストアップしています。

## ✅ GitHub リポジトリに含めるべきファイル

以下のファイルは **すでにリポジトリに含まれています**（または含めるべきです）:

### Python スクリプト
- ✅ `ild_parser.py` - ILD ファイルパーサー
- ✅ `helios_ild_player.py` - メインプレーヤー  
- ✅ `test_helios.py` - 接続テスト
- ✅ `requirements.txt` - Python 依存関係

### セットアップ・実行スクリプト
- ✅ `setup_windows.bat` - Windows 自動セットアップ
- ✅ `play_ild.bat` - Windows 簡易実行
- ✅ `setup_linux.sh` - Linux セットアップ
- ✅ `play_ild.sh` - macOS/Linux 実行

### ドキュメント
- ✅ `ILD_PLAYER_README.md` - メインドキュメント
- ✅ `WINDOWS_SETUP.md` - Windows セットアップガイド
- ✅ `QUICKSTART.md` - クイックスタートガイド
- ✅ `WINDOWS_FILES.md` - このファイル

### Helios DAC ライブラリ（既存）
- ✅ `sdk/cpp/shared_library/HeliosLaserDAC.dll` - Windows 64-bit
- ✅ `sdk/cpp/shared_library/HeliosLaserDAC-x86.dll` - Windows 32-bit
- ✅ `sdk/cpp/shared_library/libHeliosLaserDAC.dylib` - macOS
- ✅ `sdk/cpp/libusb_bin/Windows/x64/Release/dll/libusb-1.0.dll` - libusb 64-bit
- ✅ `sdk/cpp/libusb_bin/Windows/Win32/Release/dll/libusb-1.0.dll` - libusb 32-bit
- ✅ `sdk/cpp/libusb_bin/macOS/libusb-1.0.0.dylib` - libusb macOS

### Git 設定
- ✅ `.gitignore` - Python 仮想環境を除外（更新済み）

## 📂 Windows でのディレクトリ構造

### セットアップ前
```
helios_dac-1/
├── setup_windows.bat          ← これを実行
├── play_ild.bat
├── ild_parser.py
├── helios_ild_player.py
├── test_helios.py
├── requirements.txt
├── ILD_PLAYER_README.md
├── WINDOWS_SETUP.md
├── QUICKSTART.md
└── sdk/
    └── cpp/
        ├── shared_library/
        │   ├── HeliosLaserDAC.dll           ← 64-bit 版
        │   └── HeliosLaserDAC-x86.dll       ← 32-bit 版
        └── libusb_bin/
            └── Windows/
                ├── x64/Release/dll/
                │   └── libusb-1.0.dll        ← 64-bit 版
                └── Win32/Release/dll/
                    └── libusb-1.0.dll        ← 32-bit 版
```

### セットアップ後（setup_windows.bat 実行後）
```
helios_dac-1/
├── HeliosLaserDAC.dll         ← コピーされた（64-bit）
├── libusb-1.0.dll             ← コピーされた（64-bit）
├── venv/                      ← 作成された（.gitignore で除外）
├── setup_windows.bat
├── play_ild.bat
├── (その他のファイル...)
└── sdk/                       ← 元のファイルはそのまま
```

## 🎯 Windows ユーザーが実行する手順

### ステップ 1: リポジトリをクローン
```cmd
git clone https://github.com/YOUR_USERNAME/helios_dac.git
cd helios_dac
```

### ステップ 2: セットアップ
```cmd
setup_windows.bat
```

このバッチファイルが自動的に：
1. システムアーキテクチャを検出（32-bit または 64-bit）
2. 適切な DLL を `sdk/cpp/` からルートディレクトリにコピー
3. Python 仮想環境を作成
4. 必要な Python ライブラリをインストール

### ステップ 3: 使用
```cmd
REM 接続テスト
venv\Scripts\activate
python test_helios.py

REM ILD ファイルを再生
play_ild.bat your_animation.ild
```

## 📋 GitHub にコミットする前のチェックリスト

```bash
# 新規ファイルを追加
git add ild_parser.py
git add helios_ild_player.py
git add test_helios.py
git add requirements.txt
git add setup_windows.bat
git add setup_linux.sh
git add play_ild.bat
git add play_ild.sh
git add ILD_PLAYER_README.md
git add WINDOWS_SETUP.md
git add QUICKSTART.md
git add WINDOWS_FILES.md

# .gitignore の変更を追加
git add .gitignore

# 確認
git status

# コミット
git commit -m "Add ILD Player with cross-platform support

- Add ILD file parser supporting ILDA formats 0, 1, 4, 5
- Add Helios DAC player with auto-detection of platform
- Add setup scripts for Windows, macOS, Linux
- Add comprehensive documentation
- Update .gitignore to exclude Python venv"

# プッシュ
git push origin master
```

## ⚠️ 重要な注意事項

### GitHub に含めない（.gitignore で除外）
- ❌ `venv/` - Python 仮想環境
- ❌ `__pycache__/` - Python キャッシュ
- ❌ `*.pyc` - コンパイル済み Python ファイル
- ❌ `.env` - 環境変数ファイル

### GitHub に含める（既存のファイル）
- ✅ `sdk/cpp/shared_library/*.dll` - Helios ライブラリ
- ✅ `sdk/cpp/libusb_bin/` - libusb ライブラリ

これらのバイナリファイルは元々リポジトリに含まれているため、そのまま維持します。

## 🔍 ファイルサイズ確認

```cmd
REM Windows で実行
dir sdk\cpp\shared_library\*.dll
dir sdk\cpp\libusb_bin\Windows\x64\Release\dll\*.dll
```

主要な DLL ファイル:
- `HeliosLaserDAC.dll`: 約 300KB
- `libusb-1.0.dll`: 約 60-100KB

これらは GitHub の制限（100MB/ファイル）内に収まるため、問題ありません。

## 📝 README への追記案

メインの `README.md` に以下のセクションを追加することを推奨：

```markdown
## ILD Player

This repository now includes a Python-based ILD player for easy playback of ILDA files.

### Quick Start

**Windows:**
```cmd
setup_windows.bat
play_ild.bat your_file.ild
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python helios_ild_player.py your_file.ild
```

See [ILD_PLAYER_README.md](ILD_PLAYER_README.md) for detailed instructions.
```

## ✨ 完了！

これで、Windows を含むすべてのプラットフォームで、他のユーザーが簡単に ILD ファイルを再生できるようになりました！

