import React, { useState, useEffect } from 'react';
import './LoadingWave.css'; // アニメーション用のCSS

const loadingTexts = [
  { lang: "English", text: "Processing English Audio..." },
  { lang: "Indonesian", text: "Memproses Audio Bahasa..." }, // インドネシア語での処理中表現
  { lang: "Japanese", text: "音声を解析・翻訳中..." }
];

export default function MultilingualLoading() {
  const [currentIndex, setCurrentIndex] = useState(0);

  // 数秒ごとに言語（テキスト）を切り替えるタイマー
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % loadingTexts.length);
    }, 3000); // 3秒ごとに切り替え
    return () => clearInterval(timer);
  }, []);

  const currentItem = loadingTexts[currentIndex];

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-slate-900 rounded-xl">
      {/* 言語の切り替わり表示 */}
      <div className="text-xs font-semibold tracking-wider text-indigo-400 uppercase mb-2 transition-opacity duration-500">
        - {currentItem.lang} -
      </div>

      {/* ウェーブするテキスト（1文字ずつ分解してアニメーションさせる） */}
      <div className="flex space-x-1 text-xl font-bold text-white">
        {currentItem.text.split("").map((char, index) => (
          <span
            key={index}
            className="wave-char"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            {char === " " ? "\u00A0" : char}
          </span>
        ))}
      </div>
    </div>
  );
}