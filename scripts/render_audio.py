"""Render narration with Kokoro (local) from build/tts-jobs.json.

Each clip: Kokoro 24 kHz -> loudness-normalised (EBU R128, -13 LUFS, limited) with short
fades -> mono AAC 64 kbps .m4a. Existing files are skipped (filenames carry a content hash).
Writes build/durations.json. Usage: .venv/bin/python scripts/render_audio.py [--voice af_heart]
"""
import json, os, re, subprocess, sys, tempfile, time
import numpy as np, soundfile as sf

jobs_path = sys.argv[sys.argv.index("--jobs") + 1] if "--jobs" in sys.argv else "build/tts-jobs.json"
jobs = json.load(open(jobs_path))
voice = jobs["voice"]
if "--voice" in sys.argv:
    voice = sys.argv[sys.argv.index("--voice") + 1]

SPEED = float(os.environ.get("SPEED", "1.05"))   # a touch brisker reads as more enthusiastic
durs_path = "build/durations.json"
durs = json.load(open(durs_path)) if os.path.exists(durs_path) else {}

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else None

todo = [j for j in jobs["jobs"] if not os.path.exists(j["out"])]
print(f"{len(jobs['jobs'])} clips, {len(todo)} to render with {voice}", flush=True)

if todo:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from kokoro import KPipeline, KModel
    model = KModel(repo_id="hexgrad/Kokoro-82M", config="models/kokoro/config.json",
                   model="models/kokoro/kokoro-v1_0.pth").eval()
    pipe = KPipeline(lang_code=voice[0], repo_id="hexgrad/Kokoro-82M", model=model)
    vpath = f"models/kokoro/voices/{voice}.pt"
    t0 = time.time()
    for n, j in enumerate(todo, 1):
        # [[pause N]] markers become N seconds of silence (quiz "have a guess" moments)
        gap = np.zeros(int(24000 * 0.12), dtype=np.float32)
        pieces = []
        for k, part in enumerate(re.split(r"\[\[pause (\d+)\]\]", j["tts"])):
            if k % 2:
                pieces.append(np.zeros(int(24000 * float(part)), dtype=np.float32)); continue
            if not part.strip(): continue
            for _, _, a in pipe(part.strip(), voice=vpath, speed=SPEED):
                pieces += [a.numpy() if hasattr(a, "numpy") else a, gap]
        audio = np.concatenate(pieces) if pieces else np.zeros(2400, dtype=np.float32)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio, 24000)
        dur = len(audio) / 24000 + 0.4
        os.makedirs(os.path.dirname(j["out"]), exist_ok=True)
        # -13 LUFS: louder than podcast norm so the voice cuts through road noise and ducked music
        af = (f"adelay=150,apad=pad_dur=0.25,loudnorm=I=-18:TP=-2:LRA=11,"   # even level first, then dense and loud (~-9 LUFS)
              f"acompressor=threshold=-24dB:ratio=6:attack=3:release=120:makeup=14,alimiter=limit=0.94:level=false,"
              f"afade=t=in:d=0.12,afade=t=out:st={max(0, dur - 0.35):.2f}:d=0.35")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp.name, "-af", af, "-ar", "44100", "-ac", "1",
                        "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", j["out"]], check=True)
        os.unlink(tmp.name)
        durs[j["out"]] = probe(j["out"])
        if n % 5 == 0 or n == len(todo):
            json.dump(durs, open(durs_path, "w"))
            el = time.time() - t0
            print(f"  {n}/{len(todo)}  {el:.0f}s elapsed", flush=True)

for j in jobs["jobs"]:
    if j["out"] not in durs and os.path.exists(j["out"]):
        durs[j["out"]] = probe(j["out"])
json.dump(durs, open(durs_path, "w"))
print("done", flush=True)
