#!/usr/bin/env python3
"""Mix voice mp3 with procedural ambience bed + random foley details -> opus ogg.
Usage: voice_mix.py in.mp3 out.ogg {street|home|soft}
"""
import os
import random
import subprocess
import sys
import tempfile

FF = "ffmpeg"
PROBE = "ffprobe"


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def probe_dur(path):
    out = subprocess.run(
        [PROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    )
    return max(1.0, float(out.stdout.strip()))


def render_detail(kind, path, seed):
    r = random.Random(seed)
    if kind == "rustle":
        d = round(r.uniform(0.35, 0.9), 2)
        run([FF, "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"anoisesrc=color=white:duration={d}:seed={r.randint(1,9999)}",
             "-af", f"highpass=f={r.randint(2200,3600)},volume=0.28,afade=t=in:st=0:d=0.08,afade=t=out:st={max(0.05, d-0.12)}:d=0.1",
             path])
    elif kind == "door":
        f = r.randint(75, 130)
        run([FF, "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"sine=frequency={f}:duration=0.5",
             "-af", "volume=0.55*exp(-7*t):eval=frame", path])
    elif kind == "keys":
        f1 = r.randint(4200, 6800)
        f2 = f1 + r.randint(300, 900)
        run([FF, "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", f"sine=frequency={f1}:duration=0.6",
             "-f", "lavfi", "-i", f"sine=frequency={f2}:duration=0.6",
             "-filter_complex",
             "[0:a]volume=0.22*exp(-11*t):eval=frame[k1];[1:a]volume=0.16*exp(-13*t):eval=frame[k2];[k1][k2]amix=inputs=2:duration=longest:normalize=0",
             path])
    elif kind == "steps":
        f = r.randint(60, 95)
        run([FF, "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"sine=frequency={f}:duration=0.35",
             "-af", "volume=0.5*exp(-9*t):eval=frame,lowpass=f=300", path])
    else:
        raise ValueError(kind)


def main():
    inp, outp, kind = sys.argv[1], sys.argv[2], sys.argv[3]
    dur = probe_dur(inp)
    tmpd = tempfile.mkdtemp(prefix="vmix")
    try:
        if kind == "street":
            bed_src, bed_f = "anoisesrc=color=brown:duration=180:seed=7", "lowpass=f=450,volume=0.13"
            pool = []
        elif kind == "home":
            bed_src, bed_f = "anoisesrc=color=pink:duration=180:seed=7", "lowpass=f=1200,volume=0.05"
            pool = ["rustle", "door", "keys", "steps"]
        else:
            bed_src, bed_f = "anoisesrc=color=pink:duration=180:seed=7", "lowpass=f=2000,volume=0.025"
            pool = ["rustle", "keys"]

        n = random.choice([0, 1, 1, 2])
        picks = random.sample(pool, k=min(n, len(pool)))
        inputs = ["-i", inp, "-f", "lavfi", "-i", bed_src]
        fc_parts = [f"[1:a]{bed_f},aloop=loop=-1:size=2e9[bed]"]
        labels = ["[0:a]", "[bed]"]
        for idx, det in enumerate(picks):
            dp = os.path.join(tmpd, f"d{idx}.wav")
            render_detail(det, dp, random.randint(1, 999999))
            inputs += ["-i", dp]
            tag = f"d{idx}"
            if det == "steps":
                off1 = round(random.uniform(0.3, max(0.4, dur - 1.2)), 2)
                off2 = round(min(dur - 0.5, off1 + random.uniform(0.45, 0.8)), 2)
                ms1, ms2 = int(off1 * 1000), int(off2 * 1000)
                fc_parts.append(
                    f"[{2+idx}:a]asplit[a{idx}][b{idx}];"
                    f"[a{idx}]adelay={ms1},volume=0.5[{tag}a];"
                    f"[b{idx}]adelay={ms2},volume=0.4[{tag}b]"
                )
                labels += [f"[{tag}a]", f"[{tag}b]"]
            else:
                off = round(random.uniform(0.2, max(0.3, dur - 0.6)), 2)
                ms = int(off * 1000)
                fc_parts.append(f"[{2+idx}:a]adelay={ms},volume=0.55[{tag}]")
                labels.append(f"[{tag}]")
        fc_parts.append(
            "".join(labels) + f"amix=inputs={len(labels)}:duration=first:dropout_transition=0:normalize=0"
        )
        run([FF, "-y", "-loglevel", "error"] + inputs +
            ["-filter_complex", ";".join(fc_parts),
             "-c:a", "libopus", "-b:a", "48k", outp])
        print(f"ok kind={kind} details={picks} dur={dur:.1f}")
    finally:
        for f in os.listdir(tmpd):
            try:
                os.unlink(os.path.join(tmpd, f))
            except OSError:
                pass
        try:
            os.rmdir(tmpd)
        except OSError:
            pass


if __name__ == "__main__":
    main()
