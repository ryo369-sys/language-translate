import os
import json
import pandas as pd
from transformers import pipeline

# --- 1. LLM（要約・翻訳）処理 ---
def summarize_text(text: str, target_lang: str = "ja") -> str:
    """
    指定された言語（標準は日本語）に要約・翻訳する関数
    """
    # 言語に応じたプロンプトテンプレート
    prompts = {
        "ja": f"以下のテキストを日本語で簡潔に要約してください:\n\n{text}",
        "id": f"Tolong ringkas teks berikut secara singkat dalam bahasa Indonesia:\n\n{text}",
        "en": f"Please summarize the following text briefly:\n\n{text}"
    }
    
    prompt_content = prompts.get(target_lang, prompts["ja"])
    
    # パイプラインの呼び出し
    summarizer = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B-Instruct", device_map="auto")
    
    messages = [{"role": "user", "content": prompt_content}]
    output = summarizer(messages, max_new_tokens=150, do_sample=False, return_full_text=False)
    
    return output[0]["generated_text"]


# --- 2. データセット保存処理 ---
def save_to_jsonl(data_records, output_jsonl="dataset.jsonl"):
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for record in data_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{output_jsonl} に保存しました！")


# --- 3. 音声メタデータ構築処理 ---
def prepare_code_switching_dataset(tsv_path, audio_dir):
    if not os.path.exists(tsv_path):
        print(f"エラー: メタデータファイルが見つかりません: {tsv_path}")
        return []
    
    df = pd.read_csv(tsv_path, sep="\t")
    
    if 'path' not in df.columns or 'sentence' not in df.columns:
        print("エラー: 期待されるカラム(path, sentence)がTSVに含まれていません。")
        return []

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


# --- メイン実行ブロック ---
if __name__ == "__main__":
    sample_text = """
    Amazon announced Friday evening that it has hired Covariant's founders Pieter Abbeel, Peter Chen, and Rocky Duan...
    """
    
    # 動作確認
    result = summarize_text(sample_text, target_lang="ja")
    print("--- Summary Result ---")
    print(result)