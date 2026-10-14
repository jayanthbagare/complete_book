/* From Problem to Agent — site behaviour (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  var body = document.body;

  /* ---------- theme ---------- */
  function isDark() {
    var t = doc.dataset.theme;
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  var themeBtn = document.querySelector(".theme-btn");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = isDark() ? "light" : "dark";
      doc.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
      renderDiagrams();
    });
  }

  /* ---------- mobile navigation ---------- */
  var menuBtn = document.querySelector(".menu-btn");
  var scrim = document.querySelector(".scrim");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    if (menuBtn) menuBtn.setAttribute("aria-expanded", String(open));
    if (scrim) scrim.hidden = !open;
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setNav(false); });
  var active = document.querySelector(".sidebar a.active");
  if (active) active.scrollIntoView({ block: "center" });

  /* ---------- mermaid ---------- */
  var diagrams = Array.prototype.slice.call(document.querySelectorAll("pre.mermaid"));
  diagrams.forEach(function (el) { el.dataset.src = el.textContent; });
  function renderDiagrams() {
    if (!window.mermaid || !diagrams.length) return;
    diagrams.forEach(function (el) { el.removeAttribute("data-processed"); el.innerHTML = ""; el.textContent = el.dataset.src; });
    window.mermaid.initialize({
      startOnLoad: false,
      theme: isDark() ? "dark" : "neutral",
      securityLevel: "strict",
      flowchart: { htmlLabels: true, useMaxWidth: true, curve: "basis" },
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif"
    });
    window.mermaid.run({ nodes: diagrams }).catch(function (e) { console.error(e); });
  }
  document.addEventListener("DOMContentLoaded", renderDiagrams);
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", function () { if (!doc.dataset.theme) renderDiagrams(); });
  }

  /* ---------- on-this-page scrollspy ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".page-toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[decodeURIComponent(a.getAttribute("href").slice(1))] = a; });
    var heads = Object.keys(byId).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var current = null;
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) current = en.target.id; });
      if (!current) return;
      tocLinks.forEach(function (a) { a.classList.remove("current"); });
      if (byId[current]) byId[current].classList.add("current");
    }, { rootMargin: "-70px 0px -70% 0px" });
    heads.forEach(function (h) { obs.observe(h); });
  }

  /* ---------- search ---------- */
  var input = document.getElementById("search");
  var results = document.getElementById("search-results");
  if (!input || !results) return;
  var sel = -1;

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function terms(q) { return q.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 1; }); }

  function snippet(text, ts) {
    var lower = text.toLowerCase(), at = -1;
    for (var i = 0; i < ts.length && at < 0; i++) at = lower.indexOf(ts[i]);
    var start = Math.max(0, at - 60), s = text.slice(start, start + 180);
    var out = esc(s);
    ts.forEach(function (t) {
      out = out.replace(new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>");
    });
    return (start > 0 ? "…" : "") + out + "…";
  }

  function search(q) {
    var ts = terms(q), idx = window.SEARCH_INDEX || [];
    if (!ts.length) return [];
    var scored = [];
    idx.forEach(function (e) {
      var hay = e.x.toLowerCase(), head = (e.s + " " + e.t).toLowerCase(), score = 0;
      for (var i = 0; i < ts.length; i++) {
        var inBody = hay.indexOf(ts[i]) >= 0, inHead = head.indexOf(ts[i]) >= 0;
        if (!inBody && !inHead) return;
        score += (inHead ? 5 : 0) + (inBody ? 1 : 0);
      }
      if (hay.indexOf(q.toLowerCase()) >= 0) score += 4;
      scored.push({ e: e, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 12).map(function (r) { return { e: r.e, ts: ts }; });
  }

  function show(list, q) {
    sel = -1;
    if (!q.trim()) { results.hidden = true; results.innerHTML = ""; return; }
    results.hidden = false;
    if (!list.length) { results.innerHTML = '<div class="sr-empty">No matches for “' + esc(q) + '”.</div>'; return; }
    results.innerHTML = list.map(function (r) {
      return '<a role="option" href="' + r.e.u + '"><div class="sr-page">' + esc(r.e.t) + "</div>" +
        (r.e.s ? '<div class="sr-head">' + esc(r.e.s) + "</div>" : "") +
        '<div class="sr-snip">' + snippet(r.e.x, r.ts) + "</div></a>";
    }).join("");
  }

  var timer;
  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { show(search(input.value), input.value); }, 80);
  });
  input.addEventListener("keydown", function (e) {
    var items = results.querySelectorAll("a");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!items.length) return;
      e.preventDefault();
      sel = (sel + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      items.forEach(function (a, i) { a.classList.toggle("sel", i === sel); });
      items[sel].scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter") {
      var target = items[sel >= 0 ? sel : 0];
      if (target) { e.preventDefault(); window.location.href = target.getAttribute("href"); }
    } else if (e.key === "Escape") {
      input.value = ""; show([], ""); input.blur();
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== input && !/input|textarea/i.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus();
    }
  });
  document.addEventListener("click", function (e) {
    if (!results.contains(e.target) && e.target !== input) results.hidden = true;
  });
  input.addEventListener("focus", function () { if (input.value.trim()) show(search(input.value), input.value); });
})();
