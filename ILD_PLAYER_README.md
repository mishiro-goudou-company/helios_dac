# Helios DAC ILD Player

Helios DAC 用の ILD (ILDA) ファイルプレーヤーです。ILD ファイルを読み込んで Helios DAC でレーザーアニメーションを再生できます。

## 特徴

- ✅ **クロスプラットフォーム対応**: Windows、macOS、Linux で動作
- ✅ **ILD フォーマット対応**: ILDA 標準フォーマット（Format 0, 1, 4, 5）をサポート
- ✅ **簡単セットアップ**: Python と必要なライブラリのみで動作
- ✅ **柔軟な再生オプション**: PPS やループ回数を自由に設定可能

## 対応フォーマット

- Format 0: 3D 座標 + インデックスカラー
- Format 1: 2D 座標 + インデックスカラー
- Format 4: 3D 座標 + True Color
- Format 5: 2D 座標 + True Color

## クイックスタート

### macOS

```bash
# セットアップ
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 接続テスト
python test_helios.py

# ILD ファイルを再生
python helios_ild_player.py your_file.ild
```

### Windows

```cmd
REM 自動セットアップ
setup_windows.bat

REM 接続テスト
venv\Scripts\activate
python test_helios.py

REM ILD ファイルを再生（簡易版）
play_ild.bat your_file.ild
```

詳細な Windows セットアップ手順は [WINDOWS_SETUP.md](WINDOWS_SETUP.md) を参照してください。

### Linux

```bash
# libusb のインストール
sudo apt install libusb-1.0-0-dev

# セットアップ
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 接続テスト（udev ルールを設定していない場合は sudo が必要）
python test_helios.py

# ILD ファイルを再生
python helios_ild_player.py your_file.ild
```

## 使用方法

### 基本的な使い方

```bash
python helios_ild_player.py <ILDファイル> [PPS] [ループ回数]
```

### パラメータ

1. **ILD ファイル**（必須）
   - 再生する ILD ファイルのパス

2. **PPS** - Points Per Second（オプション、デフォルト: 30000）
   - 1秒あたりのポイント数
   - 推奨範囲: 20000 ～ 40000
   - 値が高いほど滑らかだが、複雑な図形では低めが良い

3. **ループ回数**（オプション、デフォルト: 10）
   - 繰り返し再生する回数
   - `-1` で無限ループ

### 使用例

```bash
# デフォルト設定で再生（30000 PPS、10ループ）
python helios_ild_player.py animation.ild

# 20000 PPS で 3回ループ
python helios_ild_player.py animation.ild 20000 3

# 無限ループ
python helios_ild_player.py animation.ild 30000 -1
```

### 停止方法

再生中に **`Ctrl + C`** を押すと停止します。

## ファイル構成

```
helios_dac-1/
├── ild_parser.py              # ILD ファイルパーサー
├── helios_ild_player.py       # Helios DAC プレーヤー
├── test_helios.py             # 接続テストスクリプト
├── requirements.txt           # Python 依存関係
├── ILD_PLAYER_README.md       # このファイル
├── WINDOWS_SETUP.md           # Windows セットアップガイド
├── setup_windows.bat          # Windows 自動セットアップ
├── play_ild.bat               # Windows 簡易実行スクリプト
└── sdk/                       # Helios DAC SDK
    └── cpp/
        ├── shared_library/
        │   ├── libHeliosLaserDAC.dylib  # macOS ライブラリ
        │   ├── HeliosLaserDAC.dll       # Windows 64-bit ライブラリ
        │   └── HeliosLaserDAC-x86.dll   # Windows 32-bit ライブラリ
        └── libusb_bin/                   # libusb ライブラリ
```

## 必要な環境

### 共通
- Python 3.8 以降
- numpy
- Helios DAC ハードウェア

### OS 別の追加要件

**macOS:**
- libusb (Homebrew でインストール: `brew install libusb`)

**Windows:**
- Microsoft Visual C++ Redistributable
- libusb-1.0.dll（SDK に含まれています）

**Linux:**
- libusb-1.0-0-dev (`sudo apt install libusb-1.0-0-dev`)
- udev ルールの設定（推奨）

## トラブルシューティング

### "DAC が検出されませんでした"

**確認事項:**
1. Helios DAC が USB で正しく接続されているか
2. 他のアプリケーションが DAC を使用していないか
3. USB ケーブルとポートを変えてみる

**Linux の場合:**
- udev ルールを設定していない場合は `sudo` で実行
- udev ルール設定方法は `docs/udev_rules_for_linux.md` を参照

### "ライブラリが見つかりません"

**解決策:**
- 必要な DLL/dylib/so ファイルがカレントディレクトリまたは適切な場所にあることを確認
- Windows の場合: `setup_windows.bat` を実行してファイルをコピー

### Windows で "DLL load failed"

**原因:** Visual C++ ランタイムがインストールされていない

**解決策:**
[Microsoft Visual C++ Redistributable](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist) をインストール

## ILD ファイルの取得

ILD ファイルは以下の方法で取得できます:

1. **レーザーショーソフトウェアから出力**
   - LaserOS
   - Pangolin QuickShow / BEYOND
   - Spaghetti

2. **オンラインリソース**
   - ILDA のサンプルファイル
   - レーザーアニメーションコミュニティ

3. **自作**
   - ILDA フォーマット仕様に基づいて作成
   - 3D モデリングソフトから変換

## 技術仕様

### ILD パーサー (`ild_parser.py`)

- ILDA 標準フォーマットのバイナリファイルをパース
- 3D/2D 座標、インデックスカラー/True Color に対応
- ブランキング（レーザーオフ）をサポート

### Helios プレーヤー (`helios_ild_player.py`)

- Helios DAC SDK の C ライブラリを ctypes 経由で呼び出し
- 自動的に座標系を変換（ILDA 形式 → Helios 形式）
- ダブルバッファリングで滑らかな再生
- ステータスポーリングによる同期

## ライセンス

このプロジェクトは元の Helios DAC SDK のライセンスに従います。
詳細は [LICENSE.md](LICENSE.md) を参照してください。

## 参考リンク

- [Helios DAC 公式リポジトリ](https://github.com/Grix/helios_dac)
- [ILDA (International Laser Display Association)](https://www.ilda.com/)
- [ILDA Digital Network (IDN)](http://ilda-digital.com/)

## 貢献

バグ報告、機能リクエスト、プルリクエストを歓迎します！

## 作成者

ILD Player: 2025
Based on: Helios DAC SDK by Gitle Mikkelsen

