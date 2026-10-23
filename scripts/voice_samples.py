"""Render the same ~20 s sample in several Kokoro voices into voice-samples/ (m4a + wav)."""
import subprocess, sys, time
import numpy as np, soundfile as sf
from kokoro import KPipeline, KModel
import torch
MODEL = KModel(repo_id="hexgrad/Kokoro-82M", config="models/kokoro/config.json", model="models/kokoro/kokoro-v1_0.pth").eval()

TEXT = ("Welcome to the road. Off to your left, that long, flat, shimmering stretch is the Yolo Bypass, "
        "a flood channel built to take the Sacramento River's overflow so the city doesn't have to. "
        "In a wet winter, this whole plain becomes a shallow inland sea, and the causeway you're on "
        "turns into a bridge over it. Keep an eye out for egrets.")
VOICES = sys.argv[1:] or ["af_heart", "am_michael", "bf_emma", "bm_george", "bm_fable", "am_fenrir"]
pipes = {}
for v in VOICES:
    lang = v[0]  # 'a' American, 'b' British
    if lang not in pipes:
        pipes[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M", model=MODEL)
    t = time.time()
    audio = np.concatenate([a for _, _, a in pipes[lang](TEXT, voice=f"models/kokoro/voices/{v}.pt", speed=1.0)])
    wav = f"voice-samples/{v}.wav"
    sf.write(wav, audio, 24000)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ac", "1", "-c:a", "aac", "-b:a", "64k", f"voice-samples/{v}.m4a"], check=True)
    print(v, f"{len(audio)/24000:.1f}s audio in {time.time()-t:.1f}s", flush=True)
