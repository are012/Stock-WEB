import { useState } from "react";

// Cloudflare useAgent를 로컬에서 흉내내는 Mock 훅입니다.
export function useAgent({ agent, onStateUpdate }: { agent: string, onStateUpdate?: (state: any) => void }) {
  const [state, setState] = useState({
    portfolio: ["삼성전자"],
    signals: [],
    lastAnalysis: "로컬 시뮬레이션 모드"
  });

  // RPC 호출을 흉내내는 stub 객체
  const stub = {
    getFinalDecision: async (ticker: string) => {
      console.log(`${ticker} 분석 시뮬레이션 시작...`);
      await new Promise(resolve => setTimeout(resolve, 1500)); // 1.5초 대기
      
      const result = {
        ticker,
        decision: Math.random() > 0.3 ? "APPROVED" : "REJECTED",
        reason: "로컬 시뮬레이션: 퀀트 지표 및 리스크 엔진 정상 작동 확인"
      };
      
      if (onStateUpdate) onStateUpdate({ ...state, lastAnalysis: `${ticker} 분석 완료` });
      return result;
    }
  };

  return { stub, state };
}
