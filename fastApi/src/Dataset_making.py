import os
import pandas as pd
from datasets import Dataset, Audio
import json

def save_to_jsonl(data_records, output_jsonl="dataset.jsonl"):
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for record in data_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{output_jsonl} に保存しました！")

def prepare_code_switching_dataset(tsv_path, audio_dir, output_jsonl="dataset.jsonl"):
    """
    Mozilla Common VoiceなどのTSVメタデータと音声ディレクトリから、
    Whisper用のデータセット構造を構築するサンプルコード
    """
    if not os.path.exists(tsv_path):
        print(f"エラー: メタデータファイルが見つかりません: {tsv_path}")
        return
    
    # Common Voiceのメタデータ（tsv）を読み込み
    df = pd.read_csv(tsv_path, sep="\t")
    
    # 必要な列（音声ファイル名、文言）を抽出
    # 一般的に 'path' と 'sentence' カラムが含まれています
    if 'path' not in df.columns or 'sentence' not in df.columns:
        print("エラー: 期待されるカラム（path, sentence）がTSVに含まれていません。")
        return

    data_records = []
    for _, row in df.iterrows():
        audio_path = os.path.join(audio_dir, row['path'])
        text = row['sentence']
        
        if os.path.exists(audio_path):
            data_records.append({
                "audio": audio_path,
                "text": text
            })
            
    print(f"有効なデータ数: {len(data_records)}件")
    return data_records

# 実行例（パスはご自身の環境に合わせて書き換えてください）
# ts_v_file = "./cv-corpus/id/validated.tsv"
# audio_folder = "./cv-corpus/id/clips/"
# dataset = prepare_code_switching_dataset(ts_v_file, audio_folder)