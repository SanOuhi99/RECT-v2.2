/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config) => {
    config.resolve.extensions.push('.jsx', '.js');
    return config;
  },
};

module.exports = nextConfig;
