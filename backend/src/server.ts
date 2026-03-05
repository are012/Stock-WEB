import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

// AI 분석 시뮬레이션 엔드포인트
app.post('/api/analyze', async (req, res) => {
  const { ticker } = req.body;
  
  console.log(`${ticker} 분석 요청 수신...`);
  
  // 실제 AI 모델 연동 위치 (예: OpenAI, Anthropic 등)
  // 현재는 시뮬레이션 결과를 반환합니다.
  await new Promise(resolve => setTimeout(resolve, 1500)); 

  const result = {
    ticker,
    decision: Math.random() > 0.4 ? "BUY" : "HOLD",
    score: Math.floor(Math.random() * 40) + 60,
    reason: "퀀트 지표(PBR, PER) 및 최근 거래량 급증 분석 결과 상승 가능성 높음",
    timestamp: new Date().toISOString()
  };

  res.json(result);
});

app.listen(PORT, () => {
  console.log(`🚀 백엔드 서버가 http://localhost:${PORT} 에서 실행 중입니다.`);
});
