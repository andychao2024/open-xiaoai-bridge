#!/usr/bin/env python3
"""
获取豆包 TTS 可用音色列表
"""

import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_client import api_request


def list_voices(version=None):
    """
    获取豆包 TTS 可用音色列表
    
    Args:
        version: 版本筛选 "1.0", "2.0", "all"
    """
    path = "/api/tts/doubao_voices"
    if version:
        path += f"?version={version}"
    
    return api_request(path)


def main():
    parser = argparse.ArgumentParser(description="获取豆包 TTS 音色列表")
    parser.add_argument("--version", choices=["1.0", "2.0", "all"],
                        help="版本筛选: 1.0, 2.0, all")
    
    args = parser.parse_args()
    
    try:
        result = list_voices(version=args.version)
        
        if not result.get("success"):
            print(f"❌ 获取失败: {result}")
            sys.exit(1)
        
        data = result.get("data", {})
        
        # 显示 2.0 音色
        if "2.0" in data:
            print("\n🎙️  2.0 音色 (seed-tts-2.0) - 高质量推荐")
            print("-" * 70)
            for voice in data["2.0"]:
                name = voice.get("name", "")
                voice_type = voice.get("voice_type", "")
                desc = voice.get("description", "")
                print(f"  {name:12} | {voice_type:45} | {desc}")
        
        # 显示 1.0 音色
        if "1.0" in data:
            print("\n🎙️  1.0 音色 (seed-tts-1.0)")
            print("-" * 70)
            for voice in data["1.0"]:
                name = voice.get("name", "")
                voice_type = voice.get("voice_type", "")
                desc = voice.get("description", "")
                emotion = "✨多情感" if "emo" in voice_type else ""
                print(f"  {name:12} | {voice_type:45} | {desc} {emotion}")
        
        print("\n💡 使用示例:")
        print(f'  python3 tts_doubao.py "你好" --speaker zh_female_vv_uranus_bigtts')
        print(f'  python3 tts_doubao.py "你好" --speaker zh_male_lengkugege_emo_v2_mars_bigtts --emotion happy')
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import os
    main()
