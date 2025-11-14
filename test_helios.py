#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helios DAC 接続テスト
"""

import ctypes
import os
import sys
import platform

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

def test_helios_connection():
    """Helios DAC 接続テスト"""
    
    # OS に応じてライブラリパスを検出
    system = platform.system()
    lib_path = None
    
    if system == "Darwin":  # macOS
        possible_paths = [
            "./sdk/cpp/shared_library/libHeliosLaserDAC.dylib",
            "./libHeliosLaserDAC.dylib",
        ]
    elif system == "Windows":
        possible_paths = [
            "./HeliosLaserDAC.dll",
            "./sdk/cpp/shared_library/HeliosLaserDAC.dll",
            "./sdk/cpp/shared_library/HeliosLaserDAC-x86.dll",
        ]
    elif system == "Linux":
        possible_paths = [
            "./libHeliosDacAPI.so",
            "./sdk/cpp/shared_library/libHeliosDacAPI.so",
        ]
    else:
        possible_paths = []
    
    for path in possible_paths:
        if os.path.exists(path):
            lib_path = path
            break
    
    if lib_path is None:
        print(f"エラー: Helios DAC ライブラリが見つかりません（OS: {system}）")
        print("\n必要な手順:")
        if system == "Darwin":
            print("  macOS: sdk/cpp/shared_library/libHeliosLaserDAC.dylib")
        elif system == "Windows":
            print("  Windows: sdk/cpp/shared_library/HeliosLaserDAC.dll")
            print("           sdk/cpp/libusb_bin/Windows/x64/Release/dll/libusb-1.0.dll")
        elif system == "Linux":
            print("  Linux: sdk/cpp/shared_library/libHeliosDacAPI.so")
        print("\n詳細は WINDOWS_SETUP.md を参照してください。")
        return False
    
    print(f"ライブラリをロード中: {lib_path}")
    
    try:
        helios_lib = ctypes.cdll.LoadLibrary(lib_path)
        print("✓ ライブラリのロードに成功")
    except OSError as e:
        print(f"✗ ライブラリのロードに失敗: {e}")
        return False
    
    # デバイスを開く
    print("\nHelios DAC を検索中...")
    num_devices = helios_lib.OpenDevices()
    print(f"✓ 検出されたデバイス数: {num_devices}")
    
    if num_devices <= 0:
        print("\n警告: Helios DAC が検出されませんでした")
        print("以下を確認してください:")
        print("  1. Helios DAC が USB で接続されているか")
        print("  2. デバイスへのアクセス権限があるか")
        print("  3. 他のアプリケーションが DAC を使用していないか")
        helios_lib.CloseDevices()
        return False
    
    # デバイス情報を取得
    print("\nデバイス情報:")
    for i in range(num_devices):
        print(f"  デバイス {i}:")
        
        # 名前を取得
        name_buffer = ctypes.create_string_buffer(32)
        result = helios_lib.GetName(i, name_buffer)
        if result == 1:
            print(f"    名前: {name_buffer.value.decode('ascii', errors='ignore')}")
        
        # ファームウェアバージョン
        fw_version = helios_lib.GetFirmwareVersion(i)
        print(f"    ファームウェア: {fw_version}")
    
    # クリーンアップ
    helios_lib.CloseDevices()
    print("\n✓ テスト完了")
    return True

if __name__ == "__main__":
    success = test_helios_connection()
    sys.exit(0 if success else 1)

