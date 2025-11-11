# The 90s Memory Archive - Episode 1 Voiceover Generator

## Project Overview

Generate a ~100-minute AI voiceover for a sleep story podcast about renting movies from Blockbuster in 1996.

## Setup Complete ✅

- ✅ Python 3.11.14 installed
- ✅ OpenAI package installed
- ✅ pydub package installed
- ✅ ffmpeg installed

## Files

- `episode_1_blockbuster_ENHANCED.md` - The complete script (~95,000 characters)
- `test_voices.py` - Generate voice samples to choose your preferred voice
- `generate_voiceover.py` - Main script to generate the full voiceover

## Quick Start

### 1. Test Voices (Recommended - ~$0.05)

```bash
python3 test_voices.py
```

This will generate 6 short samples in `voice_tests/` directory so you can choose your favorite voice.

### 2. Generate Full Voiceover (~$1.50, 15-20 minutes)

```bash
python3 generate_voiceover.py
```

Output will be saved to: `audio_output/Episode_1_Blockbuster_Final.mp3`

## Configuration

Edit the Python scripts to set:
- `API_KEY` - Your OpenAI API key (required)
- `VOICE` - Choose from: alloy, echo, fable, onyx, nova, shimmer
- `SPEED` - Recommended 0.85-0.90 for sleep stories

## Expected Output

- **Duration:** ~90-100 minutes
- **File Size:** ~80-100 MB
- **Format:** MP3, 128 kbps
- **Cost:** ~$1.50

## Next Steps

1. Provide your OpenAI API key
2. Run voice tests (optional but recommended)
3. Choose your preferred voice
4. Run the full generation
