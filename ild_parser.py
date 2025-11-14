#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ILD (ILDA) ファイルパーサー
ILDA Image Data Transfer Format に基づいて ILD ファイルを読み込みます
"""

import struct
import numpy as np
from typing import List, Tuple, Dict

class ILDFrame:
    """ILD フレームデータを保持するクラス"""
    def __init__(self):
        self.name = ""
        self.company = ""
        self.points = []  # (x, y, r, g, b, blanking) のリスト
        
class ILDParser:
    """ILD ファイルパーサー"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.frames = []
        
    def parse(self) -> List[ILDFrame]:
        """ILD ファイルをパースしてフレームリストを返す"""
        with open(self.filename, 'rb') as f:
            while True:
                # ヘッダーを読み込む（32バイト）
                header_data = f.read(32)
                if len(header_data) < 32:
                    break
                    
                # ヘッダーをパース
                header = self._parse_header(header_data)
                if header is None:
                    break
                
                # フォーマットタイプをチェック
                format_code = header['format_code']
                
                # サポートされているフォーマット
                if format_code in [0, 1, 2]:  # 3D座標、2D座標、カラーパレット
                    frame = ILDFrame()
                    frame.name = header['name']
                    frame.company = header['company']
                    
                    # ポイントデータを読み込む
                    num_points = header['num_records']
                    
                    if format_code == 0:  # 3D座標 + インデックスカラー
                        frame.points = self._parse_3d_indexed_color(f, num_points)
                    elif format_code == 1:  # 2D座標 + インデックスカラー
                        frame.points = self._parse_2d_indexed_color(f, num_points)
                    elif format_code == 2:  # カラーパレット
                        # パレットは今回は使用しない
                        f.read(num_points * 3)
                        continue
                    
                    if frame.points:
                        self.frames.append(frame)
                elif format_code == 4:  # 3D座標 + True Color
                    frame = ILDFrame()
                    frame.name = header['name']
                    frame.company = header['company']
                    frame.points = self._parse_3d_true_color(f, header['num_records'])
                    if frame.points:
                        self.frames.append(frame)
                elif format_code == 5:  # 2D座標 + True Color
                    frame = ILDFrame()
                    frame.name = header['name']
                    frame.company = header['company']
                    frame.points = self._parse_2d_true_color(f, header['num_records'])
                    if frame.points:
                        self.frames.append(frame)
                else:
                    # 未対応のフォーマット
                    break
                
        return self.frames
    
    def _parse_header(self, data: bytes) -> Dict:
        """ILD ヘッダーをパース"""
        if len(data) < 32:
            return None
            
        # ヘッダー構造
        # "ILDA" (4 bytes)
        # 予約 (3 bytes)
        # フォーマットコード (1 byte)
        # フレーム名 (8 bytes)
        # 会社名 (8 bytes)
        # レコード数 (2 bytes, big-endian)
        # フレーム番号 (2 bytes, big-endian)
        # 総フレーム数 (2 bytes, big-endian)
        # スキャナーヘッド (1 byte)
        # 予約 (1 byte)
        
        magic = data[0:4]
        if magic != b'ILDA':
            return None
        
        format_code = data[7]
        name = data[8:16].decode('ascii', errors='ignore').strip('\x00')
        company = data[16:24].decode('ascii', errors='ignore').strip('\x00')
        num_records = struct.unpack('>H', data[24:26])[0]
        frame_num = struct.unpack('>H', data[26:28])[0]
        total_frames = struct.unpack('>H', data[28:30])[0]
        
        return {
            'format_code': format_code,
            'name': name,
            'company': company,
            'num_records': num_records,
            'frame_num': frame_num,
            'total_frames': total_frames
        }
    
    def _parse_3d_indexed_color(self, f, num_points: int) -> List[Tuple]:
        """3D座標 + インデックスカラーのポイントデータをパース"""
        points = []
        for _ in range(num_points):
            data = f.read(8)  # 各ポイントは8バイト
            if len(data) < 8:
                break
            
            # X, Y, Z (各2バイト, signed, big-endian)
            # Status code (1バイト)
            # Color index (1バイト)
            x = struct.unpack('>h', data[0:2])[0]
            y = struct.unpack('>h', data[2:4])[0]
            z = struct.unpack('>h', data[4:6])[0]
            status = data[6]
            color_idx = data[7]
            
            # ブランキングビット（最上位ビット）
            blanking = (status & 0x40) != 0
            
            # インデックスカラーを RGB に変換（簡易的な変換）
            r, g, b = self._index_to_rgb(color_idx)
            
            # -32768 ~ 32767 を 0 ~ 65535 に変換
            x_norm = (x + 32768)
            y_norm = (y + 32768)
            
            points.append((x_norm, y_norm, r, g, b, blanking))
        
        return points
    
    def _parse_2d_indexed_color(self, f, num_points: int) -> List[Tuple]:
        """2D座標 + インデックスカラーのポイントデータをパース"""
        points = []
        for _ in range(num_points):
            data = f.read(6)  # 各ポイントは6バイト
            if len(data) < 6:
                break
            
            x = struct.unpack('>h', data[0:2])[0]
            y = struct.unpack('>h', data[2:4])[0]
            status = data[4]
            color_idx = data[5]
            
            blanking = (status & 0x40) != 0
            r, g, b = self._index_to_rgb(color_idx)
            
            x_norm = (x + 32768)
            y_norm = (y + 32768)
            
            points.append((x_norm, y_norm, r, g, b, blanking))
        
        return points
    
    def _parse_3d_true_color(self, f, num_points: int) -> List[Tuple]:
        """3D座標 + True Color のポイントデータをパース"""
        points = []
        for _ in range(num_points):
            data = f.read(10)  # 各ポイントは10バイト
            if len(data) < 10:
                break
            
            x = struct.unpack('>h', data[0:2])[0]
            y = struct.unpack('>h', data[2:4])[0]
            z = struct.unpack('>h', data[4:6])[0]
            status = data[6]
            b = data[7]  # Blue
            g = data[8]  # Green
            r = data[9]  # Red
            
            blanking = (status & 0x40) != 0
            
            x_norm = (x + 32768)
            y_norm = (y + 32768)
            
            points.append((x_norm, y_norm, r, g, b, blanking))
        
        return points
    
    def _parse_2d_true_color(self, f, num_points: int) -> List[Tuple]:
        """2D座標 + True Color のポイントデータをパース"""
        points = []
        for _ in range(num_points):
            data = f.read(8)  # 各ポイントは8バイト
            if len(data) < 8:
                break
            
            x = struct.unpack('>h', data[0:2])[0]
            y = struct.unpack('>h', data[2:4])[0]
            status = data[4]
            b = data[5]  # Blue
            g = data[6]  # Green
            r = data[7]  # Red
            
            blanking = (status & 0x40) != 0
            
            x_norm = (x + 32768)
            y_norm = (y + 32768)
            
            points.append((x_norm, y_norm, r, g, b, blanking))
        
        return points
    
    def _index_to_rgb(self, index: int) -> Tuple[int, int, int]:
        """カラーインデックスを RGB に変換（簡易的な実装）"""
        # ILDA 標準カラーパレットの簡易版
        # 実際のアプリケーションでは、カラーパレットを読み込むべき
        if index == 0:
            return (0, 0, 0)  # Black
        elif index < 8:
            # 基本色
            colors = [
                (255, 0, 0),    # Red
                (255, 255, 0),  # Yellow
                (0, 255, 0),    # Green
                (0, 255, 255),  # Cyan
                (0, 0, 255),    # Blue
                (255, 0, 255),  # Magenta
                (255, 255, 255) # White
            ]
            return colors[index - 1]
        else:
            # 他の色は白にする（簡易版）
            return (255, 255, 255)


if __name__ == "__main__":
    # テスト用
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ild_parser.py <ild_file>")
        sys.exit(1)
    
    parser = ILDParser(sys.argv[1])
    frames = parser.parse()
    
    print(f"読み込んだフレーム数: {len(frames)}")
    for i, frame in enumerate(frames[:5]):  # 最初の5フレームを表示
        print(f"フレーム {i}: {len(frame.points)} ポイント, 名前: {frame.name}")

