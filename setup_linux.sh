#!/bin/bash
# Helios DAC ILD Player - Linux セットアップスクリプト

echo "====================================="
echo "Helios DAC ILD Player - Linux Setup"
echo "====================================="
echo ""

# libusb のチェック
echo "[1/4] libusb のチェック中..."
if ldconfig -p | grep -q libusb-1.0; then
    echo "  ✓ libusb-1.0 が見つかりました"
else
    echo "  ✗ libusb-1.0 が見つかりません"
    echo ""
    echo "libusb-1.0 をインストールしてください:"
    echo "  Ubuntu/Debian: sudo apt install libusb-1.0-0-dev"
    echo "  Fedora/CentOS: sudo dnf install libusb-devel"
    echo "  Arch Linux:    sudo pacman -S libusb"
    echo ""
    read -p "続行しますか? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# Python のバージョン確認
echo "[2/4] Python のバージョン確認中..."
if command -v python3 &> /dev/null; then
    python3 --version
    echo "  ✓ Python が見つかりました"
else
    echo "  ✗ Python3 が見つかりません"
    echo ""
    echo "Python3 をインストールしてください:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo ""
    exit 1
fi
echo ""

# 仮想環境の作成
echo "[3/4] Python 仮想環境を作成中..."
if [ -d "venv" ]; then
    echo "  仮想環境は既に存在します"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "  ✓ 仮想環境を作成しました"
    else
        echo "  ✗ 仮想環境の作成に失敗"
        exit 1
    fi
fi
echo ""

# 依存関係のインストール
echo "[4/4] Python ライブラリをインストール中..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "  ✓ 依存関係をインストールしました"
else
    echo "  ✗ 依存関係のインストールに失敗"
    exit 1
fi
echo ""

# udev ルールのチェック
echo "====================================="
echo "udev ルールの確認"
echo "====================================="
echo ""
echo "Helios DAC を非 root ユーザーで使用するには、udev ルールの設定が推奨されます。"
echo "設定方法: docs/udev_rules_for_linux.md を参照"
echo ""
if [ -f "/etc/udev/rules.d/99-helios.rules" ]; then
    echo "  ✓ udev ルールが設定されています"
else
    echo "  ℹ udev ルールが設定されていません（sudo で実行する必要があります）"
fi
echo ""

# 完了メッセージ
echo "====================================="
echo "セットアップ完了！"
echo "====================================="
echo ""
echo "次のステップ:"
echo ""
echo "1. 接続テスト:"
echo "   source venv/bin/activate"
echo "   python test_helios.py"
echo ""
echo "   (udev ルール未設定の場合: sudo python test_helios.py)"
echo ""
echo "2. ILD ファイルを再生:"
echo "   source venv/bin/activate"
echo "   python helios_ild_player.py your_file.ild"
echo ""
echo "または実行スクリプトを使用:"
echo "   ./play_ild.sh your_file.ild 30000 10"
echo ""

