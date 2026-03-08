#!/usr/bin/env python3
"""
测试 Doubao TTS 功能
"""
import time
from config import APP_CONFIG
from core.services.tts.doubao import DoubaoTTS


def test_tts():
    tts_config = APP_CONFIG.get("tts", {}).get("doubao", {})
    app_id = tts_config.get("app_id")
    access_key = tts_config.get("access_key")
    speaker = tts_config.get("default_speaker", "zh_female_cancan_mars_bigtts")

    if not app_id or not access_key:
        print("错误: 请先配置豆包 API 凭证")
        return

    print(f"\n{'='*60}")
    print(f"测试 Doubao TTS")
    print(f"{'='*60}")
    print(f"音色: {speaker}")
    print(f"配置格式: {tts_config.get('audio_format', '默认(mp3)')}")

    # 测试 ogg_opus 格式 (从配置读取)
    print(f"\n--- 测试 1: 使用配置默认格式 ---")
    tts = DoubaoTTS(
        app_id=app_id,
        access_key=access_key,
        speaker=speaker,
    )
    print(f"实际使用格式: {tts.audio_format}")

    text = "央视财经频道《经济半小时》两会特别节目《中国经济向新行：智能经济活力奔涌》播出，聚焦我国人工智能大模型已进入全球第一梯队，而阿里千问APP作为AI助手的典型代表，正以“AI办事”的创新模式，深刻重塑大众的日常生活。"
    print(f"合成文本: {text}")

    start = time.time()
    audio_data = tts.synthesize(text)
    elapsed = time.time() - start

    if audio_data:
        print(f"✅ 成功! 音频大小: {len(audio_data)} bytes, 耗时: {elapsed:.2f}s")
    else:
        print(f"❌ 失败!")

    # 测试 mp3 格式
    print(f"\n--- 测试 2: 显式使用 mp3 格式 ---")
    start = time.time()
    audio_data_mp3 = tts.synthesize(text, format="mp3")
    elapsed = time.time() - start

    if audio_data_mp3:
        print(f"✅ 成功! 音频大小: {len(audio_data_mp3)} bytes, 耗时: {elapsed:.2f}s")
    else:
        print(f"❌ 失败!")

    # 对比
    print(f"\n--- 对比 ---")
    if audio_data and audio_data_mp3:
        ratio = len(audio_data_mp3) / len(audio_data)
        print(f"ogg_opus vs mp3 大小比例: {ratio:.2f}x")
        if ratio > 1:
            print(f"ogg_opus 节省: {(1 - 1/ratio) * 100:.1f}%")

    print(f"\n{'='*60}")
    print("测试完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    test_tts()
