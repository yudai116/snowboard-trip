(function () {
  var $ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var D = window.TRIP.data;
  var root = document.documentElement;
  var st = { date: window.TRIP.def, mode: "all", area: "all", plan: "p1", view: "auto" };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lang() { return root.dataset.lang || "ja"; }
  function tx(pair) { return pair ? (lang() === "vi" ? (pair[1] || pair[0]) : pair[0]) : ""; }
  function yen(n) { return (n < 0 ? "−¥" : "¥") + Math.abs(n).toLocaleString("ja-JP"); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function day(pid) { return D[pid][st.date]; }
  function ok(pid) { return day(pid) && typeof day(pid).pp === "number"; }
  function inFilter(el) { return (st.mode === "all" || el.dataset.mode === st.mode) && (st.area === "all" || el.dataset.area === st.area); }
  function nextLabel(k) { var keys = Object.keys(D.p1).sort(); var i = keys.indexOf(k); return i >= 0 && i + 1 < keys.length ? D.p1[keys[i + 1]].label : null; }
  function dateLabel(k) { return tx(D.p1[k].label); }

  function applyView() {
    var pc = st.view === "pc" || (st.view === "auto" && window.matchMedia("(min-width: 960px)").matches);
    root.classList.toggle("view-pc", pc);
    root.classList.toggle("view-sp", st.view === "sp");
    $("[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.view === st.view)); });
  }

  function renderCard(c) {
    var pid = c.dataset.plan, d = day(pid);
    var good = ok(pid);
    c.classList.toggle("off", !good);
    c.querySelector("[data-pricerow]").hidden = !good;
    var s = c.querySelector("[data-status]");
    s.hidden = good; s.textContent = good ? "" : dateLabel(st.date) + "：" + tx(d.status) + (d.note ? "（" + tx(d.note) + "）" : "");
    var w = c.querySelector("[data-warn]");
    w.hidden = !(good && d.warn); w.textContent = good && d.warn ? "※ " + tx(d.warn) : "";
    if (!good) { c.querySelector("[data-bd]").innerHTML = ""; return; }
    c.querySelector("[data-pp]").textContent = d.pp.toLocaleString("ja-JP");
    c.querySelector("[data-total]").textContent = yen(d.total);
    c.querySelector("[data-date]").textContent = dateLabel(st.date) + (lang() === "vi" ? " khởi hành" : " 出発");
    var rows = d.rows.map(function (r) {
      return "<tr><td>" + esc(lang() === "vi" ? r[1] : r[0]) + "<small>" + esc(lang() === "vi" ? (r[3] || r[2]) : r[2]) + "</small></td><td>" + yen(r[4]) + "</td></tr>";
    }).join("");
    rows += '<tr class="total"><td>' + (lang() === "vi" ? "Tổng 5 người / mỗi người" : "合計（5人） ／ 1人あたり") + "</td><td>" + yen(d.total) + " ／ " + yen(d.pp) + "</td></tr>";
    c.querySelector("[data-bd]").innerHTML = rows;
  }

  function render() {
    $(".chip").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.date === st.date)); });
    $(".mode").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.mode === st.mode)); });
    $(".area").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.area === st.area)); });
    $("[data-seldate]").forEach(function (n) { n.textContent = dateLabel(st.date); });

    var cards = $(".card");
    cards.forEach(renderCard);
    // 並べ替え：販売あり → ★の多い順 → 安い順
    cards.sort(function (a, b) {
      var oa = ok(a.dataset.plan), ob = ok(b.dataset.plan);
      if (oa !== ob) return oa ? -1 : 1;
      var sa = +a.dataset.star, sb = +b.dataset.star;
      if (sa !== sb) return sb - sa;
      return (oa ? day(a.dataset.plan).pp : 0) - (ob ? day(b.dataset.plan).pp : 0);
    });
    var box = document.querySelector(".cards");
    var shown = 0, n = 0, cheapest = null;
    cards.forEach(function (c) {
      box.appendChild(c);
      c.hidden = !inFilter(c);
      if (!c.hidden) { shown++; c.querySelector(".rank").textContent = String(++n); }
      var pid = c.dataset.plan;
      if (!c.hidden && ok(pid) && !day(pid).nolift && (!cheapest || day(pid).pp < day(cheapest).pp)) cheapest = pid;
    });
    cards.forEach(function (c) {
      c.querySelector("[data-cheap]").hidden = c.dataset.plan !== cheapest;
      var on = c.dataset.plan === st.plan; c.classList.toggle("selected", on);
      c.querySelector(".badge.viewing").hidden = !on;
    });
    var cnt = document.getElementById("compare-count");
    var avail = cards.filter(function (c) { return !c.hidden && ok(c.dataset.plan); }).length;
    if (cnt) cnt.textContent = lang() === "vi" ? avail + "/" + shown + " gói" : "空きあり " + avail + "件／" + shown + "件";

    // 棒グラフ
    var bars = $(".bar"), bbox = document.querySelector(".bars");
    var order = cards.map(function (c) { return c.dataset.plan; });
    bars.sort(function (a, b) { return order.indexOf(a.dataset.plan) - order.indexOf(b.dataset.plan); });
    var vis = bars.filter(function (b) { bbox.appendChild(b); b.hidden = !inFilter(b) || !ok(b.dataset.plan); return !b.hidden; });
    var max = Math.max.apply(null, vis.map(function (b) { return day(b.dataset.plan).pp; }).concat([1]));
    var rank = 0;
    vis.forEach(function (b) {
      var d = day(b.dataset.plan);
      b.querySelector("[data-val]").textContent = yen(d.pp) + (d.nolift ? "※" : "");
      b.querySelector(".fill").style.width = Math.round(d.pp / max * 100) + "%";
      b.classList.toggle("best", b.dataset.plan === cheapest);
      b.setAttribute("aria-pressed", String(b.dataset.plan === st.plan));
    });
    var un = cards.filter(function (c) { return !c.hidden && !ok(c.dataset.plan); }).length;
    var u = document.querySelector("[data-unavail]");
    if (u) u.textContent = un ? (lang() === "vi" ? un + " gói không có vào ngày này (xem cuối danh sách)." : "この日に選べないプランが" + un + "件あります（一覧の最後に表示）。※はリフト代が入っていない金額。") : "";

    // 日程・キャンセル
    $(".plan-block").forEach(function (p) { p.hidden = p.dataset.plan !== st.plan; });
    var nm = document.querySelector('.card[data-plan="' + st.plan + '"] h3 .l-' + lang());
    $("[data-plan-name]").forEach(function (x) { x.textContent = nm ? nm.textContent : ""; });
    var d1 = D.p1[st.date].label, d2 = nextLabel(st.date);
    $('[data-day="0"]').forEach(function (x) { x.textContent = tx(d1); });
    $('[data-day="1"]').forEach(function (x) { x.textContent = d2 ? tx(d2) : ""; });
    var sd = day(st.plan);
    $("[data-dl]").forEach(function (x) {
      if (!sd || !sd.deadline) { x.textContent = ok(st.plan) ? "" : dateLabel(st.date) + "：" + tx(sd.status); return; }
      x.innerHTML = (lang() === "vi" ? "Hủy miễn phí đến " : "無料で取り消せるのは ") + '<span class="num">' + esc(tx(sd.deadline)) + "</span>" + (lang() === "vi" ? "" : " まで") + "（" + esc(tx(sd.dlnote)) + "）";
    });

    // 一覧表
    $(".mat [data-c]").forEach(function (x) { x.classList.toggle("sel", x.dataset.c === st.date); });
  }

  function setDate(k) { if (D.p1[k]) { st.date = k; render(); } }
  $(".chip").forEach(function (b) { b.addEventListener("click", function () { setDate(b.dataset.date); }); });
  $(".mat th[data-c]").forEach(function (b) { b.addEventListener("click", function () { setDate(b.dataset.c); }); });
  $(".mode").forEach(function (b) { b.addEventListener("click", function () { st.mode = b.dataset.mode; render(); }); });
  $(".area").forEach(function (b) { b.addEventListener("click", function () { st.area = b.dataset.area; render(); }); });
  $(".bar").forEach(function (b) { b.addEventListener("click", function () {
    st.plan = b.dataset.plan; render();
    var c = document.getElementById("card-" + b.dataset.plan); if (c) c.scrollIntoView({ behavior: "smooth", block: "start" });
  }); });
  $("[data-show]").forEach(function (b) { b.addEventListener("click", function () {
    st.plan = b.dataset.show; if (b.dataset.setdate) st.date = b.dataset.setdate; render();
    var t = document.getElementById("schedule"); if (t) t.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }); });
  function setLang(l) { root.dataset.lang = l; root.lang = l; $("[data-lang]").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.lang === l)); }); store("lang", l); render(); }
  $("button[data-lang]").forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.lang); }); });
  $("button[data-view]").forEach(function (b) { b.addEventListener("click", function () { st.view = b.dataset.view; store("view", st.view); applyView(); }); });
  window.addEventListener("resize", applyView);

  var l = load("lang"); if (l === "vi" || l === "ja") { root.dataset.lang = l; root.lang = l; $("button[data-lang]").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.lang === l)); }); }
  var v = load("view"); if (v === "pc" || v === "sp" || v === "auto") st.view = v;
  applyView();
  render();
})();
