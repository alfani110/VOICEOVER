#!/usr/bin/env python3
"""
Generate full voiceover for Episode 1: Blockbuster Memory

This script:
1. Loads the markdown script
2. Cleans markdown formatting
3. Splits into chunks (OpenAI has character limits)
4. Generates audio for each chunk using OpenAI TTS
5. Combines all chunks into a single MP3 file

Expected duration: 15-20 minutes
Expected cost: ~$1.50
"""

import os
import re
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
import time

# ============================================================================
# CONFIGURATION - CUSTOMIZE THESE SETTINGS
# ============================================================================

# OpenAI API Key - REQUIRED
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

# Input file
SCRIPT_FILE = "episode_1_blockbuster_ENHANCED.md"

# Voice selection
# Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
# Recommended for sleep stories: "onyx" (deep male) or "nova" (calm female)
VOICE = "onyx"

# Speed (0.25 to 4.0, default is 1.0)
# 0.85-0.90 recommended for sleep stories (slower, more hypnotic)
SPEED = 0.87

# Output settings
OUTPUT_DIR = Path("audio_output")
TEMP_DIR = OUTPUT_DIR / "chunks"
FINAL_OUTPUT = OUTPUT_DIR / "Episode_1_Blockbuster_Final.mp3"

# Chunk size (characters per API call)
# OpenAI has a 4096 character limit, so we use 4000 to be safe
CHUNK_SIZE = 4000

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_markdown(text):
    """Remove markdown formatting and clean up text for TTS."""

    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Remove markdown bold/italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)

    # Remove markdown links
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)

    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)

    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Remove section markers and metadata
    text = re.sub(r'---+', '', text)
    text = re.sub(r'\*Runtime:\*.*', '', text)
    text = re.sub(r'\*Word Count:\*.*', '', text)
    text = re.sub(r'\*\*Runtime:\*\*.*', '', text)
    text = re.sub(r'\*\*Word Count:\*\*.*', '', text)

    # Remove production notes section
    text = re.sub(r'\*\*PRODUCTION NOTES:?\*\*.*', '', text, flags=re.DOTALL)

    # Remove square bracket annotations
    text = re.sub(r'\[.*?\]', '', text)

    # Clean up whitespace
    text = re.sub(r'\n\n\n+', '\n\n', text)
    text = re.sub(r'  +', ' ', text)

    return text.strip()

def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks that respect sentence boundaries."""

    # Split by paragraphs first
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        # If adding this paragraph would exceed chunk size
        if len(current_chunk) + len(para) + 2 > chunk_size:
            # Save current chunk if it exists
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If paragraph itself is too long, split by sentences
            if len(para) > chunk_size:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                    else:
                        current_chunk += " " + sentence if current_chunk else sentence
            else:
                current_chunk = para
        else:
            # Add paragraph to current chunk
            current_chunk += "\n\n" + para if current_chunk else para

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def generate_audio_chunk(client, text, chunk_num, total_chunks):
    """Generate audio for a single text chunk."""

    print(f"   🎙️  Chunk {chunk_num}/{total_chunks} ({len(text)} chars)...", end=" ")

    try:
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=VOICE,
            input=text,
            speed=SPEED
        )

        # Save to temporary file
        temp_file = TEMP_DIR / f"chunk_{chunk_num:03d}.mp3"
        response.stream_to_file(str(temp_file))

        print("✅")
        return temp_file

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def combine_audio_files(audio_files):
    """Combine multiple audio files into one."""

    print("\n🔗 Combining audio chunks...")

    combined = AudioSegment.empty()

    for i, audio_file in enumerate(audio_files, 1):
        print(f"   Adding chunk {i}/{len(audio_files)}...", end=" ")
        try:
            audio = AudioSegment.from_mp3(str(audio_file))
            combined += audio
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")

    return combined

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    """Main execution function."""

    print("=" * 60)
    print("🎬 THE 90s MEMORY ARCHIVE - Episode 1 Voiceover Generator")
    print("=" * 60)
    print()

    # Validate API key
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY.startswith("sk-"):
        print("❌ ERROR: Please set your OpenAI API key in the API_KEY variable")
        print("   Get your key from: https://platform.openai.com/api-keys")
        return

    # Check if script file exists
    if not Path(SCRIPT_FILE).exists():
        print(f"❌ ERROR: Script file not found: {SCRIPT_FILE}")
        return

    # Create output directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    TEMP_DIR.mkdir(exist_ok=True)

    # Display settings
    print(f"📝 Script: {SCRIPT_FILE}")
    print(f"🎤 Voice: {VOICE}")
    print(f"⚡ Speed: {SPEED}x")
    print(f"📁 Output: {FINAL_OUTPUT}")
    print()

    # Load and clean script
    print("📖 Loading script...", end=" ")
    with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    print("✅")

    print("🧹 Cleaning markdown...", end=" ")
    clean_text = clean_markdown(raw_text)
    print(f"✅ ({len(clean_text):,} characters)")

    # Split into chunks
    print("✂️  Splitting into chunks...", end=" ")
    chunks = split_into_chunks(clean_text)
    print(f"✅ ({len(chunks)} chunks)")

    # Estimate cost
    total_chars = sum(len(chunk) for chunk in chunks)
    estimated_cost = (total_chars / 1_000_000) * 15  # $15 per 1M characters
    print(f"💰 Estimated cost: ${estimated_cost:.2f}")
    print()

    # Confirm before proceeding
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return

    print()
    print("🎙️  Generating audio chunks...")
    print()

    # Initialize OpenAI client
    client = OpenAI(api_key=API_KEY)

    # Generate audio for each chunk
    audio_files = []
    start_time = time.time()

    for i, chunk in enumerate(chunks, 1):
        audio_file = generate_audio_chunk(client, chunk, i, len(chunks))
        if audio_file:
            audio_files.append(audio_file)
        else:
            print(f"⚠️  Warning: Chunk {i} failed, continuing...")

    # Combine all chunks
    if audio_files:
        combined_audio = combine_audio_files(audio_files)

        print(f"\n💾 Saving final output to {FINAL_OUTPUT}...", end=" ")
        combined_audio.export(str(FINAL_OUTPUT), format="mp3", bitrate="128k")
        print("✅")

        # Calculate stats
        duration_seconds = len(combined_audio) / 1000
        duration_minutes = duration_seconds / 60
        file_size_mb = FINAL_OUTPUT.stat().st_size / (1024 * 1024)
        elapsed_time = time.time() - start_time

        print()
        print("=" * 60)
        print("✅ VOICEOVER GENERATION COMPLETE!")
        print("=" * 60)
        print(f"📁 File: {FINAL_OUTPUT}")
        print(f"⏱️  Duration: {duration_minutes:.1f} minutes")
        print(f"💾 Size: {file_size_mb:.1f} MB")
        print(f"⏲️  Processing time: {elapsed_time/60:.1f} minutes")
        print(f"💰 Estimated cost: ${estimated_cost:.2f}")
        print()
        print("🎉 Your voiceover is ready to use!")
        print("=" * 60)

    else:
        print("\n❌ ERROR: No audio files were generated successfully")

if __name__ == "__main__":
    main()
