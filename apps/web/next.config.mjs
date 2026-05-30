/** @type {import('next').NextConfig} */

// GitHub Pages serves under /Tripwire; Vercel serves at root.
// Gate basePath behind a CI flag so both hosts work from one config.
const isPages = process.env.GITHUB_PAGES === "true";
const repo = "Tripwire";

const nextConfig = {
  reactStrictMode: true,
  output: "export", // fully static — arena runs client-side with the local mirror
  images: { unoptimized: true },
  basePath: isPages ? `/${repo}` : "",
  assetPrefix: isPages ? `/${repo}/` : "",
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || "",
  },
};

export default nextConfig;
