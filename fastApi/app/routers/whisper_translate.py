from fastapi import FastAPI, UploadFile, File
import whisper

app = FastAPI()

# Whisperモデルを事前にロードしておく（共通の変数）
model = whisper.load_model("base")

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    
    # 0. アップロードされた音声を一時保存するなどの前処理
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await file.read())

    # ==========================================
    # ① Whisperを使って音声解析を行う部分
    # ==========================================
    # Whisperに音声を投げると、言語やタイムスタンプ付きのセグメント（辞書型の巨大なデータ）が返ってくる
    raw_result = model.transcribe(audio_path, task="transcribe")
    
    # raw_result の中身の例：
    # {
    #   "language": "en", 
    #   "segments": [
    #      {"start": 0.0, "end": 4.5, "text": " Hello everyone."},
    #      {"start": 4.5, "end": 8.0, "text": " Welcome to the show."}
    #   ]
    # }

    detected_language = raw_result["language"]  # 例: "en" または "id"
    raw_segments = raw_result["segments"]       # Whisperが検出した時間の切れ目ごとの配列

    # ==========================================
    # ② データの加工・整形部分
    # ==========================================
    # Whisperが返してきた生データはそのままでは使いづらい・またはDBの形と少し違うため、
    # 自分が使いやすいように「加工（パース）」してリスト形式の変数に整える
    processed_segments = []
    
    for seg in raw_segments:
        segment_data = {
            "start_time": seg["start"],          # 開始時間
            "end_time": seg["end"],              # 終了時間
            "text": seg["text"].strip(),         # 余分な空白を削ったテキスト
            "language": detected_language        # 検出された言語
        }
        processed_segments.append(segment_data)

    # （ここで、加工した processed_segments を MySQL の transcript_segments テーブルに INSERT する処理が入ります）


    # ==========================================
    # ③ レスポンス変数の定義と返却
    # ==========================================
    # フロントエンド（画面）に返すためのデータを「レスポンス用の変数（辞書）」としてまとめる
    response_data = {
        "status": "success",
        "detected_language": detected_language,
        "segment_count": len(processed_segments),
        "segments": processed_segments  # ← これが最終的に画面側で使われるレスポンス変数！
    }

    # FastAPIが自動でこれをJSONに変換してブラウザやアプリに返してくれる
    return response_data