const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const WRAP = (body) => `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${body}</body></html>`;
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2) : ["shape", "heat", "cant", "stress"];
  const browser = await chromium.launch();
  for (const n of names) {
    const file = path.resolve(`out/_wrap_${n}.html`); fs.writeFileSync(file, WRAP(fs.readFileSync(`out/${n}.html`, "utf8")));
    for (const cfg of [{ tag: "desk", w: 1280, h: 900, scheme: "light" }, { tag: "phone", w: 390, h: 844, scheme: "dark" }]) {
      const ctx = await browser.newContext({ viewport: { width: cfg.w, height: cfg.h }, deviceScaleFactor: cfg.tag === "phone" ? 2 : 1, colorScheme: cfg.scheme });
      const page = await ctx.newPage(); const errs = [];
      page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") errs.push(m.type() + ": " + m.text()); });
      page.on("pageerror", (e) => errs.push("pageerror: " + e.message));
      await page.goto("file://" + file); await page.waitForTimeout(600);
      const btn = await page.$("#b-study"); if (btn) { await btn.click(); await page.waitForTimeout(1500); }
      const sw = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
      await page.screenshot({ path: `shots/${n}_${cfg.tag}.png`, fullPage: true });
      console.log(n, cfg.tag, "scrollWidth/clientWidth", sw.join("/"), errs.filter(e => !/fonts\.g/.test(e)).slice(0, 5).join(" | ") || "no errors");
      await ctx.close();
    }
  }
  await browser.close();
})();
