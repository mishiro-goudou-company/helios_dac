#!/bin/bash
# Helios DAC ILD Player - 簡易実行スクリプト（macOS/Linux）
# 使用例: ./play_ild.sh my_animation.ild 30000 10

if [ $# -eq 0 ]; then
    echo "使用方法: ./play_ild.sh <ILDファイル> [PPS] [ループ回数]"
    echo ""
    echo "例:"
    echo "  ./play_ild.sh animation.ild"
    echo "  ./play_ild.sh animation.ild 30000 5"
    echo "  ./play_ild.sh animation.ild 30000 -1    # 無限ループ"
    echo ""
    exit 1
fi

# 仮想環境をアクティベート
source venv/bin/activate

# Python スクリプトを実行
python helios_ild_player.py "$@"

# エラーコードをチェック
if [ $? -ne 0 ]; then
    echo ""
    echo "エラーが発生しました"
fi

