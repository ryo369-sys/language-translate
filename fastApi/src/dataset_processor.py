import os
import torch
import pandas as pd
import torchaudio
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

# 1. MDC からダウンロード関数をインポート
from datacollective import download_dataset

# 2. PyTorch 用 Dataset クラス（前回作成したものと同じ）
class CommonVoiceDataset(Dataset):
    def __init__(self, tsv_path: str, audio_dir: str, target_sr: int = 16000):
        self.audio_dir = audio_dir
        self.target_sr = target_sr
        
        df = pd.read_csv(tsv_path, sep="\t")
        
        self.data = []
        for _, row in df.iterrows():
            file_path = os.path.join(audio_dir, row['path'])
            if os.path.exists(file_path):
                self.data.append({
                    "path": file_path,
                    "text": row['sentence']
                })
        print(f"有効データ数: {len(self.data)}件")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        waveform, sample_rate = torchaudio.load(item["path"])
        
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
            
        if sample_rate != self.target_sr:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=self.target_sr)
            waveform = resampler(waveform)

        return {
            "waveform": waveform.squeeze(0),
            "text": item["text"]
        }

def collate_fn(batch):
    waveforms = [item["waveform"] for item in batch]
    texts = [item["text"] for item in batch]
    waveforms_padded = pad_sequence(waveforms, batch_first=True, padding_value=0.0)
    return {"waveforms": waveforms_padded, "texts": texts}


# --- メインの実行ブロック ---
if __name__ == "__main__":
    
    # 3. ここで download_dataset を呼び出してデータをダウンロードする！
    # （※ 画面に表示されていた Dataset ID を指定します）
    print("データセットをダウンロード中...")
    dataset_path = download_dataset("cmu5wcato00cknq07yjnu14e0")
    print(f"ダウンロード完了！ 保存先パス: {dataset_path}")
    
    # 4. ダウンロードされたパスを基準にして、TSVファイルや音声フォルダの場所を指定する
    # （※ 実際のフォルダ構造に合わせてパスを調整してください）
    tsv_file = os.path.join(dataset_path,"id", "validated.tsv")
    audio_folder = os.path.join(dataset_path, "id", "clips")
    
    # 5. 自作の PyTorch Dataset と DataLoader に繋ぎ込む
    if os.path.exists(tsv_file):
        dataset = CommonVoiceDataset(tsv_path=tsv_file, audio_dir=audio_folder)
        
        dataloader = DataLoader(
            dataset, 
            batch_size=4, 
            shuffle=True, 
            collate_fn=collate_fn
        )
        
        # 動作確認
        for batch in dataloader:
            print("\n--- PyTorch Batch Output ---")
            print("Waveforms Tensor Shape:", batch["waveforms"].shape)
            print("Sample Text:", batch["texts"][0])
            break