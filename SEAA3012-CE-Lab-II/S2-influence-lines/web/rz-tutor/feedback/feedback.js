/* SPDX-License-Identifier: MIT
   Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia

   rz feedback — the Feedback tab of a T&L app: rate the part (1–5, with "what helped" and "what would
   help" chips and an optional comment), the muddiest point, report a mistake, like the page, and the
   "What's new" list. No dependencies; every label is a pair of <span class="en"> / <span class="ms">, so
   the page's own language switch shows the right one (placeholders and section names follow the
   page's data-lang or lang attribute).

   window.RzFeedback.mount({
     root: '#rzfeedback', app: 'seaa3012', part: 's2',
     endpoint: 'https://rz-tutor.<account>.workers.dev/v1/feedback',   // optional: else from <meta name="rz-tutor">
     manifest: 'tutor/manifest.json',                                    // section list for "where?"; optional
     whatsNew: [{ date: '2026-11-11', en: 'Feedback tab added', ms: 'Tab Maklum Balas ditambah' }],
   });

   Why it is like this: feedback is anonymous and goes only to the lecturer's report (the rz-tutor Worker
   scrubs e-mail, phone, IC and matric-like numbers, and keeps browser sessions as salted hashes); the
   page says so above the forms and asks for no names. Without a Worker address, or when the Worker has
   feedback off, the forms stay disabled and nothing leaves the browser. Requests are sent as
   text/plain so that the browser makes no CORS preflight.
*/
(function () {
  "use strict";
  const CHIPS = {
    helped: [["notes", "Notes", "Nota"], ["slides", "Slides", "Slides"], ["explorer", "Explorer", "Explorer"], ["examples", "Worked examples", "Contoh"],
      ["exercises", "Exercises", "Latihan"], ["glossary", "Glossary", "Glosari"], ["tutor", "Dr RJ", "Dr RJ"]],
    wish: [["more_examples", "More examples", "Lebih banyak contoh"], ["worked_steps", "Step-by-step solutions", "Penyelesaian langkah demi langkah"],
      ["clearer_notes", "Clearer notes", "Nota yang lebih jelas"], ["more_exercises", "More exercises", "Lebih banyak latihan"],
      ["video", "A short video", "Video ringkas"], ["slower_pace", "A slower pace", "Rentak yang lebih perlahan"]],
  };
  const STARS = [["Very poor", "Sangat lemah"], ["Poor", "Lemah"], ["OK", "Sederhana"], ["Good", "Baik"], ["Very good", "Sangat baik"]];
  const VIEW = { start: ["Start", "Mula"], notes: ["Notes", "Nota"], slides: ["Slides", "Slides"], explorer: ["Explorer", "Explorer"],
    examples: ["Examples", "Contoh"], exercises: ["Exercises", "Latihan"], lab: ["Lab", "Makmal"], glossary: ["Glossary", "Glosari"] };
  const MAX = 500;

  const ld = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
  const sv = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage blocked: the tab still works */ } };
  const sessionId = () => "s_" + Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, "0")).join("");
  const lang = () => { const r = document.documentElement; return (r.getAttribute("data-lang") || r.lang || "en").slice(0, 2) === "ms" ? "ms" : "en"; };

  function el(tag, cls, attrs) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  /** A bilingual label: <span class="en">…</span><span class="ms">…</span>, or a single span when both are the same. */
  function bi(en, ms, tag) {
    const w = el(tag || "span");
    if (en === ms) { w.textContent = en; return w; }
    const a = el("span", "en"); a.textContent = en; const b = el("span", "ms"); b.textContent = ms;
    w.append(a, b); return w;
  }
  function loopback(u) { try { const h = new URL(u).hostname; return h === "localhost" || h === "127.0.0.1" || h === "[::1]"; } catch (e) { return false; } }
  /** The feedback address: the config, else ?endpoint= (loopback only, for local tests), else the page's <meta name="rz-tutor"> chat address. */
  function resolveEndpoint(cfg) {
    const q = new URLSearchParams(location.search).get("endpoint");
    let u = (q && loopback(q)) ? q : (cfg.endpoint || ((document.querySelector('meta[name="rz-tutor"]') || {}).content || ""));
    u = String(u || "").trim();
    if (!u) return "";
    return u.replace(/\/v1\/(chat|feedback)(\?.*)?$/, "") + "/v1/feedback";
  }

  function mount(cfg) {
    const root = typeof cfg.root === "string" ? document.querySelector(cfg.root) : cfg.root;
    if (!root || root.dataset.rzfMounted) return null;
    root.dataset.rzfMounted = "1";
    const endpoint = resolveEndpoint(cfg);
    const key = "rzfb:" + cfg.app;
    const st = Object.assign({ session: sessionId(), parts: {} }, ld(key, {}));
    const mine = st.parts[cfg.part] = Object.assign({ score: 0, chips: [], liked: false }, st.parts[cfg.part] || {});
    const save = () => sv(key, st);
    const repaint = [];                       // things that are not spans (placeholders, <option> text) and follow the language
    let sections = [];
    let live = false;

    root.classList.add("rzf");
    root.textContent = "";

    // privacy notice
    const note = el("div", "rzf-note", { role: "note" });
    note.append(bi("Your feedback is anonymous and goes only to the lecturer, to improve this page from time to time. Please do not type your name, matric number or contact details. It is not used for marks or for research.",
      "Maklum balas anda tanpa nama dan hanya sampai kepada pensyarah, untuk menambah baik halaman ini dari semasa ke semasa. Jangan taip nama, nombor matrik atau butiran hubungan. Ia tidak digunakan untuk markah atau penyelidikan.", "p"));
    const offline = bi("Feedback opens once this page is connected to the course server. Nothing is sent from here until then.",
      "Maklum balas akan dibuka sebaik sahaja halaman ini disambungkan ke pelayan kursus. Sehingga itu, tiada apa yang dihantar dari sini.", "p");
    offline.className = "rzf-offline"; offline.hidden = true;
    note.append(offline);
    root.append(note);

    const grid = el("div", "rzf-grid");
    root.append(grid);

    function card(en, ms, cls) {
      const c = el("section", "rzf-card" + (cls ? " " + cls : ""));
      const h = bi(en, ms, "h3"); h.className = "rzf-h";
      c.append(h); grid.append(c); return c;
    }
    function status(box) { const s = el("p", "rzf-status", { role: "status", "aria-live": "polite" }); box.append(s); return s; }
    function say(s, en, ms, kind) { s.textContent = ""; s.className = "rzf-status" + (kind ? " rzf-" + kind : ""); if (en) s.append(bi(en, ms)); }
    function textarea(phEn, phMs) {
      const wrap = el("div", "rzf-ta");
      const ta = el("textarea", "rzf-text", { rows: "3", maxlength: String(MAX) });
      const count = el("span", "rzf-count", { "aria-hidden": "true" });
      const upd = () => { count.textContent = ta.value.length + " / " + MAX; };
      ta.addEventListener("input", upd); upd();
      repaint.push(() => { const p = lang() === "ms" ? phMs : phEn; ta.placeholder = p; ta.setAttribute("aria-label", p); });
      wrap.append(ta, count); return { wrap, ta, reset() { ta.value = ""; upd(); } };
    }
    function sectionSelect(required) {
      const s = el("select", "rzf-sel");
      repaint.push(() => fillSections(s, required));
      return s;
    }
    function fillSections(s, required) {
      const keep = s.value, L = lang();
      s.textContent = "";
      const first = el("option", null, { value: required ? "" : "general" });
      first.textContent = required ? (L === "ms" ? "Pilih bahagian…" : "Choose a section…") : (L === "ms" ? "Umum / tidak pasti" : "General / not sure");
      s.append(first);
      if (required) { const g = el("option", null, { value: "general" }); g.textContent = L === "ms" ? "Umum / tidak pasti" : "General / not sure"; s.append(g); }
      const groups = {};
      for (const sec of sections) {
        const v = sec.view || "other";
        if (!groups[v]) { groups[v] = el("optgroup"); groups[v].label = VIEW[v] ? VIEW[v][L === "ms" ? 1 : 0] : v; s.append(groups[v]); }
        const o = el("option", null, { value: sec.id });
        o.textContent = (L === "ms" ? sec.title_ms : sec.title_en) || sec.title_en || sec.id;
        groups[v].append(o);
      }
      s.value = keep && [...s.options].some((o) => o.value === keep) ? keep : s.options[0].value;
    }
    function button(en, ms, cls) { const b = el("button", "rzf-btn" + (cls ? " " + cls : ""), { type: "button" }); b.append(bi(en, ms)); return b; }

    async function post(body) {
      if (!live) throw Object.assign(new Error("offline"), { code: "offline" });
      const r = await fetch(endpoint + "?app=" + encodeURIComponent(cfg.app), {
        method: "POST", headers: { "Content-Type": "text/plain;charset=UTF-8" },
        body: JSON.stringify(Object.assign({ part: cfg.part, session: st.session, lang: lang() }, body)),
      });
      if (r.status === 429) throw Object.assign(new Error("capped"), { code: "capped" });
      if (!r.ok) throw Object.assign(new Error("failed"), { code: "failed" });
      return r.json();
    }
    function fail(s, e) {
      if (e && e.code === "capped") say(s, "Thank you, that is plenty for now. Please try again later.", "Terima kasih, itu sudah memadai buat masa ini. Sila cuba lagi kemudian.", "warn");
      else if (e && e.code === "offline") say(s, "Not connected to the course server.", "Tidak disambungkan ke pelayan kursus.", "warn");
      else say(s, "It could not be sent. Please try again.", "Tidak dapat dihantar. Sila cuba lagi.", "warn");
    }
    const controls = [];                      // disabled while offline

    // 1. rate this part
    const rate = card("Rate this part", "Nilai bahagian ini", "rzf-rate");
    const stars = el("div", "rzf-stars", { role: "radiogroup" });
    repaint.push(() => stars.setAttribute("aria-label", lang() === "ms" ? "Nilai 1 hingga 5" : "Rating 1 to 5"));
    let score = mine.score || 0;
    const starBtns = STARS.map((lab, i) => {
      const b = el("button", "rzf-star", { type: "button", role: "radio", "aria-checked": "false", "data-score": String(i + 1) });
      b.textContent = "★";
      repaint.push(() => { const t = (i + 1) + " – " + lab[lang() === "ms" ? 1 : 0]; b.title = t; b.setAttribute("aria-label", t); });
      b.addEventListener("click", () => { score = i + 1; paintStars(); });
      controls.push(b); stars.append(b); return b;
    });
    const starLab = el("span", "rzf-starlab");
    function paintStars() {
      starBtns.forEach((b, i) => { b.classList.toggle("on", i < score); b.setAttribute("aria-checked", String(i + 1 === score)); b.tabIndex = (score ? i + 1 === score : i === 0) ? 0 : -1; });
      starLab.textContent = ""; if (score) starLab.append(bi(STARS[score - 1][0], STARS[score - 1][1]));
    }
    stars.addEventListener("keydown", (e) => {
      const d = e.key === "ArrowRight" || e.key === "ArrowUp" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -1 : 0;
      if (!d) return; e.preventDefault(); score = Math.min(5, Math.max(1, (score || 0) + d)); paintStars(); starBtns[score - 1].focus();
    });
    const starRow = el("div", "rzf-row"); starRow.append(stars, starLab); rate.append(starRow);
    const picked = new Set(mine.chips || []);
    function chipRow(en, ms, list, prefix) {
      const lab = bi(en, ms, "p"); lab.className = "rzf-lab"; rate.append(lab);
      const row = el("div", "rzf-chips");
      for (const [id, cen, cms] of list) {
        const v = prefix + id, b = el("button", "rzf-chip", { type: "button", "aria-pressed": String(picked.has(v)) });
        b.append(bi(cen, cms));
        b.addEventListener("click", () => { picked.has(v) ? picked.delete(v) : picked.add(v); b.setAttribute("aria-pressed", String(picked.has(v))); });
        controls.push(b); row.append(b);
      }
      rate.append(row);
    }
    chipRow("What helped you most?", "Apa yang paling membantu anda?", CHIPS.helped, "h:");
    chipRow("What would help more?", "Apa yang akan lebih membantu?", CHIPS.wish, "w:");
    const comment = textarea("Anything else? (optional)", "Ada apa-apa lagi? (pilihan)");
    rate.append(comment.wrap); controls.push(comment.ta);
    const rateBtn = button("Send rating", "Hantar penilaian", "rzf-primary"); controls.push(rateBtn);
    const rateS = status(rate);
    const rateRow = el("div", "rzf-row"); rateRow.append(rateBtn); rate.insertBefore(rateRow, rateS);
    rateBtn.addEventListener("click", async () => {
      if (!score) { say(rateS, "Choose 1 to 5 stars first.", "Pilih 1 hingga 5 bintang dahulu.", "warn"); return; }
      rateBtn.disabled = true;
      try {
        await post({ kind: "rate", score, chips: [...picked], text: comment.ta.value });
        mine.score = score; mine.chips = [...picked]; save(); comment.reset();
        say(rateS, "Thank you! Your rating is saved; you can change it at any time.", "Terima kasih! Penilaian anda disimpan; anda boleh mengubahnya bila-bila masa.", "ok");
        loadSummary();
      } catch (e) { fail(rateS, e); }
      rateBtn.disabled = !live;
    });
    if (mine.score) say(rateS, "You rated this part before. Send again to change it.", "Anda pernah menilai bahagian ini. Hantar semula untuk mengubahnya.");

    // 2. muddiest point
    const mud = card("Muddiest point", "Perkara paling mengelirukan", "rzf-muddy");
    const mudLab = bi("What is still unclear after studying this part?", "Apa yang masih kurang jelas selepas mempelajari bahagian ini?", "p"); mudLab.className = "rzf-lab"; mud.append(mudLab);
    const mudSel = sectionSelect(false); controls.push(mudSel);
    repaint.push(() => mudSel.setAttribute("aria-label", lang() === "ms" ? "Bahagian (pilihan)" : "Section (optional)"));
    const mudT = textarea("e.g. why the influence line for moment is a triangle", "cth. kenapa influence line untuk moment berbentuk segi tiga");
    controls.push(mudT.ta);
    const mudBtn = button("Send", "Hantar", "rzf-primary"); controls.push(mudBtn);
    mud.append(mudSel, mudT.wrap); const mudRow = el("div", "rzf-row"); mudRow.append(mudBtn); mud.append(mudRow);
    const mudS = status(mud);
    mudBtn.addEventListener("click", async () => {
      if (mudT.ta.value.trim().length < 3) { say(mudS, "Write a few words first.", "Tulis beberapa perkataan dahulu.", "warn"); return; }
      mudBtn.disabled = true;
      try {
        await post({ kind: "muddy", text: mudT.ta.value, section: mudSel.value === "general" ? "" : mudSel.value });
        mudT.reset();
        say(mudS, "Thank you. The lecturer reads these to decide what to explain better.", "Terima kasih. Pensyarah membaca semua ini untuk menentukan apa yang perlu diterangkan dengan lebih baik.", "ok");
      } catch (e) { fail(mudS, e); }
      mudBtn.disabled = !live;
    });

    // 3. report a mistake
    const mis = card("Report a mistake", "Lapor kesilapan", "rzf-mistake");
    const misLab = bi("Found a typo, a wrong sign or a broken button? Say where.", "Jumpa salah taip, tanda yang salah atau butang yang rosak? Nyatakan di mana.", "p"); misLab.className = "rzf-lab"; mis.append(misLab);
    const misSel = sectionSelect(true); controls.push(misSel);
    repaint.push(() => misSel.setAttribute("aria-label", lang() === "ms" ? "Bahagian" : "Section"));
    const misT = textarea("What is wrong, and what should it be?", "Apa yang salah, dan sepatutnya bagaimana?");
    controls.push(misT.ta);
    const misBtn = button("Report", "Lapor", "rzf-primary"); controls.push(misBtn);
    mis.append(misSel, misT.wrap); const misRow = el("div", "rzf-row"); misRow.append(misBtn); mis.append(misRow);
    const misS = status(mis);
    misBtn.addEventListener("click", async () => {
      if (!misSel.value) { say(misS, "Choose the section first.", "Pilih bahagian dahulu.", "warn"); return; }
      if (misT.ta.value.trim().length < 3) { say(misS, "Describe the mistake first.", "Terangkan kesilapan itu dahulu.", "warn"); return; }
      misBtn.disabled = true;
      try {
        await post({ kind: "mistake", text: misT.ta.value, section: misSel.value });
        misT.reset();
        say(misS, "Thank you for spotting it. It will be checked and fixed.", "Terima kasih kerana perasan. Ia akan disemak dan dibetulkan.", "ok");
      } catch (e) { fail(misS, e); }
      misBtn.disabled = !live;
    });

    // 4. like, with the public counts (the Worker withholds them below its minimum)
    const like = card("Like this page", "Suka halaman ini", "rzf-like");
    const likeBtn = el("button", "rzf-likebtn", { type: "button", "aria-pressed": String(!!mine.liked) });
    likeBtn.append(el("span", "rzf-heart", { "aria-hidden": "true" }), bi("I find this page useful", "Halaman ini berguna untuk saya"));
    likeBtn.firstChild.textContent = "👍";
    controls.push(likeBtn);
    const counts = el("p", "rzf-counts");
    const likeS = status(like);
    like.insertBefore(likeBtn, likeS); like.insertBefore(counts, likeS);
    likeBtn.addEventListener("click", async () => {
      const want = !mine.liked;
      likeBtn.disabled = true;
      try { await post({ kind: "like", value: want }); mine.liked = want; save(); likeBtn.setAttribute("aria-pressed", String(want)); say(likeS, ""); loadSummary(); }
      catch (e) { fail(likeS, e); }
      likeBtn.disabled = !live;
    });
    async function loadSummary() {
      if (!live) return;
      try {
        const r = await fetch(endpoint + "/summary?app=" + encodeURIComponent(cfg.app) + "&part=" + encodeURIComponent(cfg.part));
        if (!r.ok) return;
        const s = await r.json();
        counts.textContent = "";
        if (s.likes != null) counts.append(bi(s.likes + " students find this page useful.", s.likes + " pelajar mendapati halaman ini berguna.", "span"));
        if (s.rating) { if (s.likes != null) counts.append(document.createTextNode(" ")); counts.append(bi("Mean rating " + s.rating.mean + " / 5 from " + s.rating.n + " ratings.", "Purata penilaian " + s.rating.mean + " / 5 daripada " + s.rating.n + " penilaian.", "span")); }
      } catch (e) { /* counts are optional */ }
    }

    grid.insertBefore(like, mud);             // right after the rating, so the short card sits under it

    // 5. what's new: the lecturer's changes, newest first
    const news = (cfg.whatsNew || []).filter((x) => x && x.date && (x.en || x.ms)).sort((a, b) => String(b.date).localeCompare(String(a.date))).slice(0, 8);
    if (news.length) {
      const wn = card("What's new", "Apa yang baharu", "rzf-news");
      const ul = el("ul", "rzf-newslist");
      for (const x of news) {
        const li = el("li"); const d = el("time", "rzf-date", { datetime: x.date }); d.textContent = x.date;
        li.append(d, bi(x.en || x.ms, x.ms || x.en)); ul.append(li);
      }
      wn.append(ul);
      const thanks = bi("Many of these came from your feedback. Thank you.", "Kebanyakannya datang daripada maklum balas anda. Terima kasih.", "p"); thanks.className = "rzf-lab"; wn.append(thanks);
    }

    // language: re-paint what cannot be a pair of spans
    const paint = () => repaint.forEach((f) => { try { f(); } catch (e) { /* ignore */ } });
    paint(); paintStars();
    new MutationObserver(paint).observe(document.documentElement, { attributes: true, attributeFilter: ["data-lang", "lang"] });

    function setLive(on) {
      live = on;
      offline.hidden = on;
      root.classList.toggle("rzf-off", !on);
      controls.forEach((c) => { c.disabled = !on; });
    }
    setLive(false);

    // sections for "where?": the app's own tutor manifest, when it is there
    if (cfg.manifest !== false) {
      const src = cfg.manifest && typeof cfg.manifest === "object" ? Promise.resolve(cfg.manifest)
        : fetch(cfg.manifest || "tutor/manifest.json").then((r) => (r.ok ? r.json() : { sections: [] }));
      src.then((m) => { sections = (m.sections || []).filter((s) => s && s.id); paint(); }).catch(() => { /* the "General" choice still works */ });
    }
    // is feedback on for this app? (the Worker answers /v1/health?app= with feedback: true|false). Asked only
    // when the tab is first shown, so that reading the other tabs costs the Worker nothing
    function connect() {
      fetch(endpoint.replace(/\/v1\/feedback$/, "/v1/health") + "?app=" + encodeURIComponent(cfg.app))
        .then((r) => (r.ok ? r.json() : {})).then((h) => { if (h && h.feedback) { setLive(true); loadSummary(); } })
        .catch(() => { /* stays offline */ });
    }
    if (endpoint) {
      if ("IntersectionObserver" in window) {
        const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); connect(); } });
        io.observe(root);
      } else connect();
    }
    return { root, endpoint, live: () => live };
  }

  window.RzFeedback = { mount, resolveEndpoint };
})();
