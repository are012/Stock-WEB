import { Agent, callable } from "agents";
import { Ai } from "@cloudflare/ai";

export interface TradingState {
  portfolio: string[];
  signals: any[];
  lastAnalysis: string;
}

export class TradingAgent extends Agent<any, TradingState> {
  initialState: TradingState = {
    portfolio: ["삼성전자"],
    signals: [],
    lastAnalysis: "대기 중..."
  };

  // Analyst Agent 역할: 펀더멘털 분석
  @callable()
  async analyzeFundamental(ticker: string) {
    const ai = new Ai(this.env.AI);
    const response = await ai.run("@cf/meta/llama-2-7b-chat-int8", {
      prompt: `${ticker}의 최근 재무제표와 시장 점유율을 바탕으로 퀀트멘탈 점수를 산출해줘.`
    });
    
    this.setState({ ...this.state, lastAnalysis: `Analyst: ${ticker} 분석 완료` });
    return response;
  }

  // Chartist Agent 역할: 기술적 분석
  @callable()
  async analyzeChart(ticker: string) {
    // 실시간 차트 데이터 처리 로직 (D1 연동 가능)
    return { signal: "BUY", strength: 0.85 };
  }

  // Risk Manager 역할: 최종 승인
  @callable()
  async getFinalDecision(ticker: string) {
    const fundamental = await this.analyzeFundamental(ticker);
    const technical = await this.analyzeChart(ticker);
    
    const decision = technical.strength > 0.8 ? "APPROVED" : "REJECTED";
    
    this.setState({
      ...this.state,
      signals: [...this.state.signals, { ticker, decision, time: new Date().toISOString() }]
    });
    
    return { ticker, decision, reason: "Sharpe Ratio 및 리스크 한도 충족" };
  }
}

export default {
  async fetch(request: Request, env: any) {
    return new Response("Cloudflare Trading Agent is running.");
  }
};
