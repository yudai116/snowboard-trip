# -*- coding: utf-8 -*-
# 全ツアー版の比較ページ（日本語・ベトナム語）
import html, os, sys, json
S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
sys.path.insert(0, S)
import daily
_src = open(os.path.join(S, "gen.py"), encoding="utf-8").read()
_g = {"__file__": os.path.join(S, "gen.py")}
_argv = sys.argv; sys.argv = ["gen.py", "/dev/null"]
exec(_src[:_src.index("exec(open(os.path.join(S,'add_dates.py')")], _g)
exec(_src[_src.index("OTHERS = ["):_src.index("css = open(")], _g)
sys.argv = _argv
T = _g["T"]; notes = _g["notes"]; src = _g["src"]
DATA = json.load(open(os.path.join(S, "data.json")))
plans = DATA["plans"]

SCHOOLSUM = [("石打", "¥30,000（一般クラス2時間 ¥6,000 × 5人。子ども専用は12/30から）"), ("上越国際", "¥20,000（90分 ¥4,000 × 5人）"),
             ("軽井沢", "¥35,000（半日 ¥7,000 × 5人）"), ("白馬五竜", "¥40,000（半日 ¥8,000 × 5人・参考）"), ("HAKUBA47", "¥40,000（半日 ¥8,000 × 5人・参考）"),
             ("焼額", "¥20,500（家族プライベート2時間）")]
EXTRA_INFO = {
  "p5": dict(co="ビッグホリデー", school=("石打丸山スキー学校 一般クラス2時間¥6,000（25-26）", "Lớp 2 giờ 6.000 yên"),
             itin=("1日目 大宮駅 ## 上越新幹線 ## 越後湯沢駅 == =シャトル約20分 == =石打丸山 2日目 石打丸山 == =シャトル == =越後湯沢駅 ## 上越新幹線 ## 大宮駅", ""),
             cancel=("<p class='muted'>ビッグホリデーのキャンセル料は未確認（予約前に旅行条件書で確認）</p>", "<p class='muted'>Chưa rõ phí hủy</p>")),
  "p6": dict(co="ビッグホリデー", school=("上越国際スキースクール 90分¥4,000（4歳以上）", "90 phút 4.000 yên"),
             itin=("1日目 大宮駅 ## 上越新幹線 ## 越後湯沢駅 == =宿の無料送迎約25分（前日までに予約） == =ホテル 2日目 ホテル == =送迎 == =越後湯沢駅 ## 上越新幹線 ## 大宮駅", ""),
             cancel=("<p class='muted'>ビッグホリデーのキャンセル料は未確認</p>", "<p class='muted'>Chưa rõ phí hủy</p>")),
  "p9": dict(co="じゃらん・楽天", school=("NASPA・GALAのスクール料金は未確認", "chưa rõ"),
             itin=("1日目 大宮駅 ## 上越新幹線 ## 越後湯沢駅 == =無料送迎 == =NASPA == =無料シャトル == =GALA湯沢など 2日目 同じ 越後湯沢駅 ## 上越新幹線 ## 大宮駅", ""),
             cancel=("<p class='muted'>宿：3日前まで無料、2日前・前日20%、当日80%、不泊100%</p>", "")),
  "p10": dict(co="楽天＋えきねっと", school=("SAJ軽井沢スキー学校 半日¥7,000（小学生以上）", "nửa ngày 7.000 yên"),
              itin=("1日目 大宮駅 ## 北陸新幹線 ## 軽井沢駅 == =無料シャトル == =スキー場・ホテル 2日目 スキー場 == =シャトル == =軽井沢駅 ## 北陸新幹線 ## 大宮駅", ""),
              cancel=("<p class='muted'>宿：2日前まで無料、前日20%、当日80%、不泊100%</p>", "")),
  "p11": dict(co="トヨタレンタカー", school=("SAJ軽井沢スキー学校 半日¥7,000（小学生以上）", "nửa ngày 7.000 yên"),
              itin=("1日目 志木周辺で車を借りる == =所沢IC == =関越道・上信越道 == =碓氷軽井沢IC == =スキー場 2日目 スキー場 == =碓氷軽井沢IC == =所沢IC == =返却", ""),
              cancel=("<p class='muted'>宿：2日前まで無料、前日20%、当日80%。レンタカーのキャンセル料は店舗で確認</p>", "")),
}
out = []
for p in plans:
    q = {k: p[k] for k in ("id", "src", "hotel", "resort", "pref", "mode", "area", "star", "rev", "icon", "sub")}
    q["days"] = p["days"]
    q["schoolsum"] = next((v for k, v in SCHOOLSUM if k in p["resort"]), "")
    tags = []
    if "協定" in p["hotel"]: tags.append(["宿はおまかせ（当日まで決まらない）", "Khách sạn do công ty chọn"])
    q["tags"] = tags
    if p["src"] == "tin":
        used = {d["v"] for d in p["days"].values() if "v" in d}
        q["variants"] = {vid: {k: v[k] for k in ("om", "l2", "l2c", "rent", "local", "mode", "school", "url", "name", "itin")} for vid, v in p["variants"].items() if vid in used}
    else:
        q.update(EXTRA_INFO.get(p["id"], {})); q["url"] = p["url"]
    out.append(q)

days = {daily.key(d): {"label": daily.lab(d)} for d in daily.DAYS}
WEEKEND = {"1212", "1213", "1219", "1220", "1226", "1227"}
chips = "".join(f'<button class="chip{" we" if k in WEEKEND else ""}" type="button" data-date="{k}" aria-pressed="false"><b class="num">{int(k[2:])}</b><small>{T(daily.WD_JA[d.weekday()], daily.WD_VI[d.weekday()])}</small></button>'
                for d in daily.DAYS for k in [daily.key(d)])
# 日ごとの最安（完全に計算できて注意のないもの）
def dmin(k):
    v = [(p["days"][k]["pp"], p) for p in plans if "pp" in p["days"][k] and not p["days"][k]["w"]]
    n = sum(1 for p in plans if "pp" in p["days"][k])
    return (min(v, key=lambda x: x[0]) if v else None), n
dm = ""
for d in daily.DAYS:
    k = daily.key(d); best, n = dmin(k)
    dm += (f'<button type="button" class="dcell{" we" if k in WEEKEND else ""}" data-k="{k}"><span>{d.month}/{d.day}<small>{T(daily.WD_JA[d.weekday()], daily.WD_VI[d.weekday()])}</small></span>'
           f'<b class="num">{"¥{:,}".format(best[0]) if best else "-"}</b><small>{n}{T("件", " gói")}</small></button>')

dropped = sorted(DATA["dropped"], key=lambda x: x[3] or 0)
MODEJA = {"train": "新幹線", "bus": "バス", "car": "車"}
drop_html = "".join(f"<li>{html.escape(h)}（{html.escape(r)}・{MODEJA[m]}）：最安 ¥{v:,}/人。どの日もその日の最安の1.5倍を超える</li>" if v else f"<li>{html.escape(h)}：料金なし</li>" for h, r, m, v in dropped)

STARBOX = f'''<div class="starbox">
  <h3>{T("★の意味（宿の確かさ）", "Ý nghĩa của ★")}</h3>
  <div class="srow"><span class="stars">★★★</span><div><b>{T("評判が確かな宿", "Được đánh giá tốt, đã kiểm chứng")}</b>{T("天然温泉の大浴場があり、楽天トラベルの口コミが3.5点以上・100件以上", "Có suối nóng tự nhiên; Rakuten ≥ 3,5 điểm, ≥ 100 lượt")}</div></div>
  <div class="srow"><span class="stars">★★☆</span><div><b>{T("評判は良い宿", "Được đánh giá khá")}</b>{T("口コミが3.0点以上・15件以上。天然温泉が無い、または確認できない", "≥ 3,0 điểm, ≥ 15 lượt")}</div></div>
  <div class="srow"><span class="stars">★☆☆</span><div><b>{T("まだ確かめられていない宿", "Chưa kiểm chứng")}</b>{T("口コミが少ない・見つからない、または宿がおまかせ。悪い宿という意味ではない", "Ít/không có đánh giá; không có nghĩa là tệ")}</div></div>
  <p class="muted">{T("口コミはすべて楽天トラベルでそろえています。", "Đánh giá đều lấy từ Rakuten Travel.")}</p>
</div>'''

TIRE = _g.get("TIRE", "")
TIRE = f'''<div class="note"><b>{T("タイヤだけ借りられる？ → 借りられます（2泊3日から）", "Có thể chỉ thuê lốp? → Có (từ 3 ngày)")}</b>{T("ホイール付きのスタッドレスを店で付け替え、夏タイヤは預かってもらえます。1泊2日のプランはありません。車のタイヤサイズの在庫が必要です。", "Cửa hàng lắp lốp mùa đông và giữ lốp cũ. Cần đặt sớm.")}
  <ul class="links"><li><a href="https://www.upgarage.com/studless-tire-rental/" target="_blank" rel="noopener">アップガレージ スタッドレスタイヤレンタル</a>：2泊3日 ¥9,900〜＋脱着工賃¥7,040（25-26料金）。今季は12月開始予定</li>
  <li><a href="https://www.tiregarden.com/service" target="_blank" rel="noopener">タイヤガーデン（セキグチ）</a>：2泊3日から。2026冬の予約は11/2開始</li>
  <li><a href="https://www.kosugi-tire.com/pages_new/rental.php" target="_blank" rel="noopener">小杉タイヤ</a>：東京・神奈川の店舗</li></ul></div>'''

counts = {"train": sum(1 for p in plans if p["mode"] == "train"), "bus": sum(1 for p in plans if p["mode"] == "bus"), "car": sum(1 for p in plans if p["mode"] == "car")}

car_btn = f'<button class="mode" type="button" data-mode="car" aria-pressed="false">{T("車", "Ô tô")}<small>{counts["car"]}</small></button>' if counts["car"] else ""
body = f'''
<div class="wrap">
  <header class="hero-band">
    <div class="topbar">
      <div class="seg" role="group" aria-label="表示"><button type="button" data-view="auto" aria-pressed="true">{T("自動", "Tự động")}</button><button type="button" data-view="sp" aria-pressed="false">{T("スマホ", "Điện thoại")}</button><button type="button" data-view="pc" aria-pressed="false">PC</button></div>
      <div class="seg" role="group" aria-label="Language"><button type="button" data-lang="ja" aria-pressed="true">日本語</button><button type="button" data-lang="vi" aria-pressed="false">Tiếng Việt</button></div>
    </div>
    <div class="hero-main">
      <div class="eyebrow">SKI TRIP</div>
      <h1>{T("家族5人 スキー旅行 1泊2日", "Chuyến trượt tuyết gia đình 5 người, 2 ngày 1 đêm")}</h1>
      <div class="trip-meta">
        <span>{T("出発日 12/12〜12/27", "Ngày đi 12/12 – 27/12")}</span><span>{T("大人2・中学生1・小5・小3", "2 NL, 1 THCS, lớp 5, lớp 3")}</span>
        <span>{T("全員スキー初心者・フルレンタル", "Mới tập, thuê đồ đầy đủ")}</span><span>{T("志木発（新幹線は大宮・バスは新宿）", "Từ Shiki")}</span>
        <span>{T(f"候補 {len(plans)}件（新潟・長野）", f"{len(plans)} gói")}</span><span>{T("2026/11/13 調査", "Khảo sát 13/11/2026")}</span>
      </div>
      <div class="mode-label">{T("出発日を選ぶ（1泊2日）", "Chọn ngày đi")}</div>
      <div class="chips" role="group">{chips}</div>
      <div class="filters">
        <div><div class="mode-label">{T("交通手段", "Phương tiện")}</div><div class="modes" role="group">
          <button class="mode" type="button" data-mode="all" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="mode" type="button" data-mode="train" aria-pressed="false">{T("新幹線", "Tàu")}<small>{counts["train"]}</small></button><button class="mode" type="button" data-mode="bus" aria-pressed="false">{T("バス", "Xe buýt")}<small>{counts["bus"]}</small></button>{car_btn}</div></div>
        <div><div class="mode-label">{T("エリア", "Khu vực")}</div><div class="areas" role="group">
          <button class="area" type="button" data-area="all" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="area" type="button" data-area="niigata" aria-pressed="false">{T("新潟", "Niigata")}</button><button class="area" type="button" data-area="nagano" aria-pressed="false">{T("長野", "Nagano")}</button></div></div>
        <div><div class="mode-label">{T("宿の★", "Số ★")}</div><div class="areas four" role="group">
          <button class="fstar" type="button" data-star="0" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="fstar" type="button" data-star="2">★★{T("以上", "+")}</button><button class="fstar" type="button" data-star="3">★★★</button></div></div>
      </div>
    </div>
    <svg class="ridge" viewBox="0 0 400 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0 44 L0 30 L40 18 L70 26 L120 6 L160 22 L200 12 L250 28 L300 4 L340 20 L370 14 L400 24 L400 44 Z"/></svg>
  </header>
  <div class="toprow">
    <section class="verdict" id="best"><div id="dayBest"></div>
      <p class="muted">{T("並び順は「★の多い順 → 安い順」。料金が全部分かり、注意がないものが上に来ます。", "Sắp xếp: nhiều ★ trước, rồi rẻ hơn.")}</p></section>
    <section id="goals"><h2>{T("日ごとの最安（1人あたり・全部込み）", "Giá rẻ nhất mỗi ngày")}</h2><div class="daymin">{dm}</div>
      <p class="muted">{T("12/18以前は新潟の多くがオープン前で、確実なのは軽井沢・志賀高原・白馬五竜など。12/19〜25が安く、12/26からは年末料金。平日にしても安くならない日が多い。", "Trước 18/12 nhiều nơi chưa mở. 19–25/12 rẻ; từ 26/12 giá cuối năm.")}</p>{STARBOX}</section>
  </div>
  <nav class="toc" aria-label="目次"><a href="#best">{T("結論", "Kết luận")}</a><a href="#compare">{T("候補", "Các gói")}</a><a href="#all">{T("全件の一覧", "Danh sách")}</a><a href="#school">{T("スクール", "Trường")}</a><a href="#schedule">{T("日程", "Lịch trình")}</a><a href="#cancel">{T("キャンセル料", "Phí hủy")}</a><a href="#notes">{T("注意", "Lưu ý")}</a><a href="#more">{T("詳細", "Chi tiết")}</a></nav>
  <section id="compare">
    <h2>{T("候補を比べる", "So sánh")} <small><span data-seldate></span> {T("出発", "khởi hành")}・<span id="compare-count"></span></small></h2>
    <p class="muted">{T("金額は「志木からの電車＋新幹線・バス・車＋宿2食＋リフト2日＋レンタル2日＋現地の交通」を5人で割った1人あたり。ツアーの小学生は大人料金で数えた上限（実際はもっと安い）。※は一部の料金が分からず合計に入っていないもの。", "Giá mỗi người đã gồm tất cả; trẻ em tính như NL (tối đa). ※ = thiếu một phần.")}</p>
    <div class="sortrow"><span class="muted">{T("並び順：", "Sắp xếp:")}</span><button class="sortb" type="button" data-sort="rank" aria-pressed="true">{T("★→安い順", "★ → giá")}</button><button class="sortb" type="button" data-sort="price" aria-pressed="false">{T("安い順", "Giá")}</button></div>
    <h3 class="sub-h">{T("安い順の上位10件", "10 gói đầu")}</h3>
    <div class="bars"></div>
    <div class="cards"></div>
    <button class="btn more" type="button" id="more-btn">もっと見る</button>
  </section>
  <section id="all"><h2>{T("全件の一覧", "Danh sách tất cả")} <small><span data-seldate></span></small></h2>
    <p class="muted">{T("行をタップするとカードが開きます。", "Chạm vào dòng để mở.")}</p>
    <div class="tablewrap"><table class="cmp" id="alltable"><thead><tr><th>#</th><th>★</th><th>{T("宿・スキー場", "Khách sạn · khu trượt")}</th><th>{T("交通", "Đi lại")}</th><th>{T("1人あたり", "Mỗi người")}</th></tr></thead><tbody></tbody></table></div>
  </section>
  <section id="school"><h2>{T("スキースクール（5人で受けた場合）", "Trường trượt tuyết (5 người)")}</h2>
    <div class="tablewrap"><table class="cmp sch"><tr><th>{T("スキー場", "Khu trượt")}</th><th>{T("大人・中学生", "NL/THCS")}</th><th>{T("小学生", "Tiểu học")}</th><th>{T("5人の合計", "Tổng")}</th><th>{T("今回の日程", "Ngày đi")}</th></tr>
      <tr><td>軽井沢プリンス（半日）</td><td>¥7,000 × 3</td><td>¥7,000 × 2</td><td>¥35,000</td><td>{T("全日程OK（12/1〜）", "OK")}</td></tr>
      <tr><td>石打丸山（一般2時間）</td><td>¥6,000 × 3</td><td>¥6,000 × 2</td><td>¥30,000</td><td>{T("子ども専用は12/30から", "Lớp trẻ em từ 30/12")}</td></tr>
      <tr><td>上越国際（90分）</td><td>¥4,000 × 3</td><td>¥4,000 × 2</td><td>¥20,000</td><td>{T("開業後", "sau khi mở")}</td></tr>
      <tr><td>白馬五竜（グループ半日）</td><td>¥8,000 × 3</td><td>¥8,000 × 2</td><td>¥40,000</td><td>{T("年度不明の参考値", "tham khảo")}</td></tr>
      <tr><td>志賀高原 焼額山（家族プライベート2時間）</td><td colspan="2">{T("5人まとめて", "cả 5 người")}</td><td>¥20,500</td><td>{T("予約制", "cần đặt")}</td></tr>
      <tr><td>{T("そのほかのスキー場", "Khu khác")}</td><td colspan="2">{T("各カードにツアー会社の案内を表示", "xem trong từng gói")}</td><td>-</td><td>-</td></tr></table></div>
    <p class="muted">{T("全員初心者なら、初日の午前にグループレッスンがおすすめ。スクール代は現地払いが多く、上の金額には入っていません。", "Phí học chưa gồm trong giá.")}</p>
  </section>
  <section id="schedule"><h2>{T("日程", "Lịch trình")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b>・<span data-seldate></span></div><div id="sched" class="plan-block"></div></section>
  <section id="cancel"><h2>{T("キャンセル料", "Phí hủy")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b></div><div id="cancelbox" class="plan-block"></div></section>
  <section id="notes"><h2>{T("注意", "Lưu ý")}</h2><div class="notes">{TIRE}{notes}</div></section>
  <section id="more"><h2>{T("詳細", "Chi tiết")}</h2><div class="more">
    <details><summary>{T(f"明らかに高いので外した候補（{len(dropped)}件）", f"Gói bị loại vì quá đắt ({len(dropped)})")}</summary><p class="muted">{T("どの出発日でも、その日の最安の1.5倍を超えるものを外しました。", "Loại các gói đắt hơn 1,5 lần giá rẻ nhất mọi ngày.")}</p><ul>{drop_html}</ul></details>
    <details><summary>{T("そのほか除外した候補", "Loại khác")}</summary><ul>
      <li>新宿・立川・八王子発のJR（中央線）ツアー：新幹線は大宮から、の条件に合わない</li><li>朝食のみ・素泊まり・学生限定のプラン</li><li>車（レンタカー・自家用車＋タイヤレンタル）：雪の少ない軽井沢で計算したが、宿とスキー場のレンタルが高く、どの日も最安の1.5倍を超えた（タイヤレンタルの方法は「注意」に記載）</li>
      <li>ビッグホリデーの他のツアー（朝夕食付きは少なく、料金の内訳が取れない）</li><li>池袋・大宮発のバス：見つからず</li></ul></details>
    <details><summary>{T("調べきれなかったこと", "Chưa xác nhận")}</summary><ul>
      <li>ツアーの小学生のこども代金（予約画面でしか出ない）。そのため金額は上限</li><li>多くのスキー場の今季のオープン日（12/19より前の日は※で注意）</li>
      <li>一部のツアーの2日目のリフト代・外部店のレンタル代（※で表示）</li><li>志木からの電車賃は2026年10月の運賃改定前の値</li><li>レンタカーのスタッドレス料金、ガソリン代・駐車場代</li></ul></details>
    <details><summary>{T("出典URL", "Nguồn")}</summary><ul>{src}<li><a href="https://yoyaku.travel-inn.co.jp/" target="_blank" rel="noopener">トラベルイン（各ツアーの詳細ページ・料金カレンダー）</a></li><li><a href="https://ekitan.com/transit/fare/sf-2225/st-1728" target="_blank" rel="noopener">志木〜大宮の運賃（駅探）</a></li></ul></details>
    <p class="muted">{T("調査量（合計）：約100サイト・検索とページ取得など約1,500回", "~100 trang, ~1.500 lượt")}</p>
  </div></section>
  <footer>{T("料金は2026/11/13時点。予約前に各サイトで確認してください。", "Giá tại 13/11/2026.")}</footer>
</div>
<script>window.TRIP = {json.dumps({"plans": out, "days": days, "def": "1219"}, ensure_ascii=False, separators=(",", ":"))};</script>
'''
css = open(os.path.join(S, "tpl_css.html"), encoding="utf-8").read()
css = css.replace('family=Barlow+Condensed', 'family=Noto+Sans:wght@400;700;900&family=Barlow+Condensed')
css = css.replace("<title>スノボ旅行 湯沢 12/20</title>", '<meta charset="utf-8">\n<title>スキー旅行 家族5人 12月</title>\n<meta name="robots" content="noindex,nofollow">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
css = css.replace("</style>", open(os.path.join(S, "extra.css"), encoding="utf-8").read() + open(os.path.join(S, "extra3.css"), encoding="utf-8").read() + "\n</style>", 1)
js = open(os.path.join(S, "page3.js"), encoding="utf-8").read()
page = "<!doctype html>\n<html lang=\"ja\" data-lang=\"ja\">\n<head>\n" + css + "\n</head>\n<body>" + body + "<script>\n" + js + "\n</script>\n</body>\n</html>\n"
open(OUT, "w", encoding="utf-8").write(page)
print("written", OUT, len(page))
