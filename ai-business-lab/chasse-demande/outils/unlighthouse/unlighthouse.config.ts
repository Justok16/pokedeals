export default {
  puppeteerOptions: { executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox', '--headless=new'] },
  chrome: { useSystem: false },
  scanner: { device: 'mobile', samples: 1, maxRoutes: 30 },
  ci: { budget: 80 },
}
