module.exports = {
  reactStrictMode: true,
  productionBrowserSourceMaps: false,
  optimizeFonts: true,
  output: 'standalone',
  compress: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://rect.up.railway.app:8080',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ]
  },
  experimental: {
      outputFileTracingRoot: path.join(__dirname, '../../')
    },
  images: {
    domains: ['rect.up.railway.app'],
  },
}
