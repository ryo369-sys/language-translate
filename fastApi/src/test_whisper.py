import whisper

# モデルのロード（最初は base や small などのサイズが軽くておすすめです）
model = whisper.load_model("base")

# 音声ファイルを渡して文字起こしを実行
result = model.transcribe("あなたの音声ファイル.mp3")

# 結果のテキストを出力
print(result["text"])