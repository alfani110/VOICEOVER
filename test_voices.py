#!/usr/bin/env python3
"""
Test script to generate short audio samples with different OpenAI TTS voices.
This helps you choose the best voice for your project before running the full generation.

Cost: ~$0.05 total for all 6 voice samples
"""

import os
from pathlib import Path
from openai import OpenAI

# ============================================================================
# CONFIGURATION - SET YOUR API KEY HERE
# ============================================================================
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual OpenAI API key

# ============================================================================
# TEST SETTINGS
# ============================================================================
# Test text - a representative sample from the script
TEST_TEXT = """
Welcome to The 90s Memory Archive. I'm glad you're here.

Tonight, we're going back to a Friday evening in the summer of 1996. We're going to rent a movie from Blockbuster. We're going to drive there, walk through those automatic doors, smell that distinctive smell, browse the aisles, choose our movies, and come home to watch them.

Get comfortable, close your eyes, and let's remember together.
"""

# All available OpenAI voices
VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Speed setting (0.85-0.90 recommended for sleep stories)
SPEED = 0.87

# Output directory
OUTPUT_DIR = Path("voice_tests")

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def test_voices():
    """Generate sample audio with each available voice."""

    # Validate API key
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY.startswith("sk-"):
        print("❌ ERROR: Please set your OpenAI API key in the API_KEY variable")
        print("   Get your key from: https://platform.openai.com/api-keys")
        return

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR.absolute()}\n")

    # Initialize OpenAI client
    client = OpenAI(api_key=API_KEY)

    # Generate sample for each voice
    print("🎤 Generating voice samples...\n")

    for voice in VOICES:
        print(f"   Generating '{voice}' voice...", end=" ")

        try:
            # Generate speech
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice=voice,
                input=TEST_TEXT,
                speed=SPEED
            )

            # Save to file
            output_file = OUTPUT_DIR / f"test_{voice}.mp3"
            response.stream_to_file(str(output_file))

            print(f"✅ Saved to {output_file.name}")

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n✅ Done! Listen to the samples in the '{OUTPUT_DIR}' directory")
    print("\n📝 Voice Recommendations:")
    print("   • onyx - Deep, calm male voice (meditation guide style)")
    print("   • nova - Warm, soothing female voice (audiobook narrator style)")
    print("   • alloy - Neutral, balanced")
    print("   • echo - Clear male")
    print("   • fable - British accent")
    print("   • shimmer - Soft female")

    print(f"\n💰 Estimated cost: ~$0.05")

if __name__ == "__main__":
    test_voices()
