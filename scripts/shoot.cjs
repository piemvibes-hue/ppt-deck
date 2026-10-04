// PPT 素材拍摄管线 —— 全景 dsf=2 + 组件裁切 dsf=3
// 用法：BASE=http://localhost:5173 OUT=./shots node shoot.cjs
// 铁律：裁切一律 dsf=3（投 4-5in 槽位约 390dpi）；折叠卡片先点开再截；
// 有交互证据的状态（填入话术/警告条）先制造状态再截；命名即语义。
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.env.BASE || 'http://localhost:5173';
const OUT = process.env.OUT || './shots';
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
fs.mkdirSync(`${OUT}/crops`, { recursive: true });

const shot = async (page, name) => {
  await page.screenshot({ path: `${OUT}/${name}.png` });
  console.log('shot', name);
};

(async () => {
  const browser = await chromium.launch();

  // ① 全景页：dsf=2
  const ctx2 = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2, locale: 'zh-CN' });
  const page = await ctx2.newPage();
  // === 登录：改成你的登录路径 ===
  await page.goto(BASE + '/login', { waitUntil: 'networkidle' });
  await shot(page, 'login');
  // await page.getByRole('button', { name: /演示|Demo/ }).first().click();
  // await page.waitForSelector('text=工作台', { timeout: 25000 });
  await sleep(3000);
  await shot(page, 'overview');

  // ② 裁切页：dsf=3 重开 context（裁切卡才用；全景复用 ctx2 的）
  const ctx3 = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 3, locale: 'zh-CN' });
  const page3 = await ctx3.newPage();
  const crop = async (loc, name) => {
    if (await loc.count()) { await loc.first().screenshot({ path: `${OUT}/crops/${name}.png` }); console.log('crop', name); }
    else console.log('MISS crop', name);
  };
  // === 裁切清单：按页面表逐张拍 ===
  // await page3.goto(BASE + '/page', { waitUntil: 'networkidle' }); await sleep(3000);
  // await crop(page3.locator('text=组件标题').locator('xpath=ancestor::*[contains(@class,"rounded")][1]'), 'component_card');

  await browser.close();
})();
