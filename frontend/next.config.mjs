/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // 정적 HTML 배포를 위해 필수
  images: {
    unoptimized: true, // 정적 배포 시 이미지 최적화 비활성화
  },
};

export default nextConfig;
