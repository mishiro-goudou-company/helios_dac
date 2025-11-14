#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helios DAC ILD ファイルプレーヤー
ILD ファイルを読み込んで Helios DAC で再生します
"""

import ctypes
import time
import os
import sys
import platform
from ild_parser import ILDParser

# HeliosPoint 構造体の定義
class HeliosPoint(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_uint16),
        ('y', ctypes.c_uint16),
        ('r', ctypes.c_uint8),
        ('g', ctypes.c_uint8),
        ('b', ctypes.c_uint8),
        ('i', ctypes.c_uint8)
    ]

class HeliosILDPlayer:
    """Helios DAC ILD プレーヤー"""
    
    def __init__(self, library_path: str = None):
        """
        初期化
        
        Args:
            library_path: Helios DAC ライブラリのパス
        """
        # ライブラリパスを自動検出
        if library_path is None:
            system = platform.system()
            
            if system == "Darwin":  # macOS
                possible_paths = [
                    "./sdk/cpp/shared_library/libHeliosLaserDAC.dylib",
                    "./libHeliosLaserDAC.dylib",
                    "/usr/local/lib/libHeliosLaserDAC.dylib",
                ]
            elif system == "Windows":
                # Windows (32-bit と 64-bit の両方を試す)
                possible_paths = [
                    "./HeliosLaserDAC.dll",
                    "./sdk/cpp/shared_library/HeliosLaserDAC.dll",
                    "./sdk/cpp/shared_library/HeliosLaserDAC-x86.dll",
                ]
            elif system == "Linux":
                possible_paths = [
                    "./libHeliosDacAPI.so",
                    "./sdk/cpp/shared_library/libHeliosDacAPI.so",
                    "/usr/local/lib/libHeliosDacAPI.so",
                ]
            else:
                possible_paths = []
            
            for path in possible_paths:
                if os.path.exists(path):
                    library_path = path
                    break
        
        if library_path is None:
            system = platform.system()
            raise FileNotFoundError(
                f"Helios DAC ライブラリが見つかりません（OS: {system}）。\n\n"
                f"必要な手順:\n"
                f"  macOS: sdk/cpp/shared_library/libHeliosLaserDAC.dylib をカレントディレクトリにコピー\n"
                f"  Windows: sdk/cpp/shared_library/HeliosLaserDAC.dll と libusb-1.0.dll をカレントディレクトリにコピー\n"
                f"  Linux: sdk/cpp/shared_library/libHeliosDacAPI.so をカレントディレクトリにコピー\n\n"
                f"詳細は WINDOWS_SETUP.md または README を参照してください。"
            )
        
        # ライブラリをロード
        try:
            self.helios_lib = ctypes.cdll.LoadLibrary(library_path)
            print(f"ライブラリをロード: {library_path}")
        except OSError as e:
            raise RuntimeError(f"ライブラリのロードに失敗: {e}")
        
        self.num_devices = 0
        
    def open_devices(self):
        """DAC デバイスを開く"""
        self.num_devices = self.helios_lib.OpenDevices()
        print(f"検出された Helios DAC 数: {self.num_devices}")
        return self.num_devices
    
    def close_devices(self):
        """DAC デバイスを閉じる"""
        self.helios_lib.CloseDevices()
        print("デバイスをクローズしました")
    
    def play_ild_file(self, ild_filename: str, pps: int = 30000, loop_count: int = 10):
        """
        ILD ファイルを再生
        
        Args:
            ild_filename: ILD ファイルのパス
            pps: Points Per Second (30000 推奨)
            loop_count: ループ回数（-1 で無限ループ）
        """
        # ILD ファイルをパース
        print(f"ILD ファイルをパース中: {ild_filename}")
        parser = ILDParser(ild_filename)
        frames = parser.parse()
        
        if not frames:
            print("エラー: フレームが見つかりません")
            return
        
        print(f"読み込んだフレーム数: {len(frames)}")
        
        # フレームを Helios フォーマットに変換
        helios_frames = []
        for i, frame in enumerate(frames):
            if not frame.points:
                continue
            
            # ポイント数の制限（Helios は最大 4095 ポイント）
            max_points = min(len(frame.points), 4095)
            points = frame.points[:max_points]
            
            # HeliosPoint 配列を作成
            frame_type = HeliosPoint * len(points)
            helios_frame = frame_type()
            
            for j, (x, y, r, g, b, blanking) in enumerate(points):
                # 座標を 0-65535 から 0-4095 にスケール（Helios は 12ビット）
                helios_frame[j].x = int((x / 65535.0) * 4095)
                helios_frame[j].y = int((y / 65535.0) * 4095)
                
                # ブランキング時は色を消す
                if blanking:
                    helios_frame[j].r = 0
                    helios_frame[j].g = 0
                    helios_frame[j].b = 0
                    helios_frame[j].i = 0
                else:
                    helios_frame[j].r = r
                    helios_frame[j].g = g
                    helios_frame[j].b = b
                    helios_frame[j].i = 255  # 輝度
            
            helios_frames.append((helios_frame, len(points)))
            
            if (i + 1) % 100 == 0:
                print(f"  {i + 1} / {len(frames)} フレームを変換...")
        
        print(f"{len(helios_frames)} フレームを変換完了")
        
        # デバイスで再生
        if self.num_devices <= 0:
            print("エラー: DAC が検出されませんでした")
            return
        
        print(f"\n再生開始...")
        print(f"  PPS: {pps}")
        print(f"  ループ回数: {'無限' if loop_count == -1 else loop_count}")
        print("  (Ctrl+C で停止)")
        
        try:
            loop_num = 0
            while loop_count == -1 or loop_num < loop_count:
                for i, (helios_frame, num_points) in enumerate(helios_frames):
                    # 各 DAC に送信
                    for device_num in range(self.num_devices):
                        # DAC が準備完了になるまで待つ
                        status_attempts = 0
                        while status_attempts < 512:
                            status = self.helios_lib.GetStatus(device_num)
                            if status == 1:
                                break
                            status_attempts += 1
                            time.sleep(0.0001)  # 100 マイクロ秒待機
                        
                        # フレームを送信
                        result = self.helios_lib.WriteFrame(
                            device_num,
                            pps,
                            0,  # flags
                            ctypes.pointer(helios_frame),
                            num_points
                        )
                        
                        if result < 0:
                            print(f"警告: フレーム送信エラー (device {device_num}): {result}")
                
                loop_num += 1
                if loop_count != -1 and loop_num % max(1, loop_count // 10) == 0:
                    print(f"  進行状況: {loop_num} / {loop_count} ループ")
        
        except KeyboardInterrupt:
            print("\n\n停止中...")
        
        # 停止
        for device_num in range(self.num_devices):
            self.helios_lib.Stop(device_num)
        
        print("再生完了")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python helios_ild_player.py <ILDファイル> [PPS] [ループ回数]")
        print("例: python helios_ild_player.py animation.ild 30000 10")
        print("    python helios_ild_player.py animation.ild 30000 -1  # 無限ループ")
        sys.exit(1)
    
    ild_file = sys.argv[1]
    pps = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
    loop_count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    if not os.path.exists(ild_file):
        print(f"エラー: ファイルが見つかりません: {ild_file}")
        sys.exit(1)
    
    # プレーヤーを作成
    player = HeliosILDPlayer()
    
    # デバイスを開く
    num_devices = player.open_devices()
    
    if num_devices <= 0:
        print("\nエラー: Helios DAC が検出されませんでした。")
        print("以下を確認してください:")
        print("1. Helios DAC が USB で接続されているか")
        print("2. macOS の場合、デバイスへのアクセス権限があるか")
        print("3. 他のアプリケーションが DAC を使用していないか")
        sys.exit(1)
    
    try:
        # ILD ファイルを再生
        player.play_ild_file(ild_file, pps, loop_count)
    finally:
        # クリーンアップ
        player.close_devices()


if __name__ == "__main__":
    main()

