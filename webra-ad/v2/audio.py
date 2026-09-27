"""WEBRA v2 score - restrained premium electronic, 120 BPM, A minor. Writes audio.wav (48k stereo).
Accents sit on the same beats as index.html. Fewer, softer SFX; shared reverb bus; gentle master."""
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000; DUR = 30.0; BEAT = 0.5; BAR = 2.0
N = int(SR * DUR)
dry = np.zeros((2, N)); verb = np.zeros((2, N)); duck = np.ones(N)
rng = np.random.default_rng(11)

def t_(d): return np.arange(int(d * SR)) / SR
def filt(x, f, kind='low', o=2):
    return sosfilt(butter(o, f, kind, fs=SR, output='sos'), x)
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def add(sig, at, g=1.0, pan=0.0, send=0.0, ducked=True):
    i = int(round(at * SR)); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * g; lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    k = duck[i:j] if ducked else 1
    for bus, amt in ((dry, 1.0), (verb, send)):
        if amt: bus[0, i:j] += s * lg * amt * k; bus[1, i:j] += s * rg * amt * k
def note(n): return 440 * 2 ** ((n - 69) / 12)

# ---------------- instruments ----------------
def kick():
    t = t_(0.5); f = 46 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5) * np.minimum(1, t / 0.002)
def hat(d=0.04):
    n = rng.standard_normal(int(SR * 0.12)); return filt(n, 8000, 'high') * env(len(n), .001, d)
def snap():
    n = rng.standard_normal(int(SR * .3)); return filt(filt(n, 1200, 'high'), 6000) * env(len(n), .001, .05)
def sub(f, d):
    t = t_(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, t / .01) * np.minimum(1, (d - t) / .03)
def pluck(f, d=0.45):
    t = t_(d); s = sum(np.sin(2 * np.pi * f * h * t) / h ** 1.6 for h in range(1, 7))
    return filt(s, 3200) * env(len(t), .003, .16)
def pad(fs, d):
    t = t_(d); s = np.zeros(len(t))
    for f in fs:
        for det in (-.1, .1): s += np.sin(2 * np.pi * f * (1 + det / 100) * t) + .35 * np.sin(2 * np.pi * 2 * f * (1 + det / 100) * t)
    s = filt(s / (2 * len(fs)), 1600)
    return s * np.minimum(1, t / .8) * np.minimum(1, (d - t) / .8)
def air(d=0.9, up=True):   # soft transition swell, no harsh whoosh
    n = rng.standard_normal(int(SR * d)); x = np.linspace(0, 1, len(n))
    sh = (x ** 2 if up else np.sin(np.pi * x) ** 2) * (1 - x) ** .3 if up else np.sin(np.pi * x) ** 2
    return filt(filt(n, 500, 'high'), 4500) * sh * .5
def thump():               # restrained low accent for headline reveals
    t = t_(0.9); f = 38 + 30 * np.exp(-t * 14)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .004, .28)
def tick(f=2600):
    t = t_(.05); return np.sin(2 * np.pi * f * t) * env(len(t), .0005, .008)
def key():
    t = t_(.025); return filt(rng.standard_normal(len(t)), 3500) * env(len(t), .0003, .004)
def bell(f, d=3.0):
    t = t_(d); m = np.sin(2 * np.pi * f * 2 * t) * 1.3 * np.exp(-t * 2.5)
    return np.sin(2 * np.pi * f * t + m) * env(len(t), .003, 1.1)

# ---------------- arrangement ----------------
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]   # Am F C G
arp = [0, 2, 1, 2, 0, 2, 1, 2]
for b in range(15):
    t0 = b * BAR; root, ch = prog[b % 4]
    in_break = 22 <= t0 < 24
    add(pad([note(n) for n in ch], BAR + .8), t0, .10 if t0 < 4 else .12, send=.5)
    if t0 >= 2 and not in_break:
        for q in range(8):
            n = ch[arp[q]] + 12
            add(pluck(note(n)), t0 + q * BEAT / 2, .10 if t0 < 4 else .13, (-.35, .35)[q % 2], send=.35)
    if t0 >= 4 and not in_break:
        for q in range(4):
            add(sub(note(root - 24), BEAT * .9), t0 + q * BEAT + BEAT * .5 * (q % 2 == 1) * 0, .34)
# drums: build from 4 s, breakdown 22-24, half-time outro
for i in range(60):
    t = i * BEAT
    if 4 <= t < 22 or 24 <= t < 28:
        add(kick(), t, .62, ducked=False)
        d = int(.16 * SR); a = int(t * SR); duck[a:a + d] = np.minimum(duck[a:a + d], .45 + .55 * np.linspace(0, 1, d))
        add(hat(), t + BEAT / 2, .10, .25)
        if i % 2: add(snap(), t, .16, send=.4)
        if 12 <= t < 22: add(hat(.015), t + BEAT / 4, .04, -.3); add(hat(.015), t + 3 * BEAT / 4, .04, -.3)
    elif 28 <= t < 30 and i % 2 == 0:
        add(kick(), t, .35, ducked=False)

# ---------------- sound design (on the beat) ----------------
add(air(1.2), -0.2 + .2, .12, send=.4)                         # open
for at in (0.45, 5.0, 12.0, 18.0): add(thump(), at, .42)       # headline reveals
add(air(1.0), 2.9, .10, send=.5)
add(air(1.0), 3.0 + .7, .16, send=.6)                          # phone -> website (3.7)
for k, at in enumerate([4.75, 5.4, 5.75, 6.0, 6.125, 6.25]): add(tick(2200 + 180 * k), at, .07, (k % 2 - .5) * .6, send=.3)
add(air(.9), 6.9, .12, send=.5)                                # desktop -> mobile
add(air(.9), 8.95, .14, send=.5)                               # website -> search bar
for c in range(26): add(key(), 10.3 + c * .046, .22, .15)      # typing
add(tick(1400), 11.5, .12, send=.3)                            # enter
add(bell(note(76), 2.0), 12.1, .07, .2, send=.6)               # business found
add(air(1.1), 14.8, .16, send=.6)                              # camera pan down
for k in range(6): add(bell(note([69, 72, 76, 79, 81, 84][k]), .8), 18.3 + k * .25, .045, (k % 2 - .5) * .8, send=.5)  # tasks resolve
add(air(.9), 20.6, .14, send=.5)                               # chips -> stripes
x = np.linspace(0, 1, int(SR * 2.0)); riser = filt(rng.standard_normal(len(x)), 1500 + 0, 'high') * x ** 2.2 * .12
add(filt(riser, 7000), 21.9, 1.0, send=.6)                     # into the reveal
# sonic logo on 24.0: soft sub hit + open A-minor chord + three-note motif
add(thump(), 24.0, .6); add(pad([note(n) for n in (45, 57, 64, 69, 72)], 5.5), 24.0, .16, send=.7)
for k, (n, at) in enumerate([(76, 24.0), (83, 24.25), (81, 24.5)]):
    add(bell(note(n)), at, .14, (-.3, .3, 0)[k], send=.8)
for at in (24.6, 25.0, 25.5): add(tick(2000), at, .04, send=.4)

# ---------------- reverb bus + master ----------------
ir_t = t_(2.2); ir = rng.standard_normal((2, len(ir_t))) * np.exp(-ir_t * 3.0)
ir = np.stack([filt(ir[c], 5000) for c in range(2)]); ir[:, :int(.02 * SR)] = 0
wet = np.stack([fftconvolve(verb[c], ir[c])[:N] for c in range(2)]) * .06
mix = dry + wet
mix = np.stack([filt(mix[c], 25, 'high') for c in range(2)])
g = 10 ** (-14.2 / 20) / np.sqrt(np.mean(mix ** 2))            # approx -14 LUFS integrated
mix = np.tanh(mix * g * 1.2) / 1.2
fade = np.ones(N); k = int(1.5 * SR); fade[-k:] = np.linspace(1, 0, k) ** 1.5; mix *= fade
mix *= min(1, .89 / np.max(np.abs(mix)))
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print('audio.wav written')
