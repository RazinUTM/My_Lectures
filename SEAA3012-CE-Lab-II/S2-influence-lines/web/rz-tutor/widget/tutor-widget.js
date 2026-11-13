/* SPDX-License-Identifier: MIT
   Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia

   rz tutor widget — the AI chat that sits under the guide panel's speech bubble.
   No dependencies. The host page supplies three callbacks so the widget never touches the
   page's own engine: goto(target) to navigate and spotlight, pose(name) to change the avatar,
   lang() for the current UI language. Everything else (notice gate, class code, transcript,
   quote-mode fallback) is inside.

   window.RzTutor.mount({
     root: '#tutor', endpoint: 'https://rz-tutor.<account>.workers.dev/v1/chat', app: 'seaa4243', part: 'p1',
     manifest: window.TUTOR_MANIFEST,          // optional: {sections:[...]} for offline quote mode and labels
     lang: () => (document.documentElement.lang === 'ms' ? 'ms' : 'en'),
     where: () => ({ view: 'notes', anchor: 'n3' }),
     goto: (t) => {...}, pose: (name) => {...}, onAnswer: (el) => {...},   // onAnswer: typeset math in a rendered answer
     name: 'Dr RJ', storageKey: 'seaa4243-tutor'
   });
*/
(function () {
  "use strict";
  const S = {
    en: {
      notice: "Questions you type here go to an AI service (Anthropic) through the course server. Do not include names, matric numbers or personal details. The tutor can be wrong: check against the notes. Use {name} to understand, not to copy: anything you hand in for marks must be your own work.",
      agree: "Faham · I understand", placeholder: "Ask {name}…", send: "Ask", thinking: "{name} is thinking…",
      goto: "Go to: {label}", copy: "Copy transcript", copied: "Copied.", reset: "New conversation", code: "Class code",
      codeAsk: "Enter the class code given in class to use the AI tutor.", codeSave: "Save", offline: "The tutor server is not reachable. Try these sections:",
      offlineNone: "The tutor server is not reachable. Try the Notes or the Glossary.", limit: "Daily limit reached for the AI tutor.", you: "You", mode: "mode",
      fromNotes: "From the course notes", notInNotes: "Not in the course notes",
      off: "The AI tutor is not switched on yet. These sections match your question:", offNone: "The AI tutor is not switched on yet. Try the Notes or the Glossary.",
    },
    ms: {
      notice: "Soalan yang anda taip di sini dihantar ke perkhidmatan AI (Anthropic) melalui pelayan kursus. Jangan masukkan nama, nombor matrik atau butiran peribadi. Tutor ini boleh tersilap: semak dengan nota. Guna {name} untuk faham, bukan untuk menyalin: apa sahaja yang anda hantar untuk markah mesti hasil kerja anda sendiri.",
      agree: "Faham · I understand", placeholder: "Tanya {name}…", send: "Tanya", thinking: "{name} sedang fikir…",
      goto: "Pergi ke: {label}", copy: "Salin transkrip", copied: "Disalin.", reset: "Perbualan baharu", code: "Kod kelas",
      codeAsk: "Masukkan kod kelas yang diberi dalam kelas untuk guna tutor AI.", codeSave: "Simpan", offline: "Pelayan tutor tidak dapat dihubungi. Sila cuba bahagian ini:",
      offlineNone: "Pelayan tutor tidak dapat dihubungi. Sila cuba Nota atau Glosari.", limit: "Had harian tutor AI sudah dicapai.", you: "Anda", mode: "mod",
      fromNotes: "Daripada nota kursus", notInNotes: "Tiada dalam nota kursus",
      off: "Tutor AI belum dihidupkan lagi. Bahagian ini berkaitan dengan soalan anda:", offNone: "Tutor AI belum dihidupkan lagi. Cuba Nota atau Glosari.",
    },
  };
  const ld = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
  const sv = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage blocked: the widget still works */ } };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const ICON = {
    send: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h12M12 6l6 6-6 6"/></svg>',
    copy: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="11" height="12" rx="2"/><path d="M15 8V6a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h1"/></svg>',
    reset: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3"/><path d="M4.5 4.5v4h4"/></svg>',
  };
  const SOURCED = { cited: 1, verified: 1, rewritten: 1 };
  const sessionId = () => "s_" + Array.from(crypto.getRandomValues(new Uint8Array(12)), (b) => b.toString(16).padStart(2, "0")).join("");

  function mount(cfg) {
    const root = typeof cfg.root === "string" ? document.querySelector(cfg.root) : cfg.root;
    if (!root) return null;
    const key = cfg.storageKey || (cfg.app + "-tutor");
    const st = Object.assign({ agreed: false, session: sessionId(), code: "", turns: [], votes: {} }, ld(key, {}));
    const t = (k, p) => { const L = S[cfg.lang ? cfg.lang() : "en"] || S.en; return (L[k] || S.en[k] || k).replace(/\{(\w+)\}/g, (_, n) => (p && p[n]) != null ? p[n] : (n === "name" ? cfg.name || "the tutor" : "")); };
    const save = () => sv(key, { agreed: st.agreed, session: st.session, code: st.code, turns: st.turns.slice(-12), votes: st.votes });
    const pose = (p) => { if (cfg.pose) try { cfg.pose(p); } catch (e) { /* ignore */ } };
    let busy = false, pending = "";

    root.classList.add("rzt");
    root.innerHTML = "";
    const log = el("div", "rzt-log"); log.setAttribute("aria-live", "polite");
    const status = el("div", "rzt-status");
    const form = el("form", "rzt-form");
    const input = el("input", "rzt-in"); input.type = "text"; input.maxLength = 1000; input.autocomplete = "off";
    const send = el("button", "rzt-send"); send.type = "submit";
    const tools = el("div", "rzt-tools");
    const copyB = el("button", "rzt-tb"); copyB.type = "button";
    const resetB = el("button", "rzt-tb"); resetB.type = "button";
    tools.append(copyB, resetB);
    form.append(input, send);
    root.append(log, status, form, tools);

    function iconBtn(b, icon, label) { b.innerHTML = icon + '<span class="rzt-lbl">' + esc(label) + "</span>"; b.title = label; b.setAttribute("aria-label", label); }
    function paintChrome() {
      input.placeholder = t("placeholder"); input.setAttribute("aria-label", t("placeholder"));
      iconBtn(send, ICON.send, t("send")); iconBtn(copyB, ICON.copy, t("copy")); iconBtn(resetB, ICON.reset, t("reset"));
      if (gateEl && gateEl.isConnected) { gateEl.firstChild.textContent = t("notice"); gateEl.lastChild.textContent = t("agree"); }
    }
    let gateEl = null;
    // the 👍/👎 goes to the lecturer's feedback report as a count (no text, no question) when the page has a Worker
    function sendVote(v) {
      if (!cfg.endpoint || !/\/v1\/chat(\?|$)/.test(cfg.endpoint)) return;
      try {
        fetch(cfg.endpoint.replace(/\/v1\/chat(\?.*)?$/, "/v1/feedback") + "?app=" + encodeURIComponent(cfg.app), {
          method: "POST", headers: { "Content-Type": "text/plain;charset=UTF-8" }, keepalive: true,   // a simple request: no preflight
          body: JSON.stringify({ kind: "tutor_vote", part: cfg.part, session: st.session, value: v }),
        }).catch(() => { /* a lost vote is not worth an error */ });
      } catch (e) { /* ignore */ }
    }
    function gate() {
      if (st.agreed || !cfg.endpoint) return;   // without an endpoint nothing leaves the browser, so there is nothing to agree to
      const g = el("div", "rzt-gate", "<p>" + esc(t("notice")) + "</p>");
      const b = el("button", "rzt-tb rzt-primary", esc(t("agree"))); b.type = "button";
      b.addEventListener("click", () => { st.agreed = true; save(); g.remove(); form.hidden = false; tools.hidden = false; input.focus(); });
      g.append(b); root.insertBefore(g, log); form.hidden = true; tools.hidden = true; gateEl = g;
    }
    function askCode() {
      const g = el("div", "rzt-gate", "<p>" + esc(t("codeAsk")) + "</p>");
      const i = el("input", "rzt-in"); i.type = "text"; i.maxLength = 64; i.placeholder = t("code"); i.autocomplete = "off";
      const b = el("button", "rzt-tb rzt-primary", esc(t("codeSave"))); b.type = "button";
      b.addEventListener("click", () => { st.code = i.value.trim(); save(); g.remove(); const q = pending; pending = ""; if (st.code && q) ask(q); else input.focus(); });
      i.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); b.click(); } });
      g.append(i, b); root.insertBefore(g, form); i.focus();
    }
    function bubble(role, text, out) {
      out = out || {}; const targets = out.targets, mode = out.mode;
      const b = el("div", "rzt-msg rzt-" + role);
      b.append(el("b", null, esc(role === "user" ? t("you") : (cfg.name || "Tutor"))));
      b.append(el("p", null, esc(text)));
      if (targets && targets.length) {
        const row = el("div", "rzt-targets");
        targets.forEach((tg) => {
          const gb = el("button", "rzt-goto", '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg><span>' + esc(t("goto", { label: tg.label })) + "</span>");
          gb.type = "button"; gb.addEventListener("click", () => { pose("present"); if (cfg.goto) cfg.goto(tg); });
          row.append(gb);
        });
        b.append(row);
      }
      if (role === "tutor" && mode) {
        const m = el("div", "rzt-meta");
        if (SOURCED[out.grounding]) m.append(el("span", "rzt-src", esc(t("fromNotes"))));
        else if (out.grounding === "not-covered") m.append(el("span", "rzt-src rzt-nc", esc(t("notInNotes"))));
        const up = el("button", "rzt-vote", "👍"); up.type = "button"; up.setAttribute("aria-label", "helpful");
        const dn = el("button", "rzt-vote", "👎"); dn.type = "button"; dn.setAttribute("aria-label", "not helpful");
        const vote = (v) => { st.votes[v] = (st.votes[v] || 0) + 1; save(); up.disabled = dn.disabled = true; sendVote(v); };
        up.addEventListener("click", () => vote("up")); dn.addEventListener("click", () => vote("down"));
        if (!out.grounding || out.grounding === "fallback") m.append(el("span", "rzt-mode", esc(t("mode") + ": " + mode)));   // why the answer is short
        m.append(up, dn);
        b.append(m);
      }
      log.append(b); log.scrollTop = log.scrollHeight;
      if (role === "tutor" && cfg.onAnswer) { try { cfg.onAnswer(b); } catch (e) { /* ignore */ } }   // e.g. MathJax typesetting of \(…\) in the answer
    }
    function offline(question) {
      const near = nearest(question, cfg.manifest, cfg.lang ? cfg.lang() : "en");
      const off = !cfg.endpoint;   // the AI is switched off on purpose, not unreachable
      return { answer: near.length ? t(off ? "off" : "offline") : t(off ? "offNone" : "offlineNone"), targets: near, mode: "offline", pose: "arms-crossed" };
    }
    async function ask(question) {
      if (busy || !question) return;
      busy = true; send.disabled = true; input.value = "";
      bubble("user", question);
      st.turns.push({ role: "user", content: question }); save();
      status.textContent = t("thinking"); pose("think");
      let out;
      try {
        if (!cfg.endpoint) throw new Error("no endpoint");   // offline mode by design: no request is made
        const r = await fetch(cfg.endpoint + (cfg.endpoint.includes("?") ? "&" : "?") + "app=" + encodeURIComponent(cfg.app), {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ app: cfg.app, part: cfg.part, lang: cfg.lang ? cfg.lang() : "en", session: st.session, code: st.code,
            where: cfg.where ? cfg.where() : {}, messages: st.turns.slice(-12) }),
        });
        if (r.status === 401) { busy = false; send.disabled = false; status.textContent = ""; st.turns.pop(); save(); log.lastChild.remove(); pending = question; askCode(); return; }
        if (!r.ok) throw new Error("http " + r.status);
        out = await r.json();
      } catch (e) {
        out = offline(question);
      }
      st.turns.push({ role: "assistant", content: out.answer }); save();
      bubble("tutor", out.answer, out);
      pose(out.pose || "explain");
      status.textContent = out.mode === "capped" ? t("limit") : "";
      busy = false; send.disabled = false; input.focus();
    }
    form.addEventListener("submit", (e) => { e.preventDefault(); ask(input.value.trim()); });
    copyB.addEventListener("click", () => {
      const text = st.turns.map((m) => (m.role === "user" ? t("you") : (cfg.name || "Tutor")) + ": " + m.content).join("\n\n");
      const done = () => { status.textContent = t("copied"); setTimeout(() => { status.textContent = ""; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, () => {}); else done();
    });
    resetB.addEventListener("click", () => { st.turns = []; st.session = sessionId(); save(); log.innerHTML = ""; status.textContent = ""; pose("welcome"); });

    paintChrome(); gate();
    st.turns.forEach((m) => bubble(m.role === "user" ? "user" : "tutor", m.content));
    return { ask, refresh: paintChrome, reset: () => resetB.click(), state: st };
  }

  const STOP = new Set("the a an of in on at to for and or is are be what how why which do does with from by this that it its apa yang di ke dari dan atau ialah adalah untuk pada dengan bagaimana macam mana kenapa mengapa saya awak ini itu ni tu boleh tak nak ada bila".split(" "));
  function nearest(question, manifest, lang) {
    if (!manifest || !manifest.sections) return [];
    const words = new Set(String(question).toLowerCase().replace(/[^a-z0-9À-ɏ\s-]/g, " ").split(/\s+/).filter((w) => w.length > 2 && !STOP.has(w)));
    const scored = [];
    manifest.sections.forEach((s) => {
      if (s.view === "slides") return;
      const title = (s.title_en + " " + (s.title_ms || "")).toLowerCase();
      let score = 0; words.forEach((w) => { if (title.includes(w)) score += w.length > 5 ? 2 : 1; });
      if (score) scored.push([score, s]);
    });
    scored.sort((a, b) => b[0] - a[0]);
    return scored.slice(0, 2).map(([, s]) => ({ id: s.id, view: s.view, anchor: s.anchor || null, selector: s.selector || null, label: (lang === "ms" ? s.title_ms : s.title_en) || s.title_en }));
  }

  window.RzTutor = { mount, nearest };
})();
