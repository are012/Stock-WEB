import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "QuantMental AI Trading",
  description: "AI 기반 퀀트멘탈 자동매매 대시보드",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
