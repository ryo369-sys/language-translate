from datasets import load_from_disk

# 同じ場所にある 'my_dataset' フォルダから読み込む
dataset = load_from_disk("./my_dataset")

# 読み込み確認（最初のデータセットを表示）
first_data = dataset['train'][0]

print("テキスト:", first_data['text'])  # もしくは書き起こしテキストのキー名
print("音声データ:", first_data['audio'])