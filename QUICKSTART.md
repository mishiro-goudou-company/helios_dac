# Helios DAC ILD Player - クイックスタートガイド

このガイドでは、各プラットフォームで最速で ILD ファイルを再生する方法を説明します。

## 📦 含まれているファイル

### Python スクリプト
- `ild_parser.py` - ILD ファイルパーサー
- `helios_ild_player.py` - メインプレーヤー
- `test_helios.py` - 接続テスト

### セットアップスクリプト
- `setup_windows.bat` - Windows 自動セットアップ（ダブルクリック）
- `setup_linux.sh` - Linux セットアップスクリプト
- `requirements.txt` - Python 依存関係

### 実行スクリプト
- `play_ild.bat` - Windows 簡易実行（ダブルクリックまたはコマンドライン）
- `play_ild.sh` - macOS/Linux 簡易実行

### ドキュメント
- `ILD_PLAYER_README.md` - 詳細な説明書
- `WINDOWS_SETUP.md` - Windows 詳細セットアップガイド
- `QUICKSTART.md` - このファイル

## 🚀 クイックスタート

### Windows

```cmd
1. setup_windows.bat をダブルクリック（または右クリック→管理者として実行）
2. play_ild.bat をダブルクリックして使い方を確認
3. ILD ファイルを play_ild.bat にドラッグ&ドロップ
```

または、コマンドラインで：
```cmd
setup_windows.bat
play_ild.bat your_animation.ild
```

### macOS

```bash
# ターミナルで実行
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 接続テスト
python test_helios.py

# ILD ファイルを再生
python helios_ild_player.py your_animation.ild

# または実行スクリプトを使用
chmod +x play_ild.sh
./play_ild.sh your_animation.ild
```

### Linux

```bash
# セットアップスクリプトを実行
chmod +x setup_linux.sh
./setup_linux.sh

# 接続テスト（udev ルール設定済みの場合）
source venv/bin/activate
python test_helios.py

# ILD ファイルを再生
python helios_ild_player.py your_animation.ild

# または実行スクリプトを使用
./play_ild.sh your_animation.ild
```

## 💡 よくある使い方

### パラメータを指定して再生

```bash
# 書式
python helios_ild_player.py <ILDファイル> [PPS] [ループ回数]

# 例：30000 PPS で 5回ループ
python helios_ild_player.py animation.ild 30000 5

# 例：無限ループ
python helios_ild_player.py animation.ild 30000 -1
```

### Windows バッチファイルで再生

```cmd
REM ファイルをドラッグ&ドロップ
play_ild.bat animation.ild

REM パラメータ付き
play_ild.bat animation.ild 30000 5
```

## 🔧 必要なファイル（OS別）

### Windows で必要なファイル

プロジェクトのルートディレクトリに以下のファイルが必要：

```
HeliosLaserDAC.dll      ← sdk/cpp/shared_library/ からコピー
libusb-1.0.dll          ← sdk/cpp/libusb_bin/Windows/x64/Release/dll/ からコピー
```

**setup_windows.bat が自動的にコピーします**

### macOS で必要なファイル

```
libHeliosLaserDAC.dylib ← sdk/cpp/shared_library/ にあります
```

### Linux で必要なファイル

```
libHeliosDacAPI.so      ← sdk/cpp/shared_library/ にビルドが必要
libusb-1.0              ← パッケージマネージャーでインストール
```

## ❓ トラブルシューティング

### "DAC が検出されませんでした"

1. Helios DAC が USB で接続されているか確認
2. 他のアプリケーションが使用していないか確認
3. USB ケーブルとポートを変更してみる
4. 接続テストを実行: `python test_helios.py`

### Windows: "DLL load failed"

Visual C++ Redistributable をインストール:
https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist

### Linux: "Permission denied"

udev ルールを設定するか、sudo で実行:
```bash
sudo python test_helios.py
```

詳細: `docs/udev_rules_for_linux.md`

## 📚 詳細ドキュメント

- **詳細な使い方**: [ILD_PLAYER_README.md](ILD_PLAYER_README.md)
- **Windows セットアップ**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md)
- **Helios DAC SDK**: [sdk/README.md](sdk/README.md)

## 🎯 推奨設定

### PPS (Points Per Second) の選び方

| アニメーションの種類 | 推奨 PPS |
|---------------------|---------|
| シンプルな図形 | 20000-25000 |
| 標準的なアニメーション | 30000 |
| 複雑な図形 | 35000-40000 |
| 高速スキャン | 40000+ |

### ループ回数

- **テスト**: 1-3 回
- **プレビュー**: 5-10 回
- **デモ**: 10-50 回
- **連続再生**: -1（無限ループ）

## 📝 GitHub へのコミット準備

以下のファイルを Git に追加してコミット：

```bash
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
git add .gitignore

git commit -m "Add ILD Player for Helios DAC"
git push
```

**注意**: `venv/` ディレクトリは `.gitignore` により自動的に除外されます。

## ⚡ 1分でスタート（macOS の例）

```bash
cd /path/to/helios_dac-1
python3 -m venv venv
source venv/bin/activate
pip install numpy
python test_helios.py
python helios_ild_player.py your_file.ild
```

完了！🎉

