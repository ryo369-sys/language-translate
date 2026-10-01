// ① セグメント（1行ごとのテキストと時間）の型
export interface TranscriptSegment {
  start_time: number;
  end_time: number;
  text: string;
  language: string;
}

// ② FastAPI全体のレスポンス（APIの戻り値）の型
export interface TranscribeResponse {
  status: string;
  detected_language: string;
  segment_count: number;
  segments: TranscriptSegment[]; // ← ①の型を配列として持たせる
}