// OCEANPERU 공통 상세페이지 빌더
// 사용법: node template/build.mjs            → products/* 전체 생성
//         node template/build.mjs maguro     → 한 제품만 생성
// 결과: template/<id>.html (CSS 인라인, 이미지는 products/<id>/ 상대경로)
import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const css = readFileSync(join(ROOT, "detail.css"), "utf8");
const LOGO = "../assets/web/logo-square.webp";

const esc = (s = "") => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

const qBadge = (n) => `<div class="q-badge" aria-hidden="true"><svg viewBox="0 0 132 242"><path d="M36 70a30 30 0 1 1 46 25c-12 8-16 14-16 30" fill="none" stroke="#d8433a" stroke-width="26" stroke-linecap="butt"/><circle cx="66" cy="178" r="64" fill="#d8433a"/><text x="66" y="194" text-anchor="middle" fill="#fff" font-family="Pretendard Variable,Pretendard,sans-serif" font-weight="900" font-size="44">Q ${n}</text></svg></div>`;

const wave = (flip = false) => `<div class="wave${flip ? " flip" : ""}" aria-hidden="true"></div>`;

function qHead(sec, n) {
  const word = sec.bgWord ? `<div class="q-bgword${/^\d+$/.test(sec.bgWord) ? " num" : ""}" aria-hidden="true">${esc(sec.bgWord)}</div>` : "";
  return `${word}${qBadge(n)}<h2 class="q-title">${esc(sec.question)}</h2>`;
}

const warn = (text) => `<div class="warn"><i aria-hidden="true"></i><p>${esc(text)}</p></div>`;

const renderers = {
  parts(sec, img) {
    const parts = sec.parts.map((p, i) => `
      <div class="part${i % 2 ? " rev" : ""}">
        <img src="${img(p.image)}" alt="${esc(p.name)}" loading="lazy">
        <div class="part-text">
          <div class="part-name"><b>${esc(p.name)}</b>${p.sub ? `<small>${esc(p.sub)}</small>` : ""}</div>
          <p class="part-desc">${esc(p.desc)}</p>
        </div>
      </div>`).join("");
    return `
      ${sec.image ? `<img class="parts-main" src="${img(sec.image)}" alt="" loading="lazy">` : ""}
      <div class="parts-intro">
        <h3>${sec.headline.map(esc).join("<br>")}</h3>
        <p class="t-body">${esc(sec.body)}</p>
      </div>
      <div class="parts-box"><h3>${esc(sec.partsTitle)}</h3>${parts}</div>`;
  },
  steps(sec, img) {
    const steps = sec.steps.map((s) => `
      <div class="step"><img src="${img(s.image)}" alt="${esc(s.caption)}" loading="lazy"><p>${esc(s.caption)}</p></div>`).join("");
    return `${sec.notice ? warn(sec.notice) : ""}<div class="steps">${steps}</div>${sec.footnote ? warn(sec.footnote) : ""}`;
  },
  packaging(sec, img) {
    return `
      <img class="pack-main" src="${img(sec.mainImage)}" alt="포장 상태" loading="lazy">
      <div class="pack-row"><img src="${img(sec.subImage)}" alt="" loading="lazy"><p>${esc(sec.note)}</p></div>
      <div class="pack-box"><img src="${img(sec.boxImage)}" alt="아이스 박스 포장" loading="lazy">
        <ul class="pack-quote">${sec.items.map((t) => `<li>${esc(t)}</li>`).join("")}</ul></div>`;
  },
  notice(sec) {
    return `<table class="notice"><tbody>${sec.rows.map(([k, v]) => `<tr><th scope="row">${esc(k)}</th><td>${esc(v)}</td></tr>`).join("")}</tbody></table>`;
  },
};

function render(p) {
  const img = (f) => `products/${p.id}/${f}`;
  const h = p.hero, cp = p.checkpoint;
  const sections = p.sections.map((sec, i) => {
    const fn = renderers[sec.type];
    if (!fn) throw new Error(`${p.id}: 알 수 없는 섹션 type "${sec.type}"`);
    return `${wave()}<section class="q q-${sec.type}">${qHead(sec, i + 1)}${fn(sec, img)}</section>`;
  }).join("\n");

  return `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(p.pageTitle)} | OCEANPERU</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>body{margin:0;background:#fff}
${css}</style>
</head>
<body>
<!-- OCEANPERU DETAIL START : Cafe24 상세설명에는 이 주석 사이(<style> 포함)만 붙여 넣으면 됩니다 -->
<article class="opd" id="opd-${p.id}">
  ${wave()}
  <header class="hero-head">
    <img class="hero-logo" src="${LOGO}" alt="OCEANPERU">
    ${h.fish !== false ? `<img class="hero-fish l" src="${img("deco-fish.webp")}" alt="" aria-hidden="true"><img class="hero-fish r" src="${img("deco-fish.webp")}" alt="" aria-hidden="true">` : ""}
    <p class="hero-tagline">${esc(h.tagline)}</p>
    <p class="hero-sub">${h.subtitleAccent ? `<em>${esc(h.subtitleAccent)}</em> ` : ""}${esc(h.subtitle)}</p>
    <h1 class="hero-title">${esc(h.title)}</h1>
  </header>
  ${wave()}
  <img class="hero-photo" src="${img(h.image)}" alt="${esc(h.imageAlt || h.title)}">
  ${wave()}
  <section class="cp">
    <div class="cp-bg" style="background-image:url('${img(cp.background)}')" aria-hidden="true"></div>
    <p class="cp-label">${esc(cp.label)}</p>
    <h2 class="cp-title">CHECK POINT!</h2>
    <div class="cp-uses">${cp.uses.map((u) => `<figure class="cp-card"><img src="${img(u.image)}" alt="${esc(u.label)}" loading="lazy"><span>${esc(u.label)}</span></figure>`).join("")}</div>
    <ol class="cp-points">${cp.points.map((pt, i) => `<li><b>${String(i + 1).padStart(2, "0")}<small>${esc(pt.key)}</small></b><p>${esc(pt.text)}</p></li>`).join("")}</ol>
  </section>
  ${sections}
</article>
<!-- OCEANPERU DETAIL END -->
</body>
</html>
`;
}

const only = process.argv[2];
const ids = only ? [only] : readdirSync(join(ROOT, "products")).filter((d) => existsSync(join(ROOT, "products", d, "data.json")));
for (const id of ids) {
  const data = JSON.parse(readFileSync(join(ROOT, "products", id, "data.json"), "utf8"));
  writeFileSync(join(ROOT, `${id}.html`), render(data));
  console.log(`✓ template/${id}.html`);
}
