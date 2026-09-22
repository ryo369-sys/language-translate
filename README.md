sql関係のDockerコンテナ設定次第でやる

作成予定テーブル

いいね　通報 ※userテーブルにプロフィールのデータを取得する

# Multi-Scale Audio Translation Model for Indonesian-English Code-Switching

YouTube等の動画・配信における**「インドネシア語と英語が混ざったカジュアルな音声（コードスイッチング）」**を、直接**日本語へ翻訳**する音声翻訳（End-to-End Speech Translation）モデルです。

会話速度の変化（早口・遅口）に強い堅牢なモデルを構築するため、**多速度メルスペクトログラムの特徴量統合（Multi-Speed Feature Fusion）**を採用しています。

---

## 課題意識と目的

* **背景**: インドネシアのVTuberやWebクリエイターの配信では、日常的にインドネシア語と英語が高度に混ざったカジュアルな会話が行われていますが、既存の翻訳モデルでは精度良く処理できない課題があります。
* **目的**: 
  1. 口語・スラングを含んだ混ざり言葉の音声に対応する。
  2. 配信特有の発話スピードの揺らぎ（早口・遅口）に対応する。
  3. 音声から直接日本語テキストを出力するパイプラインを構築する。

---

## システム構成 & モデルアーキテクチャ

### 処理パイプライン

1. **音声前処理（Speed Perturbation）**
   * 入力音声（16kHz Mono）から `0.8倍速`, `1.0倍速`, `1.2倍速` の3つの波形を生成（ピッチ維持）。
   * それぞれを **80次元 Log-Mel Spectrogram** に変換。
2. **Multi-Speed Feature Fusion（速度特徴量の平均統合）**
   * 3パターンのスペクトログラムを共通の Audio Encoder に入力。
   * 得られた中間特徴量ベクトルを平均（`torch.mean`）化し、話速の変化に対する堅牢性を向上。
3. **Text Generation (Decoder)**
   * 統合された特徴量から、日本語翻訳テキストを出力。

---

## データセット & ライセンス

商用利用可能なオープンデータセットおよび合成データを用いて構築しています。

* **音声データ**: 
  * [Mozilla Common Voice](https://commonvoice.mozilla.org/) (CC-0) - 基礎音声認識・音響モデル用
* **会話・並列テキストデータ**: 
  * [OpenSubtitles (OPUS)](https://opus.nlpl.eu/OpenSubtitles.php) - インドネシア語 ⇔ 英語（日常会話・スラング抽出）
  * [JESC](https://arxiv.org/abs/1710.10639) (CC BY-SA 4.0) - 英語 ⇔ 日本語（映画・アニメ字幕）
* **合成コードスイッチングデータ**:
  * OpenSubtitlesのインドネシア語テキストに対し、特定のカジュアル表現や接続詞（*So, Honestly, Literally* 等）を英語に置換するルールベース/LLM拡張を適用して作成。

---

## 開発・学習環境

* **OS**: Windows 11 Home
* **CPU**: AMD Ryzen 7 8700F
* **RAM**: 32GB DDR5
* **GPU**: NVIDIA GeForce RTX 5070 (VRAM 12GB / CUDA対応)
* **Framework**: PyTorch, torchaudio, librosa

---

## 使い方（Quick Start）

### 1. 依存ライブラリのインストール
```bash
pip install torch torchaudio librosa numpy
