"use client";

import { useState, useEffect } from "react";
import { useAgent } from "agents/react";
import { TrendingUp, ShieldCheck, FileText, Activity, Play } from "lucide-react";

export default function Dashboard() {
  const [ticker, setTicker] = useState("삼성전자");
  const [decision, setDecision] = useState<any>(null);

  // Cloudflare TradingAgent 연결
  const agent = useAgent({
    agent: "TradingAgent",
    onStateUpdate: (state) => {
      console.log("에이전트 상태 업데이트:", state);
    },
  });

  const handleStartAnalysis = async () => {
    // 에이전트의 @callable() 메서드 호출
    const result = await agent.stub.getFinalDecision(ticker);
    setDecision(result);
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Cloudflare Agents AI 트레이딩</h1>
        <div className="status">
          <input 
            type="text" 
            value={ticker} 
            onChange={(e) => setTicker(e.target.value)}
            style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #333', background: '#222', color: '#fff' }}
          />
          <button 
            onClick={handleStartAnalysis}
            style={{ marginLeft: '1rem', padding: '0.5rem 1rem', background: '#0070f3', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Play size={16} /> 분석 시작
          </button>
        </div>
      </header>

      <div className="grid">
        {/* 실시간 결정 상태 */}
        <div className="card">
          <div className="card-title"><Activity size={20} /> AI 최종 결정</div>
          <div className="content">
            {decision ? (
              <>
                <h2 className={decision.decision === "APPROVED" ? "signal-buy" : "signal-sell"}>
                  {decision.decision}: {decision.ticker}
                </h2>
                <p>근거: {decision.reason}</p>
              </>
            ) : (
              <p>분석 버튼을 눌러 에이전트를 가동하세요.</p>
            )}
          </div>
        </div>

        {/* Cloudflare Agents 정보 */}
        <div className="card">
          <div className="card-title"><ShieldCheck size={20} /> 에이전트 인프라 (Durable Objects)</div>
          <p style={{ fontSize: '0.85rem', color: '#888' }}>
            이 에이전트는 Cloudflare 글로벌 네트워크의 각 엣지에서 상태를 유지하며 동작합니다.
          </p>
          <div className="xai-logic">
            - 위치: Region Earth<br />
            - 데이터베이스: Cloudflare D1 (SQLite)<br />
            - 모델: Workers AI (@cf/meta/llama-2)
          </div>
        </div>
      </div>
    </div>
  );
}
