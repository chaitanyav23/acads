# ─── Standard library ─────────────────────────────────────────────────────────
import os
import glob
import argparse
import warnings
warnings.filterwarnings("ignore")
 
# ─── Third-party ──────────────────────────────────────────────────────────────
import numpy as np
import cv2
from scipy.signal import butter, sosfiltfilt, welch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
 
# Optional GPU support via PyTorch
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
 
# =============================================================================
# ▌ 1. CONFIGURATION  (edit these or pass as CLI args)
# =============================================================================
 
DEFAULT_CFG = dict(
    # ── I/O ────────────────────────────────────────────────────────────────
    input_dir   = "./attention_only",    # folder of attention-masked .avi/.mp4
    output_dir  = "./evm_outputs",         # where to save amplified videos + signals
    ext         = "*.mp4",                 # glob pattern for video files
 
    # ── Video ──────────────────────────────────────────────────────────────
    fps         = 30.0,                    # camera frame rate (UBFC-RPPG = 30 fps)
 
    # ── Preprocessing ──────────────────────────────────────────────────────
    pre_smooth  = True,                    # Gaussian blur before pyramid (reduces mask artifacts)
    smooth_ksize= 3,                       # kernel size for pre-smoothing (must be odd)
 
    # ── Spatial decomposition ──────────────────────────────────────────────
    pyramid_type    = "laplacian",         # "laplacian" (motion) or "gaussian" (color / rPPG)
    n_levels        = 4,                   # number of pyramid levels
    color_space     = "YIQ",              # "YIQ" (recommended) or "BGR"
 
    # ── Temporal filtering ─────────────────────────────────────────────────
    filter_method   = "fft",              # "iir" (real-time friendly) or "fft" (offline, sharper)
    # Heart rate band  : 0.8 – 2.0 Hz  ≡  48 – 120 bpm
    freq_low_hr     = 0.8,
    freq_high_hr    = 2.0,
    # Respiration band : 0.1 – 0.5 Hz  ≡  6 – 30 breaths/min
    freq_low_rr     = 0.1,
    freq_high_rr    = 0.5,
    # Choose which band to amplify for the *video output*
    target          = "hr",               # "hr" or "rr"
    iir_order       = 2,                  # Butterworth filter order (2 is stable & smooth)
 
    # ── Amplification ──────────────────────────────────────────────────────
    alpha           = 20,                 # magnification factor (10–50 typical for color)
    # Spatial wavelength cutoff: attenuate alpha for high spatial frequencies
    # (Eq. 14 in Wu et al.): set to None to disable attenuation
    lambda_cutoff   = None,               # e.g. 16 pixels — set None for color-only EVM
 
    # ── Output options ──────────────────────────────────────────────────────
    save_video      = True,               # write amplified video
    save_signal     = True,               # save 1-D mean-intensity signal as .npy + plot
    fourcc          = "mp4v",             # codec for output video
    use_gpu         = True,               # use PyTorch GPU for temporal filtering if available
)
 
 
# =============================================================================
# ▌ 2. COLOR-SPACE HELPERS
# =============================================================================
 
# YIQ conversion matrices (from/to float BGR in [0,1])
_BGR2YIQ = np.array([
    [0.114,  0.587,  0.299 ],
    [0.436, -0.275, -0.321 ],
    [-0.100, -0.523, 0.311 ],
], dtype=np.float32)
 
_YIQ2BGR = np.linalg.inv(_BGR2YIQ).astype(np.float32)
 
 
def bgr_to_yiq(frame: np.ndarray) -> np.ndarray:
    """Convert float32 BGR [0,1] → YIQ."""
    return frame @ _BGR2YIQ.T
 
 
def yiq_to_bgr(frame: np.ndarray) -> np.ndarray:
    """Convert float32 YIQ → BGR [0,1], clamped."""
    return np.clip(frame @ _YIQ2BGR.T, 0.0, 1.0)
 
# =============================================================================
# ▌ 3. VIDEO I/O
# =============================================================================
 
def read_video(path: str, color_space: str = "YIQ"):
    """
    Read all frames from *path*, convert to float32.
 
    Returns
    -------
    frames : np.ndarray  shape (T, H, W, C)  float32
    fps    : float
    """
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {path}")
 
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = []
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        f = cv2.resize(bgr, (48, 48)) 
        f = f.astype(np.float32) / 255.0
        if color_space == "YIQ":
            f = bgr_to_yiq(f)
        frames.append(f)
    cap.release()
 
    if not frames:
        raise ValueError(f"No frames read from {path}")
    return np.stack(frames, axis=0), fps
 
 
def write_video(path: str, frames: np.ndarray, fps: float,
                color_space: str = "YIQ", fourcc: str = "mp4v"):
    """
    Write float32 frames (T, H, W, C) to *path*.
    Converts back to BGR uint8 automatically.
    """
    T, H, W, _ = frames.shape
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fcc = cv2.VideoWriter_fourcc(*fourcc)
    vw  = cv2.VideoWriter(path, fcc, fps, (W, H))
    for f in frames:
        if color_space == "YIQ":
            f = yiq_to_bgr(f)
        bgr_u8 = np.clip(f * 255.0, 0, 255).astype(np.uint8)
        vw.write(bgr_u8)
    vw.release()
 
 
# =============================================================================
# ▌ 4. SPATIAL DECOMPOSITION — Gaussian & Laplacian Pyramids
# =============================================================================
 
def gaussian_pyramid(frame: np.ndarray, n_levels: int):
    """
    Build a Gaussian pyramid for a single HxWxC frame.
    Returns list of n_levels+1 arrays (original + downsampled levels).
    """
    pyramid = [frame]
    for _ in range(n_levels):
        frame = cv2.pyrDown(frame)
        pyramid.append(frame)
    return pyramid
 
 
def laplacian_pyramid(frame: np.ndarray, n_levels: int):
    """
    Build a Laplacian pyramid (band-pass spatial decomposition).
    Returns list of n_levels arrays (residuals) + 1 low-freq residual.
    """
    g_pyr = gaussian_pyramid(frame, n_levels)
    l_pyr = []
    for i in range(n_levels):
        up = cv2.pyrUp(g_pyr[i + 1], dstsize=(g_pyr[i].shape[1], g_pyr[i].shape[0]))
        l_pyr.append(g_pyr[i] - up)
    l_pyr.append(g_pyr[n_levels])   # lowest-frequency residual
    return l_pyr
 
 
def reconstruct_from_laplacian(l_pyr: list) -> np.ndarray:
    """Collapse a Laplacian pyramid back to a full-resolution frame."""
    frame = l_pyr[-1]
    for lap in reversed(l_pyr[:-1]):
        frame = cv2.pyrUp(frame, dstsize=(lap.shape[1], lap.shape[0]))
        frame = frame + lap
    return frame
 
 
# =============================================================================
# ▌ 5. BUILD SPATIAL PYRAMID STACK  (all frames)
# =============================================================================
 
def build_pyramid_stack(frames: np.ndarray, pyr_type: str, n_levels: int,
                        pre_smooth: bool = False, smooth_ksize: int = 3):
    """
    Apply spatial pyramid decomposition to every frame.
 
    Parameters
    ----------
    frames : (T, H, W, C)
 
    Returns
    -------
    pyr_stack : list of n_levels+1 arrays, each (T, h_l, w_l, C)
    """
    T = frames.shape[0]
 
    # Optional pre-smoothing (reduces hard mask-edge artifacts)
    if pre_smooth:
        k = smooth_ksize if smooth_ksize % 2 == 1 else smooth_ksize + 1
        frames = np.stack(
            [cv2.GaussianBlur(f, (k, k), 0) for f in frames], axis=0
        )
 
    # Decompose first frame to determine level shapes
    if pyr_type == "laplacian":
        sample_pyr = laplacian_pyramid(frames[0], n_levels)
    else:
        sample_pyr = gaussian_pyramid(frames[0], n_levels)
 
    n_lvls = len(sample_pyr)
    # Pre-allocate
    pyr_stack = [
        np.zeros((T,) + lvl.shape, dtype=np.float32)
        for lvl in sample_pyr
    ]
 
    # Fill for each frame
    for t, f in enumerate(frames):
        if pyr_type == "laplacian":
            pyr = laplacian_pyramid(f, n_levels)
        else:
            pyr = gaussian_pyramid(f, n_levels)
        for lv in range(n_lvls):
            pyr_stack[lv][t] = pyr[lv]
 
    return pyr_stack
 
# =============================================================================
# ▌ 6. TEMPORAL BANDPASS FILTERING
# =============================================================================
 
def _iir_bandpass(signal_t: np.ndarray, fps: float,
                  f_low: float, f_high: float, order: int = 2) -> np.ndarray:
    """
    Apply zero-phase Butterworth bandpass along axis 0 (time).
 
    signal_t : (T, ...) float32
    Returns   : same shape, filtered
    """
    nyq = fps / 2.0
    lo  = max(f_low  / nyq, 1e-4)
    hi  = min(f_high / nyq, 1.0 - 1e-4)
    if lo >= hi:
        raise ValueError(f"Invalid bandpass: [{f_low}, {f_high}] Hz at {fps} fps")
 
    sos = butter(order, [lo, hi], btype="bandpass", output="sos")
 
    # sosfiltfilt along axis 0 (time) — handles multi-dim arrays
    T = signal_t.shape[0]
    orig_shape = signal_t.shape
    flat = signal_t.reshape(T, -1)          # (T, N)
 
    # Minimum padlen for sosfiltfilt = 3 * max(filter order)
    padlen = min(3 * (2 * order + 1), T - 1)
    filtered = sosfiltfilt(sos, flat, axis=0, padlen=padlen)
    return filtered.reshape(orig_shape).astype(np.float32)
 
 
def _fft_bandpass(signal_t: np.ndarray, fps: float,
                  f_low: float, f_high: float) -> np.ndarray:
    """
    Ideal (brick-wall) bandpass via FFT — best for offline processing.
    Works along axis 0 (time).
    """
    T = signal_t.shape[0]
    orig_shape = signal_t.shape
    flat = signal_t.reshape(T, -1)          # (T, N)
 
    freqs  = np.fft.rfftfreq(T, d=1.0 / fps)
    fft_c  = np.fft.rfft(flat, axis=0)
 
    # Build ideal bandpass mask
    mask = ((freqs >= f_low) & (freqs <= f_high)).astype(np.float32)
    fft_c = fft_c * mask[:, None]
 
    filtered = np.fft.irfft(fft_c, n=T, axis=0)
    return filtered.reshape(orig_shape).astype(np.float32)
 
 
def temporal_filter(pyr_level: np.ndarray, fps: float,
                    f_low: float, f_high: float,
                    method: str = "iir", iir_order: int = 2) -> np.ndarray:
    """
    Apply temporal bandpass filter to a single pyramid level (T, h, w, C).
    """
    if method == "fft":
        return _fft_bandpass(pyr_level, fps, f_low, f_high)
    else:
        return _iir_bandpass(pyr_level, fps, f_low, f_high, order=iir_order)
 

from scipy.signal import detrend

def preprocess_signal(signal):
    """
    Remove drift, trim edges, apply window, normalize
    """
    # 1. Detrend (remove illumination drift)
    signal = detrend(signal, type='linear')

    # 2. Remove edge artifacts
    if len(signal) > 20:
        signal = signal[10:-10]

    # 3. Apply window (reduce FFT leakage)
    window = np.hanning(len(signal))
    signal = signal * window

    # 4. Normalize
    signal = (signal - np.mean(signal)) / (np.std(signal) + 1e-8)

    return signal

def fft_bandpass_1d(signal, fps, f_low, f_high):
    T = len(signal)

    freqs = np.fft.rfftfreq(T, d=1/fps)
    fft_signal = np.fft.rfft(signal)

    mask = (freqs >= f_low) & (freqs <= f_high)
    fft_signal = fft_signal * mask.astype(np.float32)

    filtered = np.fft.irfft(fft_signal, n=T)
    return filtered

def compute_snr(signal, fps, f_low, f_high):
    freqs, psd = welch(signal, fs=fps, nperseg=min(256, len(signal)))

    band = (freqs >= f_low) & (freqs <= f_high)
    peak_power = np.max(psd[band])
    noise_power = np.mean(psd[~band] + 1e-8)

    snr = 10 * np.log10(peak_power / noise_power)
    return snr


def compute_confidence(signal, fps, f_low, f_high):
    freqs, psd = welch(signal, fs=fps)

    band = (freqs >= f_low) & (freqs <= f_high)
    peak = np.max(psd[band])
    total = np.sum(psd)

    return peak / (total + 1e-8)



# =============================================================================
# ▌ 7. AMPLIFICATION  (with optional spatial-frequency attenuation)
# =============================================================================
 
def compute_alpha_for_level(alpha: float, level: int, total_levels: int,
                             lambda_cutoff: float | None) -> float:
    """
    Eq. (14) from Wu et al.: attenuate alpha for high spatial frequencies.
 
    For the color-amplification use-case (rPPG / heart rate from face),
    high-frequency bands are typically set alpha=0 (only lowest bands matter).
    For motion magnification, use a linear ramp as described in the paper.
 
    lambda_cutoff : spatial wavelength in pixels below which alpha is attenuated.
                    If None, full alpha is applied at every level.
    """
    if lambda_cutoff is None:
        return alpha
 
    # Approximate spatial wavelength at this pyramid level
    # Each level doubles the effective pixel size
    lambda_level = 2.0 ** (level + 1)      # pixels at original resolution
 
    if lambda_level >= lambda_cutoff:
        return alpha
    else:
        # Linear ramp: scale alpha down to 0 at highest frequencies
        return alpha * (lambda_level / lambda_cutoff)
 
# =============================================================================
# ▌ 8. FULL EVM PIPELINE  (single video)
# =============================================================================
 
def run_evm(video_path: str, cfg: dict) -> dict:
    """
    Run Eulerian Video Magnification on a single video.
 
    Returns a dict with keys:
      "amplified_frames" : (T, H, W, C) float32 in original color space
      "signal_hr"        : (T,)  1-D mean-Y (luminance) for HR estimation
      "signal_rr"        : (T,)  1-D mean-Y for RR estimation
      "fps"              : frame rate used
    """
    print("    Starting EVM processing...")

    # ── 8.1  Read frames ──────────────────────────────────────────────────────
    print(f"  Reading: {os.path.basename(video_path)}")
    frames_orig, fps_detected = read_video(video_path, cfg["color_space"])
    fps = cfg.get("fps") or fps_detected
    T, H, W, C = frames_orig.shape
    print(f"    Frames: {T}  Size: {W}×{H}  FPS: {fps:.1f}")
 
    if T < 10:
        raise ValueError(f"Video too short ({T} frames). Need ≥ 10.")
 
    # Nyquist check
    nyq = fps / 2.0
    if cfg["freq_high_hr"] >= nyq:
        raise ValueError(
            f"HR high-cut {cfg['freq_high_hr']} Hz exceeds Nyquist {nyq:.1f} Hz "
            f"(FPS={fps}). Lower freq_high_hr or increase FPS."
        )
 
    # ── 8.2  Build pyramid stack ───────────────────────────────────────────────
    print("    Building pyramid stack …")
    pyr_stack = build_pyramid_stack(
        frames_orig,
        pyr_type   = cfg["pyramid_type"],
        n_levels   = cfg["n_levels"],
        pre_smooth = cfg["pre_smooth"],
        smooth_ksize = cfg["smooth_ksize"],
    )
    n_lvls = len(pyr_stack)
 
    # ── 8.3  Temporal filtering + amplification per level ─────────────────────
    # Choose which frequency band to amplify in the output video
    if cfg["target"] == "hr":
        fl, fh = cfg["freq_low_hr"], cfg["freq_high_hr"]
    else:
        fl, fh = cfg["freq_low_rr"], cfg["freq_high_rr"]
 
    print(f"    Temporal filter [{fl}–{fh} Hz] ({cfg['filter_method'].upper()}) …")
    filtered_stack = []
    for lv, pyr_level in enumerate(pyr_stack):
        alpha_lv = compute_alpha_for_level(
            cfg["alpha"], lv, n_lvls, cfg.get("lambda_cutoff")
        )
 
        # For color amplification (rPPG), suppress fine spatial detail
        # i.e. only amplify the coarsest levels (standard practice)
        if cfg["pyramid_type"] == "gaussian" and lv < n_lvls - 1:
            # Only lowest-frequency Gaussian level carries the pulse signal
            filtered_stack.append(np.zeros_like(pyr_level))
            continue
 
        filt = temporal_filter(
            pyr_level,
            fps      = fps,
            f_low    = fl,
            f_high   = fh,
            method   = cfg["filter_method"],
            iir_order= cfg["iir_order"],
        )
        # Amplify
        filtered_stack.append(filt * alpha_lv)
 
    # ── 8.4  Reconstruct amplified frames ─────────────────────────────────────
    print("    Reconstructing frames …")
    amplified = np.zeros_like(frames_orig)
 
    if cfg["pyramid_type"] == "laplacian":
        # Build amplified pyramid and collapse
        for t in range(T):
            amp_pyr = [filtered_stack[lv][t] for lv in range(n_lvls)]
            delta   = reconstruct_from_laplacian(amp_pyr)
            # Add amplified delta to original; clamp after color conversion
            amplified[t] = frames_orig[t] + delta
 
    else:
        # Gaussian: upsample the amplified lowest level and add to original
        lowest_lv = n_lvls - 1
        amp_low   = filtered_stack[lowest_lv]
        for t in range(T):
            up = amp_low[t]
            # Upsample back to original resolution
            for _ in range(lowest_lv):
                up = cv2.pyrUp(up, dstsize=(up.shape[1] * 2, up.shape[0] * 2))
            # Match size (pyrDown/Up may be off by 1 pixel)
            up = cv2.resize(up, (W, H), interpolation=cv2.INTER_LINEAR)
            amplified[t] = frames_orig[t] + up
 
# ── 8.5  Extract 1-D temporal signals for HR / RR estimation ─────────────

    # --- Use amplified frames directly ---
    if cfg["color_space"] == "YIQ":
        y_channel = amplified[..., 0]   # luminance
    else:
        y_channel = amplified.mean(axis=-1)

    # --- Simple spatial averaging (NO MASK — already ROI input) ---
    raw_signal = y_channel.reshape(T, -1).mean(axis=1)

    # --- PREPROCESS (detrend + trim + window + normalize) ---
    raw_signal = preprocess_signal(raw_signal)

    # --- FILTER (bandpass via FFT) ---
    signal_hr = fft_bandpass_1d(
        raw_signal, fps,
        cfg["freq_low_hr"], cfg["freq_high_hr"]
    )

    signal_rr = fft_bandpass_1d(
        raw_signal, fps,
        cfg["freq_low_rr"], cfg["freq_high_rr"]
    )

    # --- QUALITY METRICS ---
    snr_hr = compute_snr(signal_hr, fps, cfg["freq_low_hr"], cfg["freq_high_hr"])
    conf_hr = compute_confidence(signal_hr, fps, cfg["freq_low_hr"], cfg["freq_high_hr"])

    print(f"    HR SNR: {snr_hr:.2f} dB | Confidence: {conf_hr:.3f}")

    return {
        "amplified_frames": amplified,
        "signal_hr"        : signal_hr,
        "signal_rr"        : signal_rr,
        "raw_signal"       : raw_signal,
        "fps"              : fps,
    }
 
# =============================================================================
# ▌ 9. SIGNAL ANALYSIS  — frequency estimation (HR / RR in BPM / BrPM)
# =============================================================================
 
def estimate_rate_from_signal(signal: np.ndarray, fps: float,
                               f_low: float, f_high: float) -> float:
    """
    Estimate dominant frequency (bpm) from a 1-D temporal signal using Welch's PSD.
    """
    nperseg = min(256, len(signal))
    freqs, psd = welch(signal, fs=fps, nperseg=nperseg)

    # DEBUG PLOT (optional)
#    plt.plot(freqs, psd)
 #   plt.title("PSD")
  #  plot_path = os.path.join(cfg["output_dir"], f"{stem}_signals.png")
   # plt.savefig(plot_path, dpi=150, bbox_inches="tight")

    mask = (freqs >= f_low) & (freqs <= f_high)

    if mask.sum() == 0:
        return float("nan")

    valid_freqs = freqs[mask]
    valid_psd = psd[mask]

    # ignore very low edge of band (common noise)
    min_valid = valid_freqs > (f_low + 0.1)

    valid_freqs = valid_freqs[min_valid]
    valid_psd = valid_psd[min_valid]

    dominant_freq = valid_freqs[np.argmax(valid_psd)]

    return dominant_freq * 60.0
 
# =============================================================================
# ▌ 10. SAVE OUTPUTS
# =============================================================================
 
def save_outputs(result: dict, out_stem: str, cfg: dict):
    """Save amplified video, signal arrays, and a summary plot."""
    os.makedirs(cfg["output_dir"], exist_ok=True)
 
    # ── Video ──────────────────────────────────────────────────────────────────
    if cfg["save_video"]:
        vid_path = os.path.join(cfg["output_dir"], f"{out_stem}_evm.mp4")
        write_video(
            vid_path,
            result["amplified_frames"],
            result["fps"],
            color_space = cfg["color_space"],
            fourcc      = cfg["fourcc"],
        )
        print(f"    Video saved → {vid_path}")
 
    # ── Signal arrays ──────────────────────────────────────────────────────────
    if cfg["save_signal"]:
        np.save(
            os.path.join(cfg["output_dir"], f"{out_stem}_signal_hr.npy"),
            result["signal_hr"],
        )
        np.save(
            os.path.join(cfg["output_dir"], f"{out_stem}_signal_rr.npy"),
            result["signal_rr"],
        )
 
        # ── Plot ───────────────────────────────────────────────────────────────
        fps = result["fps"]
        T   = len(result["raw_signal"])
        t   = np.arange(T) / fps
 
        hr_bpm = estimate_rate_from_signal(
            result["signal_hr"], fps, cfg["freq_low_hr"], cfg["freq_high_hr"]
        )
        rr_brpm = estimate_rate_from_signal(
            result["signal_rr"], fps, cfg["freq_low_rr"], cfg["freq_high_rr"]
        )
 
        fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=False)
 
        axes[0].plot(t, result["raw_signal"], color="steelblue", lw=0.8)
        axes[0].set_title("Raw mean luminance signal")
        axes[0].set_ylabel("Intensity"); axes[0].grid(True, alpha=0.3)
 
        axes[1].plot(t, result["signal_hr"], color="tomato", lw=1.0)
        axes[1].set_title(
            f"HR bandpass [{cfg['freq_low_hr']}–{cfg['freq_high_hr']} Hz]  "
            f"→  Estimated HR ≈ {hr_bpm:.1f} BPM"
        )
        axes[1].set_ylabel("Amplitude"); axes[1].grid(True, alpha=0.3)
 
        axes[2].plot(t, result["signal_rr"], color="seagreen", lw=1.0)
        axes[2].set_title(
            f"RR bandpass [{cfg['freq_low_rr']}–{cfg['freq_high_rr']} Hz]  "
            f"→  Estimated RR ≈ {rr_brpm:.1f} Br/min"
        )
        axes[2].set_xlabel("Time (s)"); axes[2].set_ylabel("Amplitude")
        axes[2].grid(True, alpha=0.3)
 
        plt.suptitle(f"EVM Vital-Sign Signals — {out_stem}", fontweight="bold")
        plt.tight_layout()
        plot_path = os.path.join(cfg["output_dir"], f"{out_stem}_signals.png")
        plt.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"    Plot  saved → {plot_path}")
        print(f"    Estimated HR : {hr_bpm:.1f} BPM")
        print(f"    Estimated RR : {rr_brpm:.1f} Br/min")
 
     # =============================================================================
# ▌ 11. BATCH PROCESSING LOOP
# =============================================================================
 
def process_folder(cfg: dict):
    """
    Find all videos matching cfg['ext'] in cfg['input_dir'] and run EVM.
    Results are written to cfg['output_dir'].
    """
    pattern = os.path.join(cfg["input_dir"], cfg["ext"])
    video_files = sorted(glob.glob(pattern))
 
    if not video_files:
        print(f"[WARN] No videos found matching: {pattern}")
        return
 
    print(f"\nFound {len(video_files)} video(s) in '{cfg['input_dir']}'")
    print(f"Output directory: '{cfg['output_dir']}'\n")
    print("=" * 60)
 
    summary = []
    for i, vp in enumerate(video_files, 1):
        stem = os.path.splitext(os.path.basename(vp))[0]
        print(f"\n[{i}/{len(video_files)}] {stem}")
        try:
            result = run_evm(vp, cfg)
            save_outputs(result, stem, cfg)
 
            fps = result["fps"]
            hr  = estimate_rate_from_signal(
                result["signal_hr"], fps, cfg["freq_low_hr"], cfg["freq_high_hr"]
            )
            rr  = estimate_rate_from_signal(
                result["signal_rr"], fps, cfg["freq_low_rr"], cfg["freq_high_rr"]
            )
            summary.append({"file": stem, "HR_bpm": hr, "RR_brpm": rr})
 
        except Exception as e:
            print(f"    [ERROR] Skipped — {e}")
            summary.append({"file": stem, "HR_bpm": float("nan"), "RR_brpm": float("nan")})
 
    # ── Print summary table ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"{'File':<30}  {'HR (BPM)':>10}  {'RR (Br/min)':>12}")
    print("-" * 60)
    for row in summary:
        print(f"{row['file']:<30}  {row['HR_bpm']:>10.1f}  {row['RR_brpm']:>12.1f}")
    print("=" * 60)
 
    # Optionally save summary CSV
    csv_path = os.path.join(cfg["output_dir"], "evm_summary.csv")
    with open(csv_path, "w") as f:
        f.write("file,HR_bpm,RR_brpm\n")
        for row in summary:
            f.write(f"{row['file']},{row['HR_bpm']:.2f},{row['RR_brpm']:.2f}\n")
    print(f"\nSummary CSV → {csv_path}")
 
 
# =============================================================================
# ▌ 12. CLI ENTRY POINT
# =============================================================================
 
def parse_args():
    p = argparse.ArgumentParser(description="Eulerian Video Magnification — Vital Signs Pipeline")
    p.add_argument("--input_dir",     default=DEFAULT_CFG["input_dir"])
    p.add_argument("--output_dir",    default=DEFAULT_CFG["output_dir"])
    p.add_argument("--ext",           default=DEFAULT_CFG["ext"])
    p.add_argument("--fps",           type=float, default=DEFAULT_CFG["fps"])
    p.add_argument("--alpha",         type=float, default=DEFAULT_CFG["alpha"])
    p.add_argument("--target",        choices=["hr", "rr"], default=DEFAULT_CFG["target"])
    p.add_argument("--pyramid_type",  choices=["laplacian", "gaussian"], default=DEFAULT_CFG["pyramid_type"])
    p.add_argument("--n_levels",      type=int, default=DEFAULT_CFG["n_levels"])
    p.add_argument("--filter_method", choices=["iir", "fft"], default=DEFAULT_CFG["filter_method"])
    p.add_argument("--freq_low_hr",   type=float, default=DEFAULT_CFG["freq_low_hr"])
    p.add_argument("--freq_high_hr",  type=float, default=DEFAULT_CFG["freq_high_hr"])
    p.add_argument("--freq_low_rr",   type=float, default=DEFAULT_CFG["freq_low_rr"])
    p.add_argument("--freq_high_rr",  type=float, default=DEFAULT_CFG["freq_high_rr"])
    p.add_argument("--color_space",   choices=["YIQ", "BGR"], default=DEFAULT_CFG["color_space"])
    p.add_argument("--no_video",      action="store_true")
    p.add_argument("--no_signal",     action="store_true")
    return p.parse_args()
 
 
if __name__ == "__main__":
    args = parse_args()
    cfg  = dict(DEFAULT_CFG)   # start from defaults
    cfg.update(vars(args))     # override with CLI args
    cfg["save_video"]  = not args.no_video
    cfg["save_signal"] = not args.no_signal
    process_folder(cfg)
 
 
