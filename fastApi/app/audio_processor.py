import torchaudio
import torchaudio.transforms as T
import torch

def process_audio_multi_speed(file_path: str, target_sr: int = 16000, n_mels: int = 80):
    """
    音声を読み込み、0.8x / 1.0x / 1.2x の Log-Mel Spectrogram を生成する関数
    """
    # 1. 音声ファイルの読み込み
    waveform, sample_rate = torchaudio.load(file_path)

    # ステレオの場合はモノラル（1ch）に変換
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # 16kHzにリサンプリング
    if sample_rate != target_sr:
        resampler = T.Resample(orig_freq=sample_rate, new_freq=target_sr)
        waveform = resampler(waveform)

    # 2. 速度変更 (Speed Perturbation) 用の変換器
    # ※ピッチを維持しつつ速度だけ変更
    speeds = [0.8, 1.0, 1.2]
    mel_spectrograms = []

    mel_transform = T.MelSpectrogram(
        sample_rate=target_sr,
        n_fft=400,
        hop_length=160,
        n_mels=n_mels
    )

    for speed in speeds:
        if speed == 1.0:
            speed_waveform = waveform
        else:
            # 速度変更処理
            speed_waveform, _ = torchaudio.sox_effects.apply_effects_tensor(
                waveform, target_sr, [['speed', str(speed)], ['rate', str(target_sr)]]
            )
        
        # Log-Mel Spectrogram の抽出
        mel_spec = mel_transform(speed_waveform)
        log_mel_spec = torch.log(torch.clamp(mel_spec, min=1e-5)) # ゼロ割防止のlog変換
        
        mel_spectrograms.append(log_mel_spec)

    # 0.8x, 1.0x, 1.2x の 3つの Log-Mel スペクトログラムを返す
    return mel_spectrograms

if __name__ == "__main__":
    print("Audio processor module initialized.")