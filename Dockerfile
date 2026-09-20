# NVIDIA CUDA + PyTorch 公式ベースイメージ
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# 環境変数の設定
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# システムパッケージ（Python, ffmpeg, sox 等）のインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ffmpeg \
    sox \
    libsox-fmt-all \
    git \
    && rm -rf /var/lib/apt/lists/*

# シンボリックリンクの作成 (python -> python3)
RUN ln -s /usr/bin/python3 /usr/bin/python

# ワークディレクトリエントリ
WORKDIR /app

# 依存関係のキャッシュとインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# プロジェクトコードのコピー
COPY . .

# FastAPI サーバーの起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]