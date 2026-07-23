# datasets ライブラリのインストール
# pip install datasets librosa soundfile

from datasets import load_dataset

# ① 以前ロードしたのと同じように書く（自動的にキャッシュから読み込まれます）
dataset = load_dataset("ZMaxwell-Smith/OIL")

# ② 保存したい「新しいフォルダ名」を指定するだけ！
dataset.save_to_disk("./my_dataset")