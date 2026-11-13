(function () {
  var $ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var TRIP = window.TRIP, PL = TRIP.plans, DAYS = TRIP.days, root = document.documentElement;
  var st = { date: TRIP.def, mode: "all", area: "all", plan: null, view: "auto", show: 12, sort: "rank", fstar: 0 };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function vi() { return root.dataset.lang === "vi"; }
  function L(ja, v) { return vi() ? v : ja; }
  var VI = TRIP.vi || {};
  function V(s) { return vi() && s && VI[s] ? VI[s] : s; }
  function tx(p) { return p ? (vi() ? (p[1] || p[0]) : p[0]) : ""; }
  function yen(n) { return (n < 0 ? "−¥" : "¥") + Math.abs(n).toLocaleString("ja-JP"); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var BYID = {}; PL.forEach(function (p) { BYID[p.id] = p; });
  function dlab(k) { return tx(DAYS[k].label); }
  function nextKey(k) { var ks = Object.keys(DAYS).sort(); var i = ks.indexOf(k); return i + 1 < ks.length ? ks[i + 1] : null; }
  function day(p) { return p.days[st.date]; }
  function ok(p) { var d = day(p); return d && typeof d.pp === "number"; }
  function clean(p) { var d = day(p); return ok(p) && (!d.w || d.w.length === 0); }
  function inF(p) { return (st.mode === "all" || p.mode === st.mode) && (st.area === "all" || p.area === st.area) && p.star >= st.fstar; }
  function stars(n) { return "★★★".slice(0, n) + "☆☆☆".slice(0, 3 - n); }
  var MODE = { train: ["新幹線", "Tàu"], bus: ["バス（新宿発）", "Xe buýt"], car: ["車", "Ô tô"] };
  var WARN = { inc: ["一部の料金（2日目のリフトまたはレンタル）が分からず、合計に入っていません", "Thiếu một phần giá"],
    early: ["12/19より前はスキー場がオープン前の可能性（公式で確認を）", "Trước 19/12 có thể chưa mở cửa"],
    nolift: ["リフト代が分からず、合計に入っていません", "Chưa gồm vé cáp treo"] };
  function rankList() {
    var arr = PL.filter(inF);
    arr.sort(function (a, b) {
      var oa = ok(a) ? (clean(a) ? 0 : 1) : 2, ob = ok(b) ? (clean(b) ? 0 : 1) : 2;
      if (oa !== ob) return oa - ob;
      var pa = ok(a) ? day(a).pp : 1e9, pb = ok(b) ? day(b).pp : 1e9;
      if (st.sort === "price") return pa - pb;
      if (st.sort === "comfort") return (b.comfort - a.comfort) || (pa - pb);
      if (st.sort === "rating") return ((b.score || 0) - (a.score || 0)) || (pa - pb);
      if (st.sort === "slope") return (a.slope - b.slope) || (pa - pb);
      if (st.sort === "legs") return (a.legs - b.legs) || (pa - pb);
      if (a.star !== b.star) return b.star - a.star;
      return (ok(a) ? day(a).pp : 1e9) - (ok(b) ? day(b).pp : 1e9);
    });
    return arr;
  }

  // 料金の内訳（トラベルインは部品から組み立てる）
  function rowsOf(p) {
    var d = day(p);
    if (p.src === "extra") return d.rows.map(function (r) { return [L(r[0], r[1]), L(r[2], r[3] || r[2]), r[4]]; });
    var v = p.variants[d.v], a = d.a, R = [];
    R.push([L("ツアー代金 大人（中学生を含む）", "Giá tour NL (gồm THCS)"), yen(a) + " × 3" + L("人", ""), a * 3]);
    R.push([L("ツアー代金 小学生（上限）", "Giá tour trẻ em (tối đa)"), L("こども代金は予約画面で確定するため大人代金で計算 ", "tính bằng giá NL ") + yen(a) + " × 2", a * 2]);
    if (v.om) R.push([L("大宮乗車割引", "Giảm giá Omiya"), L("大人 −", "NL −") + yen(v.om[0]) + " × 3、" + L("こども −", "TE −") + yen(v.om[1]) + " × 2", -(v.om[0] * 3 + v.om[1] * 2)]);
    if (v.l2) R.push([L("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)"), v.l2[1] === 0 ? L("2日券が最初から込み", "đã gồm vé 2 ngày") : L("大人 +", "NL +") + yen(v.l2[1]) + " × 3、" + L("こども +", "TE +") + yen(v.l2c[1]) + " × 2", v.l2[1] * 3 + v.l2c[1] * 2]);
    else R.push([L("2日目のリフト", "Vé ngày 2"), L("ツアーは1日券のみ。2日目は現地で購入（料金未確認・合計に入っていない）", "chưa rõ, chưa gồm"), 0]);
    if (v.rent) R.push([L("レンタル 2日（スキー＋ウェア）", "Thuê đồ 2 ngày"), v.rent[0] === 0 ? L("ツアーに込み", "đã gồm") : L("大人 ", "NL ") + yen(v.rent[0]) + " × 3、" + L("こども ", "TE ") + yen(v.rent[1]) + " × 2", v.rent[0] * 3 + v.rent[1] * 2]);
    else R.push([L("レンタル", "Thuê đồ"), L("外部のレンタル店（料金未確認・合計に入っていない）", "chưa rõ, chưa gồm"), 0]);
    if (v.local) R.push([L("現地の交通（各自負担・往復・上限）", "Đi lại tại chỗ (khứ hồi)"), yen(v.local) + " × 5" + L("人", ""), v.local * 5]);
    R.push(v.mode === "train" ? [L("志木⇔大宮の電車（往復）", "Tàu Shiki ⇔ Omiya"), L("大人¥420・こども¥210 × 往復", "420 / 210 yên × 2"), 3360]
                              : [L("志木⇔新宿の電車（往復・参考）", "Tàu Shiki ⇔ Shinjuku"), L("大人約¥500・こども約¥260 × 往復", "~500 / ~260 yên × 2"), 4040]);
    return R;
  }
  function schoolOf(p) {
    if (p.src === "extra") return p.school ? tx(p.school) : "";
    var v = p.variants[day(p).v]; return v && v.school ? v.school : "";
  }
  function urlOf(p) { return p.src === "extra" ? p.url : p.variants[day(p).v].url; }
  function vname(p) { return p.src === "extra" ? (p.co || "") : (p.variants[day(p).v].name || ""); }

  function cardHTML(p, n) {
    var d = day(p), on = p.id === st.plan;
    var h = '<article class="card' + (on ? " selected" : "") + (ok(p) ? "" : " off") + '" id="card-' + p.id + '" data-plan="' + p.id + '">';
    h += '<div class="card-head"><div class="rank num">' + n + '</div><div><h3>' + esc(V(p.hotel)) + '</h3><div class="badges">';
    if (on) h += '<span class="badge viewing">' + L("表示中", "Đang xem") + "</span>";
    if (p.id === st.cheapest) h += '<span class="badge cheap">' + L("この日の最安", "Rẻ nhất ngày này") + "</span>";
    h += '<span class="badge">' + esc(tx(MODE[p.mode])) + "</span>";
    (p.tags || []).forEach(function (t) { h += '<span class="badge fast">' + esc(L(t[0], t[1])) + "</span>"; });
    h += "</div></div></div>";
    h += '<p class="meta"><span class="stars">' + stars(p.star) + "</span><span>" + esc(V(p.resort)) + "</span>" + (p.rev ? "<span>" + L("楽天 ", "Rakuten ") + p.rev.score + "（" + p.rev.count + L("件", "") + "）</span>" : "<span>" + L("口コミ未確認", "chưa có đánh giá") + "</span>") + "</p>";
    if (!ok(p)) {
      h += '<div class="status">' + esc(dlab(st.date)) + "：" + esc(d.st === "txt" ? tx(d.txt) : L("この日は販売なし", "không bán")) + "</div></article>";
      return h;
    }
    h += '<div class="price-row"><div class="price-big num"><span class="yen">¥</span>' + d.pp.toLocaleString("ja-JP") + '</div><div class="price-unit">' + L("1人あたり・全部込み", "mỗi người, đã gồm tất cả") + "<br>" + L("5人 ", "5 người ") + '<b class="num">' + yen(d.tot) + "</b>・" + esc(dlab(st.date)) + L(" 出発", "") + "</div></div>";
    (d.w || []).forEach(function (w) { h += '<div class="warn-line">※ ' + esc(tx(WARN[w])) + "</div>"; });
    if (d.note) h += '<div class="warn-line">※ ' + esc(tx(d.note)) + "</div>";
    h += '<dl class="kpis"><div><dt>' + L("快適さ", "Thoải mái") + '</dt><dd class="num">' + p.comfort.toFixed(1) + '</dd></div><div><dt>' + L("ゲレンデまで", "Ra dốc") + '</dt><dd>' + esc(V(p.slopel) || L("未確認", "chưa rõ")) + '</dd></div><div><dt>' + L("乗り換え", "Chuyển xe") + '</dt><dd>' + p.legs + L("回", " lần") + '</dd></div></dl>';
    if (p.sub) h += '<p class="sub">' + esc(V(p.sub)) + "</p>";
    var facts = [];
    if (p.icon) p.icon.split("//").forEach(function (x) { if (/禁煙|温泉|露天|初心者|ゲレンデ/.test(x)) facts.push(V(x).replace(/【|】/g, " ")); });
    if (facts.length) h += '<div class="facts2">' + facts.map(function (x) { return "<span>" + esc(x) + "</span>"; }).join("") + "</div>";
    var rows = rowsOf(p).map(function (r) { return "<tr><td>" + esc(r[0]) + "<small>" + esc(r[1]) + "</small></td><td>" + yen(r[2]) + "</td></tr>"; }).join("");
    rows += '<tr class="total"><td>' + L("合計（5人） ／ 1人あたり", "Tổng 5 người / mỗi người") + "</td><td>" + yen(d.tot) + " ／ " + yen(d.pp) + "</td></tr>";
    h += '<div class="bd"><h4>' + L("料金の内訳（5人分・全部込み）", "Chi tiết giá (5 người)") + '</h4><table class="breakdown"><tbody>' + rows + "</tbody></table></div>";
    var sc = schoolOf(p);
    if (sc) h += '<div class="school"><b>' + L("スキースクール", "Trường trượt tuyết") + "</b>" + esc(V(sc)) + (p.schoolsum ? "<br><b class=\"num\">" + L("5人で受けた場合 ", "5 người: ") + esc(tx(p.schoolsum)) + "</b>" : "") + "</div>";
    h += '<div class="btns"><a class="btn" href="' + esc(urlOf(p)) + '" target="_blank" rel="noopener">' + L("このプランを予約", "Đặt gói này") + " <small>" + esc(V(p.src === "extra" ? p.co : "トラベルイン")) + "</small></a>";
    h += '<button class="btn show" type="button" data-show="' + p.id + '">' + L("日程・キャンセル料を見る", "Xem lịch trình & phí hủy") + "</button></div>";
    if (p.src !== "extra") h += '<p class="muted small">' + esc(V(vname(p))) + "</p>";
    return h + "</article>";
  }

  function render() {
    $(".chip").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.date === st.date)); });
    $(".mode").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.mode === st.mode)); });
    $(".area").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.area === st.area)); });
    $(".fstar").forEach(function (b) { b.setAttribute("aria-pressed", String(+b.dataset.star === st.fstar)); });
    $(".sortb").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.sort === st.sort)); });
    $("[data-seldate]").forEach(function (n) { n.textContent = dlab(st.date); });
    var list = rankList();
    var avail = list.filter(ok);
    st.cheapest = null;
    list.filter(clean).forEach(function (p) { if (!st.cheapest || day(p).pp < day(BYID[st.cheapest]).pp) st.cheapest = p.id; });
    if (!st.plan || !BYID[st.plan]) st.plan = avail.length ? avail[0].id : null;
    // おすすめ（この日）
    var top = list.filter(clean)[0];
    var vb = document.getElementById("dayBest");
    if (vb) vb.innerHTML = top ? ('<span class="label">' + L("この日のいちばん上", "Đứng đầu ngày này") + '</span><h3>' + esc(V(top.hotel)) + '</h3><p class="meta"><span class="stars">' + stars(top.star) + "</span><span>" + esc(V(top.resort)) + "</span><span>" + esc(tx(MODE[top.mode])) + '</span></p><div class="price-row"><div class="price-big num"><span class="yen">¥</span>' + day(top).pp.toLocaleString("ja-JP") + '</div><div class="price-unit">' + L("1人あたり・全部込み", "mỗi người") + '</div></div><button class="btn show" type="button" data-show="' + top.id + '">' + L("このプランを見る", "Xem gói này") + "</button>") : "";
    // 棒グラフ（上位10件）
    var bars = avail.slice(0, 10), max = Math.max.apply(null, bars.map(function (p) { return day(p).pp; }).concat([1]));
    document.querySelector(".bars").innerHTML = bars.map(function (p) {
      var d = day(p);
      return '<button class="bar' + (p.id === st.cheapest ? " best" : "") + '" type="button" data-plan="' + p.id + '" aria-pressed="' + (p.id === st.plan) + '"><span class="name"><span class="stars">' + stars(p.star) + "</span> " + esc(V(p.hotel)) + " <small>" + esc(tx(MODE[p.mode])) + '</small></span><span class="val num">' + yen(d.pp) + (d.w && d.w.length ? "※" : "") + '</span><span class="track"><span class="fill" style="display:block;width:' + Math.round(d.pp / max * 100) + '%"></span></span></button>';
    }).join("");
    // カード
    var shown = list.slice(0, st.show);
    if (st.plan && shown.indexOf(BYID[st.plan]) < 0 && list.indexOf(BYID[st.plan]) >= 0) shown.push(BYID[st.plan]);
    document.querySelector(".cards").innerHTML = shown.map(function (p, i) { return cardHTML(p, list.indexOf(p) + 1); }).join("");
    var more = document.getElementById("more-btn");
    more.hidden = st.show >= list.length;
    more.textContent = L("もっと見る（残り" + (list.length - Math.min(st.show, list.length)) + "件）", "Xem thêm (" + (list.length - Math.min(st.show, list.length)) + ")");
    document.getElementById("compare-count").textContent = L("空きあり " + avail.length + "件／" + list.length + "件", avail.length + "/" + list.length + " gói");
    // 一覧表
    document.querySelector("#alltable tbody").innerHTML = list.map(function (p, i) {
      var d = day(p);
      return '<tr data-plan="' + p.id + '" class="' + (ok(p) ? "" : "na") + (p.id === st.plan ? " sel" : "") + '"><td class="num">' + (i + 1) + '</td><td><span class="stars">' + stars(p.star) + "</span></td><td>" + esc(V(p.hotel)) + "<small>" + esc(V(p.resort)) + "</small></td><td>" + esc(tx(MODE[p.mode])) + "</td><td class=\"num r\">" + (ok(p) ? yen(d.pp) + (d.w && d.w.length ? "※" : "") : esc(d.st === "txt" ? tx(d.txt) : L("販売なし", "không bán"))) + "</td></tr>";
    }).join("");
    // 日ごとの最安
    $(".daymin [data-k]").forEach(function (c) { c.classList.toggle("sel", c.dataset.k === st.date); });
    // 日程・キャンセル
    var p = BYID[st.plan];
    $("[data-plan-name]").forEach(function (x) { x.textContent = p ? V(p.hotel) : ""; });
    var sc = document.getElementById("sched"), cc = document.getElementById("cancelbox");
    if (!p || !ok(p)) { sc.innerHTML = '<p class="muted">' + L("選んだ日に販売のあるプランを選んでください。", "Hãy chọn gói có bán ngày này.") + "</p>"; cc.innerHTML = ""; return; }
    var n2 = nextKey(st.date);
    var stp = p.src === "extra" ? p.steps : p.variants[day(p).v].steps;
    var KIND = { train: ["新幹線", "Shinkansen"], bus: ["バス", "Xe buýt"], walk: ["徒歩", "Đi bộ"], local: ["電車", "Tàu điện"], other: ["移動", "Di chuyển"] };
    function tl(list) {
      return '<ol class="route2">' + list.map(function (s) {
        if (s[0] === "leg") return '<li class="lg ' + s[1] + '"><span class="kind">' + esc(tx(KIND[s[1]] || KIND.other)) + "</span><span>" + esc(V(s[2])) + "</span></li>";
        if (s[0] === "note") return '<li class="nt">' + esc(V(s[2])) + "</li>";
        return '<li class="st ' + s[1] + '"><span class="tm num">' + esc(s[3] || "") + '</span><span class="pl">' + (s[1] === "hotel" ? L("泊：", "Nghỉ: ") + esc(V(p.hotel)) : esc(V(s[2]))) + "</span></li>";
      }).join("") + "</ol>";
    }
    sc.innerHTML = '<div class="day"><h3>' + L("1日目 ", "Ngày 1 ") + esc(dlab(st.date)) + "</h3>" + tl(stp.d1) + '<p class="muted">' + L("着いたらすぐ滑れます（荷物は宿やセンターに預ける）。", "Đến nơi là trượt được ngay.") + "</p></div>" +
      '<div class="day"><h3>' + L("2日目 ", "Ngày 2 ") + esc(n2 ? dlab(n2) : "") + "</h3>" + tl(stp.d2) + "</div>" +
      '<p class="muted">' + L("ツアー会社の行程表をもとにしています。時刻はバスツアーのみ決まっていて、新幹線の列車は乗車1か月前に選びます。", "Theo lịch trình của công ty tour.") + "</p>";
    if (p.src === "extra") { cc.innerHTML = p.cancel ? tx(p.cancel) : ""; return; }
    var dd = new Date(2026, 11, +st.date.slice(2)); dd.setDate(dd.getDate() - 21);
    cc.innerHTML = '<div class="deadline">' + L("無料で取り消せるのは ", "Hủy miễn phí đến ") + '<span class="num">' + (vi() ? dd.getDate() + "/" + (dd.getMonth() + 1) : (dd.getMonth() + 1) + "/" + dd.getDate()) + "</span>" + L(" まで（21日前）", "") + "</div>" +
      '<div class="cancel"><h3>' + L("トラベルイン（ツアー全体）", "Travel-inn") + '</h3><div class="steps"><div class="step">' + L("〜21日前", "đến 21 ngày") + '<b>0%</b></div><div class="step mid">' + L("20〜8日前", "20–8 ngày") + '<b>20%</b></div><div class="step mid">' + L("7〜2日前", "7–2 ngày") + '<b>30%</b></div><div class="step hi">' + L("前日・当日", "hôm trước/hôm đi") + "<b>40〜50%</b></div></div><p class=\"muted\">" + L("申込は出発10日前の14時まで。無連絡の不参加は100%。", "Hạn đặt: 14h, 10 ngày trước.") + "</p></div>";
  }

  function setPlan(id, scroll) { st.plan = id; render(); if (scroll) { var t = document.getElementById(scroll); if (t) t.scrollIntoView({ behavior: "smooth", block: "start" }); } }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("button, tr[data-plan]"); if (!b) return;
    if (b.classList.contains("chip")) { st.date = b.dataset.date; render(); }
    else if (b.dataset.k) { st.date = b.dataset.k; render(); }
    else if (b.classList.contains("mode")) { st.mode = b.dataset.mode; st.show = 12; render(); }
    else if (b.classList.contains("area")) { st.area = b.dataset.area; st.show = 12; render(); }
    else if (b.classList.contains("fstar")) { st.fstar = +b.dataset.star; st.show = 12; render(); }
    else if (b.classList.contains("sortb")) { st.sort = b.dataset.sort; render(); }
    else if (b.id === "more-btn") { st.show += 12; render(); }
    else if (b.dataset.show) { if (b.dataset.setdate) st.date = b.dataset.setdate; setPlan(b.dataset.show, "schedule"); }
    else if (b.classList.contains("bar") || b.tagName === "TR") { setPlan(b.dataset.plan, null); var c = document.getElementById("card-" + b.dataset.plan); if (c) c.scrollIntoView({ behavior: "smooth", block: "start" }); }
    else if (b.dataset.lang) { root.dataset.lang = b.dataset.lang; root.lang = b.dataset.lang; $("button[data-lang]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); store("lang", b.dataset.lang); render(); }
    else if (b.dataset.view) { st.view = b.dataset.view; store("view", st.view); applyView(); }
  });
  function applyView() {
    var pc = st.view === "pc" || (st.view === "auto" && window.matchMedia("(min-width: 960px)").matches);
    root.classList.toggle("view-pc", pc); root.classList.toggle("view-sp", st.view === "sp");
    $("button[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.view === st.view)); });
  }
  window.addEventListener("resize", applyView);
  st.schoolSum = TRIP.schoolSum || {};
  var l = load("lang"); if (l === "vi" || l === "ja") { root.dataset.lang = l; root.lang = l; $("button[data-lang]").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.lang === l)); }); }
  var v = load("view"); if (v === "pc" || v === "sp" || v === "auto") st.view = v;
  applyView(); render();
})();
