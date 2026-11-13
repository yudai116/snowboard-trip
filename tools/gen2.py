# -*- coding: utf-8 -*-
# 日付で切り替わる比較ページ（日本語・ベトナム語）を作る
import html, os, sys, json
S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
_src = open(os.path.join(S, "gen.py"), encoding="utf-8").read()
_g = {"__file__": os.path.join(S, "gen.py")}
sys_argv = sys.argv; sys.argv = ["gen.py", "/dev/null"]
exec(_src[:_src.index("exec(open(os.path.join(S,'add_dates.py')")], _g)   # T, plan(), P
exec(_src[_src.index("OTHERS = ["):_src.index("css = open(")], _g)           # OTHERS, EXCL, SRC, NOTES
sys.argv = sys_argv
T = _g["T"]; P = _g["P"]; yen = _g["yen"]
sys.path.insert(0, S)
import daily

# ---------- プランの追加・修正 ----------
_g["plan"](id="p12", mode="car", area="nagano", star=2,
  name=("軽井沢プリンス＋プリンスホテル ウエスト（自家用車＋タイヤレンタル）", "Karuizawa Prince + Prince West (xe nhà + thuê lốp)"),
  date=("", ""), co="アップガレージほか", pp=0, total=0, rentpp=0,
  badges=[("", "車", "Ô tô"), ("", "タイヤだけ借りる", "Chỉ thuê lốp")],
  pros=[("自分の車にスタッドレスだけ借りて付ける。レンタカーより安い", "Thuê lốp mùa đông lắp vào xe nhà – rẻ hơn thuê ô tô"),
        ("軽井沢は高速の出口から近く、雪道が短い", "Karuizawa gần lối ra cao tốc, ít đường tuyết")],
  cons=[("レンタルは2泊3日から。車のタイヤサイズに合う在庫が必要", "Thuê tối thiểu 3 ngày 2 đêm; cần đúng cỡ lốp"),
        ("料金は昨季（25-26）の例。今季は12月開始予定", "Giá mùa trước; mùa này bắt đầu tháng 12"), ("ガソリン代・駐車場は未確認", "Chưa gồm xăng, đỗ xe")],
  rows=[], extra=[], lift=("大人¥7,500〜・小学生まで無料", "NL từ 7.500, TE miễn phí"),
  review=("楽天 4.38（3,019件）", "Rakuten 4,38"),
  url="https://www.upgarage.com/studless-tire-rental/", urlname="アップガレージ",
  url2=("https://www.tiregarden.com/service", "タイヤガーデン"),
  sched=[("1日目", "Ngày 1", [("前日", "タイヤ店でスタッドレスに交換（夏タイヤは預ける）", "Thay lốp ở cửa hàng", True), ("6:00", "志木を出発 → 所沢IC", "Rời Shiki → IC Tokorozawa", False), ("8:30頃", "碓氷軽井沢IC → スキー場・滑走", "Đến khu trượt", False), ("夜", "ホテルで夕食", "Ăn tối", False)]),
         ("2日目", "Ngày 2", [("15:30頃", "スキー場発", "Rời khu trượt", False), ("18:30頃", "志木着。後日タイヤを返却", "Về Shiki; trả lốp sau", True)])],
  cancel=[("タイヤレンタル（アップガレージ）", "Thuê lốp", None, ("Web事前決済。キャンセル規定は申込ページで確認（未確認）", "Thanh toán trước trên web")),
          ("軽井沢プリンスホテル ウエスト", "Prince West", [("〜2日前", "đến 2 ngày", "0%", ""), ("前日", "hôm trước", "20%", "mid"), ("当日", "hôm đi", "80%", "hi"), ("不泊", "không đến", "100%", "hi")], ("", ""))],
  deadline=None, car=True)

FIX = {  # 値段に関わる文言を「全部込み」に合わせて直す
  "p2": dict(badges=[("", "新幹線", "Shinkansen")], pros=[("上越国際は広く、初心者コースが多い。スクール90分¥4,000", "Joetsu Kokusai rộng, nhiều dốc cho người mới; lớp 90 phút 4.000 yên"), ("全室禁煙・レンタル1日700円/点", "Cấm hút thuốc, thuê đồ 700 yên"), ("2日目のリフト追加が安い（大人+¥3,400まで）", "Vé ngày 2 rẻ")]),
  "p3": dict(badges=[("", "バス", "Xe buýt")], pros=[("申込が1回で済む（宿・リフト・往復バス）", "Một lần đặt gồm tất cả"), ("上越国際は初心者コースが多い", "Nhiều dốc cho người mới")],
             cons=[("新宿（都庁の大型バス駐車場）7:10発。志木を6時前後に出る", "Xuất phát 7:10 Shinjuku; rời Shiki ~6 giờ"), ("新幹線版との差は1人¥500前後", "Chỉ rẻ hơn tàu ~500 yên/người"), ("池袋・大宮発のバスは見つからず", "Không có xe từ Ikebukuro/Omiya")]),
  "p4": dict(cons=[("新幹線版との差は1人¥500〜1,500", "Rẻ hơn tàu 500–1.500 yên/người"), ("新宿7:10発・20:50着", "Đi 7:10, về 20:50")]),
  "p7": dict(badges=[("", "新幹線", "Shinkansen"), ("fast", "12/12から滑れる", "Trượt được từ 12/12"), ("", "小学生リフト無料", "Tiểu học miễn phí vé")]),
  "p8": dict(badges=[("", "新幹線", "Shinkansen"), ("", "12/12から滑れる", "Trượt được từ 12/12")]),
  "p6": dict(badges=[("", "新幹線", "Shinkansen"), ("fast", "ゲレンデ0分", "Sát dốc"), ("", "レンタル込み", "Gồm thuê đồ")]),
  "p9": dict(pros=[("口コミ4.42（2,250件）。広い部屋・ビュッフェ（寿司・ローストビーフ）", "Đánh giá 4,42; buffet sushi, bò nướng"), ("源泉かけ流しの大浴場・露天、屋内プール。全室禁煙", "Suối nóng tự nhiên, hồ bơi, cấm hút thuốc"), ("駅から無料送迎、各スキー場へ無料シャトル", "Xe miễn phí từ ga và đến các khu trượt")],
             name=("NASPAニューオータニ泊＋GALA湯沢など（自分で手配）", "NASPA New Otani + GALA Yuzawa (tự đặt)"),
             badges=[("", "新幹線", "Shinkansen"), ("", "宿の評価が高い", "Khách sạn được đánh giá cao")],
             cons=[("NASPAスキーガーデンは昨季12/28オープン。それまでは無料シャトルでGALA湯沢・石打へ", "NASPA Ski Garden mở 28/12 mùa trước; trước đó đi xe sang GALA/Ishiuchi"), ("レンタル・リフトの今季料金が未確認（参考値）", "Giá vé, thuê đồ là tham khảo")]),
  "p10": dict(badges=[("", "新幹線", "Shinkansen"), ("fast", "移動がいちばんラク", "Di chuyển dễ nhất"), ("", "小学生リフト無料", "Tiểu học miễn phí")]),
  "p11": dict(badges=[("", "車", "Ô tô"), ("", "レンタカー", "Thuê ô tô")]),
}
for p in P:
    for k, v in FIX.get(p["id"], {}).items(): p[k] = v
    # 日程の見出しは日付を選ぶと入れ替わる
    p["sched"] = [(("1日目", "Ngày 1") if i == 0 else ("2日目", "Ngày 2")) + (items,) for i, (_, _, items) in enumerate(p["sched"])]
BYID = {p["id"]: p for p in P}
IDS = [p["id"] for p in P]
DATA = daily.build(IDS)
p12rows_base = [("タイヤレンタル（ホイール付き・2泊3日）", "Thuê lốp (kèm mâm, 3 ngày)", "アップガレージ 25-26料金 ¥9,900〜＋脱着工賃¥7,040（車種で変わる）", "9.900 + 7.040 (mùa trước)", 16940),
                ("高速 練馬IC⇔碓氷軽井沢IC（往復・参考）", "Cao tốc (tham khảo)", "普通車¥3,700 × 2", "3.700 × 2", 7400)]
for k, dd in DATA["p11"].items():  # p12 は p11 のレンタカーをタイヤレンタルに置きかえる
    if "rows" in dd:
        rows = [dd["rows"][0]] + p12rows_base + dd["rows"][3:]
        tot = sum(r[4] for r in rows)
        DATA["p12"][k] = dict(dd, rows=rows, total=tot, pp=round(tot / 5))
    else:
        DATA["p12"][k] = dd

SCHOOL = {
  "ishiuchi": ("石打丸山スキー学校（一般クラス・2時間）", "Trường Ishiuchi (lớp chung 2 giờ)", 6000, 6000, "小学生は一般クラスで受講。子ども専用（2時間¥7,500）は12/30から。料金は25-26", "Trẻ học lớp chung; lớp riêng trẻ em từ 30/12"),
  "joetsu": ("上越国際スキースクール（90分）", "Trường Joetsu Kokusai (90 phút)", 4000, 4000, "4歳以上同じ料金（トラベルイン掲載）。現地申込", "Từ 4 tuổi cùng giá"),
  "karuizawa": ("SAJ軽井沢スキー学校（半日）", "Trường SAJ Karuizawa (nửa ngày)", 7000, 7000, "小学生以上同じ料金。12/1から開講。受付9:00〜9:45", "Từ tiểu học cùng giá; mở từ 1/12"),
  "hakuba": ("Hakuba Snowsports School（グループ半日）", "Hakuba Snowsports School (nửa ngày)", 8000, 8000, "大人子ども同額。年度不明の参考値", "Giá tham khảo"),
}
SCH_OF = {"p1": "ishiuchi", "p4": "ishiuchi", "p5": "ishiuchi", "p2": "joetsu", "p3": "joetsu", "p6": "joetsu",
          "p7": "karuizawa", "p10": "karuizawa", "p11": "karuizawa", "p12": "karuizawa", "p8": "hakuba"}
def school_html(pid):
    k = SCH_OF.get(pid)
    if not k:
        return f'<div class="school"><b>{T("スキースクール", "Trường trượt tuyết")}</b>{T("NASPA・GALAのスクールはあるが料金は未確認（NASPA 025-780-6888）", "Có trường nhưng chưa rõ giá")}</div>'

    nj, nv, a, c, mj, mv = SCHOOL[k]; tot = a * 3 + c * 2
    return (f'<div class="school"><b>{T("スキースクール（5人で1回）", "Trường trượt tuyết (5 người, 1 buổi)")}　<span class="num">{yen(tot)}</span></b>'
            f'{T(nj, nv)}<br>{T(f"大人・中学生 ¥{a:,} × 3人 ＋ 小学生 ¥{c:,} × 2人", f"NL ¥{a:,} × 3 + TE ¥{c:,} × 2")}<br><small>{T(mj, mv)}</small></div>')

def stars(n): return "★" * n + "☆" * (3 - n)

def card(p):
    pid = p["id"]
    b = "".join(f'<span class="badge {c}">{T(j, v)}</span>' for c, j, v in p["badges"])
    pc = "".join(f'<p class="pro">{T(j, v)}</p>' for j, v in p["pros"]) + "".join(f'<p class="con">{T(j, v)}</p>' for j, v in p["cons"])
    rev = T(*p["review"]) if p.get("review") else T("楽天で未調査", "chưa kiểm tra")
    btn2 = f'<a class="btn sub" href="{html.escape(p["url2"][0])}" target="_blank" rel="noopener">{T("予約ページ", "Trang đặt")} <small>{p["url2"][1]}</small></a>' if p.get("url2") else ""
    return f'''
      <article class="card" id="card-{pid}" data-mode="{p["mode"]}" data-area="{p["area"]}" data-plan="{pid}" data-star="{p["star"]}">
        <div class="card-head"><div class="rank num">-</div><div>
          <h3>{T(*p["name"])}</h3>
          <div class="badges"><span class="badge viewing" hidden>{T("表示中", "Đang xem")}</span><span class="badge cheap" data-cheap hidden>{T("この日の最安", "Rẻ nhất ngày này")}</span>{b}</div></div></div>
        <p class="meta"><span class="stars" title="{p["star"]}">{stars(p["star"])}</span><span>{rev}</span><span>{p["co"]}</span></p>
        <div class="status" data-status hidden></div>
        <div class="price-row" data-pricerow><div class="price-big num"><span class="yen">¥</span><span data-pp></span></div>
          <div class="price-unit">{T("1人あたり・全部込み", "mỗi người, đã gồm tất cả")}<br>{T("5人", "5 người")} <b class="num" data-total></b>・<span data-date></span></div></div>
        <div class="warn-line" data-warn hidden></div>
        <div class="pc">{pc}</div>
        <div class="bd"><h4>{T("料金の内訳（5人分・全部込み）", "Chi tiết giá (5 người, đã gồm tất cả)")}</h4><table class="breakdown"><tbody data-bd></tbody></table></div>
        {school_html(pid)}
        <div class="btns">
          <a class="btn" href="{html.escape(p["url"])}" target="_blank" rel="noopener">{T("このプランを予約", "Đặt gói này")} <small>{p["urlname"]}</small></a>{btn2}
          <button class="btn show" type="button" data-show="{pid}">{T("日程・キャンセル料を見る", "Xem lịch trình & phí hủy")}</button>
        </div>
      </article>'''

def sched(p):
    out = ""
    for i, (dj, dv, items) in enumerate(p["sched"]):
        li = "".join(f'<li class="{"key" if k else ""}"><span class="t">{t}</span><span class="dot"></span><span class="what">{T(j, v)}</span></li>' for t, j, v, k in items)
        out += f'<div class="day"><h3>{T(dj, dv)} <span data-day="{i}"></span></h3><ol class="timeline">{li}</ol></div>'
    return f'<div class="plan-block" data-plan="{p["id"]}" hidden>{out}<p class="muted">{T("時刻は目安です。新幹線の列車は乗車1か月前に決まります。", "Giờ chỉ là dự kiến.")}</p></div>'

def cancel(p):
    out = ""
    for nj, nv, steps, (mj, mv) in p["cancel"]:
        st = '<div class="steps">' + "".join(f'<div class="step {c}">{T(a, b)}<b>{pct}</b></div>' for a, b, pct, c in steps) + "</div>" if steps else ""
        # 日付つきの期限はスクリプトで入れる
        mj2 = mj if ("まで" not in mj or "日前" in mj and "/" not in mj) else ""
        out += f'<div class="cancel"><h3>{T(nj, nv)}</h3>{st}<p class="muted">{T(mj2, mv if mj2 else "")}</p></div>'
    return f'<div class="plan-block" data-plan="{p["id"]}" hidden><div class="deadline" data-dl></div>{out}</div>'

def bar(p):
    return (f'<button class="bar" type="button" data-mode="{p["mode"]}" data-area="{p["area"]}" data-plan="{p["id"]}" aria-pressed="false">'
            f'<span class="name"><span class="stars">{stars(p["star"])}</span> {T(*p["name"])}</span><span class="val num" data-val></span>'
            f'<span class="track"><span class="fill" style="display:block;width:50%"></span></span></button>')

# ---------- 日付の選択 ----------
WEEKEND = {"1212", "1213", "1219", "1220", "1226", "1227"}
chips = "".join(f'<button class="chip{" we" if k in WEEKEND else ""}" type="button" data-date="{k}" aria-pressed="false"><b class="num">{int(k[2:])}</b><small>{T(daily.WD_JA[d.weekday()], daily.WD_VI[d.weekday()])}</small></button>'
                for d in daily.DAYS for k in [daily.key(d)])

# 日程の一覧表（16日 × プラン）
def cell(pid, k):
    d = DATA[pid][k]
    if "pp" in d: return f'<td data-c="{k}">{d["pp"]:,}{"※" if d.get("nolift") else ""}</td>'
    return f'<td class="na" data-c="{k}">{T(*d["status"])}</td>'
mat_th = "".join(f'<th data-c="{daily.key(d)}" class="{"we" if daily.key(d) in WEEKEND else ""}">{d.month}/{d.day}<br>{T(daily.WD_JA[d.weekday()], daily.WD_VI[d.weekday()])}</th>' for d in daily.DAYS)
mat_rows = "".join(f'<tr><td>{stars(p["star"])} {T(*p["name"])}</td>' + "".join(cell(p["id"], daily.key(d)) for d in daily.DAYS) + "</tr>" for p in P)

GOALS = [
  ("総合", "Tổng thể", "p1", "1219", "石打＋アーバンヒル（新幹線）。ゲレンデ徒歩1分・温泉・鍋食べ放題で、値段も中くらい", "Ishiuchi + Urban Hill: sát dốc, suối nóng, giá vừa phải"),
  ("安さ", "Giá rẻ", "p3", "1223", "上越国際＋ひろみ（新宿発バス）。12/23なら1人¥25,148（全部込み）", "Joetsu + Hiromi (xe buýt): 25.148 yên/người ngày 23/12"),
  ("移動がラク・雪が確実", "Di chuyển dễ, chắc có tuyết", "p10", "1212", "軽井沢プリンス（新幹線約45分・人工雪で営業中・小学生リフト無料）", "Karuizawa: tàu 45 phút, tuyết nhân tạo"),
  ("ご飯", "Bữa ăn", "p9", "1219", "NASPAニューオータニ（ビュッフェ 夕食4.32）", "NASPA New Otani (buffet 4,32)"),
  ("温泉・宿の評価", "Suối nóng & đánh giá", "p9", "1219", "NASPAニューオータニ（楽天4.42・2,250件・源泉かけ流し）", "NASPA New Otani (4,42)"),
]
goals = "".join(f'<div class="goal"><b>{T(a, b)}</b><span>{T(j, v)}</span><button class="link" type="button" data-show="{pid}" data-setdate="{dk}">{T("見る", "Xem")}</button></div>' for a, b, pid, dk, j, v in GOALS)

STARBOX = f'''<div class="starbox">
  <h3>{T("★の意味（宿の確かさ）", "Ý nghĩa của ★")}</h3>
  <div class="srow"><span class="stars">★★★</span><div><b>{T("評判が確かな宿", "Khách sạn được đánh giá tốt, đã kiểm chứng")}</b>{T("天然温泉の大浴場があり、楽天トラベルの口コミが3.5点以上・100件以上", "Có suối nóng tự nhiên; đánh giá Rakuten ≥ 3,5 và ≥ 100 lượt")}</div></div>
  <div class="srow"><span class="stars">★★☆</span><div><b>{T("評判は良い宿", "Khách sạn được đánh giá khá")}</b>{T("口コミが3.0点以上・15件以上。ただし天然温泉かどうか等が確認できていない", "Đánh giá ≥ 3,0 và ≥ 15 lượt; chưa xác nhận suối nóng tự nhiên")}</div></div>
  <div class="srow"><span class="stars">★☆☆</span><div><b>{T("まだ確かめられていない宿", "Chưa kiểm chứng")}</b>{T("ツアー専用のペンション等で口コミを調べられていない。悪い宿という意味ではない", "Chưa xem được đánh giá; không có nghĩa là tệ")}</div></div>
  <p class="muted">{T("口コミはすべて楽天トラベルでそろえています。並び順は ★の多い順 → 同じ★の中は安い順 です。", "Đánh giá đều lấy từ Rakuten Travel. Sắp xếp: nhiều ★ trước, rồi rẻ hơn trước.")}</p>
</div>'''

TIRE = f'''<div class="note"><b>{T("タイヤだけ借りられる？ → 借りられます（2泊3日から）", "Có thể chỉ thuê lốp không? → Có (từ 3 ngày 2 đêm)")}</b>{T(
  "ホイール付きのスタッドレスを店で付け替えてもらい、夏タイヤは預かってもらえます。1泊2日のプランはなく、前日に付けて翌日〜翌々日に返す形です。車のタイヤサイズの在庫が必要なので早めに申し込みを。",
  "Cửa hàng lắp lốp mùa đông (kèm mâm) và giữ lốp cũ. Không có gói 1 đêm. Cần đặt sớm theo cỡ lốp.")}
  <ul class="links">
    <li><a href="https://www.upgarage.com/studless-tire-rental/" target="_blank" rel="noopener">アップガレージ スタッドレスタイヤレンタル</a>：{T("2泊3日 ¥9,900〜＋脱着工賃¥7,040（25-26料金）。今季は12月開始予定・Web事前決済", "3 ngày 9.900 yên + phí lắp 7.040 yên (mùa trước)")}</li>
    <li><a href="https://www.tiregarden.com/service" target="_blank" rel="noopener">タイヤガーデン（セキグチ）レンタルスタッドレス</a>：{T("2泊3日から。2026冬の予約は11/2開始", "Từ 3 ngày; nhận đặt từ 2/11")}</li>
    <li><a href="https://www.kosugi-tire.com/pages_new/rental.php" target="_blank" rel="noopener">小杉タイヤ レンタルスタッドレス</a>：{T("東京・神奈川の店舗。料金表とWeb予約あり", "Cửa hàng ở Tokyo/Kanagawa")}</li>
  </ul></div>'''

V_P = "p1"; V_D = "1219"
vd = DATA[V_P][V_D]
verdict = f'''
  <section class="verdict" id="best">
    <span class="label">{T("いちばんおすすめ", "Đề xuất số 1")}</span>
    <h2>{T(*BYID[V_P]["name"])}</h2>
    <p class="muted">{T("12/19（土）〜20（日）出発がおすすめ（12/20〜24出発も同じ値段）", "Nên đi 19–20/12 (20–24/12 cùng giá)")}</p>
    <div class="price-row"><div class="price-big num"><span class="yen">¥</span>{vd["pp"]:,}</div><div class="price-unit">{T("1人あたり・全部込み", "mỗi người, đã gồm tất cả")}<br>{T("5人", "5 người")} {yen(vd["total"])}</div></div>
    <ul class="reasons">
      <li>{T("交通（志木から）・宿2食・リフト2日・レンタル2日の全部込みで、この金額", "Đã gồm đi lại từ Shiki, 2 bữa, vé 2 ngày, thuê đồ 2 ngày")}</li>
      <li>{T("ゲレンデまで徒歩1分・温泉・全室禁煙・鍋食べ放題", "Ra dốc 1 phút, suối nóng, cấm hút thuốc, lẩu ăn thoải mái")}</li>
      <li>{T("大宮から約1時間。スクールは一般クラス2時間（5人で¥30,000）", "Từ Omiya ~1 giờ; lớp học 2 giờ (5 người 30.000 yên)")}</li>
    </ul>
    <div class="deadline">{T("予約するなら", "Nên đặt trước")} <span class="num">11/28</span> {T("まで（無料キャンセル期限・21日前）", "(hạn hủy miễn phí)")}</div>
    <div class="btns"><a class="btn" href="{html.escape(BYID[V_P]["url"])}" target="_blank" rel="noopener">{T("予約する", "Đặt ngay")} <small>トラベルイン</small></a>
      <button class="btn show" type="button" data-show="{V_P}" data-setdate="{V_D}">{T("この日程・キャンセル料を見る", "Xem lịch trình & phí hủy")}</button></div>
  </section>'''

others = _g["others"]; excl = _g["excl"]; src = _g["src"]; notes = _g["notes"]

css = open(os.path.join(S, "tpl_css.html"), encoding="utf-8").read()
css = css.replace('family=Barlow+Condensed', 'family=Noto+Sans:wght@400;700;900&family=Barlow+Condensed')
css = css.replace("<title>スノボ旅行 湯沢 12/20</title>", '<meta charset="utf-8">\n<title>スキー旅行 家族5人 12月</title>\n<meta name="robots" content="noindex,nofollow">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
css = css.replace("</style>", open(os.path.join(S, "extra.css"), encoding="utf-8").read() + "\n</style>", 1)
js = open(os.path.join(S, "page.js"), encoding="utf-8").read()

body = f'''
<div class="wrap">
  <header class="hero-band">
    <div class="topbar">
      <div class="seg" role="group" aria-label="表示"><button type="button" data-view="auto" aria-pressed="true">{T("自動", "Tự động")}</button><button type="button" data-view="sp" aria-pressed="false">{T("スマホ", "Điện thoại")}</button><button type="button" data-view="pc" aria-pressed="false">PC</button></div>
      <div class="seg langs" role="group" aria-label="Language"><button type="button" data-lang="ja" aria-pressed="true">日本語</button><button type="button" data-lang="vi" aria-pressed="false">Tiếng Việt</button></div>
    </div>
    <div class="hero-main">
      <div class="eyebrow">SKI TRIP</div>
      <h1>{T("家族5人 スキー旅行 1泊2日", "Chuyến trượt tuyết gia đình 5 người, 2 ngày 1 đêm")}</h1>
      <div class="trip-meta">
        <span>{T("出発日 12/12〜12/27", "Ngày đi 12/12 – 27/12")}</span>
        <span>{T("大人2・中学生1・小5・小3", "2 người lớn, 1 THCS, lớp 5, lớp 3")}</span>
        <span>{T("全員スキー初心者・フルレンタル", "Tất cả mới tập, thuê đồ đầy đủ")}</span>
        <span>{T("志木発（新幹線は大宮・バスは新宿）", "Từ Shiki (tàu từ Omiya, xe buýt từ Shinjuku)")}</span>
        <span>{T("2026/11/13 調査", "Khảo sát 13/11/2026")}</span>
      </div>
      <div class="mode-label">{T("出発日を選ぶ（1泊2日）", "Chọn ngày đi (2 ngày 1 đêm)")}</div>
      <div class="chips" role="group">{chips}</div>
      <div class="filters">
        <div><div class="mode-label">{T("交通手段", "Phương tiện")}</div>
          <div class="modes" role="group"><button class="mode" type="button" data-mode="all" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="mode" type="button" data-mode="train" aria-pressed="false">{T("新幹線", "Tàu")}</button><button class="mode" type="button" data-mode="bus" aria-pressed="false">{T("バス", "Xe buýt")}</button><button class="mode" type="button" data-mode="car" aria-pressed="false">{T("車", "Ô tô")}</button></div></div>
        <div><div class="mode-label">{T("エリア", "Khu vực")}</div>
          <div class="areas" role="group"><button class="area" type="button" data-area="all" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="area" type="button" data-area="niigata" aria-pressed="false">{T("新潟", "Niigata")}</button><button class="area" type="button" data-area="nagano" aria-pressed="false">{T("長野", "Nagano")}</button></div></div>
      </div>
    </div>
    <svg class="ridge" viewBox="0 0 400 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0 44 L0 30 L40 18 L70 26 L120 6 L160 22 L200 12 L250 28 L300 4 L340 20 L370 14 L400 24 L400 44 Z"/></svg>
  </header>
  <div class="toprow">{verdict}
  <section id="goals"><h2>{T("目的別の総評", "Gợi ý theo mục đích")}</h2><div class="goals">{goals}</div>{STARBOX}</section></div>
  <nav class="toc" aria-label="目次">
    <a href="#best">{T("結論", "Kết luận")}</a><a href="#compare">{T("候補", "Các gói")}</a><a href="#dates">{T("日程の一覧", "Bảng ngày")}</a><a href="#school">{T("スクール", "Trường")}</a>
    <a href="#schedule">{T("日程", "Lịch trình")}</a><a href="#cancel">{T("キャンセル料", "Phí hủy")}</a><a href="#notes">{T("注意", "Lưu ý")}</a><a href="#more">{T("詳細", "Chi tiết")}</a>
  </nav>
  <section id="compare">
    <h2>{T("候補を比べる", "So sánh các gói")} <small><span data-seldate></span> {T("出発", "khởi hành")}・<span id="compare-count"></span></small></h2>
    <p class="muted">{T("金額はすべて「志木からの電車＋新幹線・バス・車＋宿2食＋リフト2日＋レンタル2日」の合計を5人で割った1人あたり。ツアーの小学生は大人料金で数えた上限（実際はもっと安い）。スクール代は別に表示。", "Giá = tàu từ Shiki + tàu/xe + khách sạn 2 bữa + vé 2 ngày + thuê đồ 2 ngày, chia 5. Trẻ em tính như người lớn (tối đa). Phí học ghi riêng.")}</p>
    <div class="bars" aria-label="1人あたりの費用">{"".join(bar(p) for p in P)}</div>
    <p class="muted" data-unavail></p>
    <div class="cards">{"".join(card(p) for p in P)}</div>
    <div class="more"><details><summary>{T("そのほかの候補（概要）", "Các lựa chọn khác")}</summary><ul>{others}</ul></details></div>
  </section>
  <section id="dates">
    <h2>{T("日程の一覧（1人あたり・全部込み）", "Bảng giá theo ngày (mỗi người)")}</h2>
    <p class="muted">{T("列の日付をタップすると、その日に切り替わります。土日は色付き。「販売なし」はツアーの設定がない日、「オープン前」はスキー場が開いていない見込みの日、「未調査」は宿の料金を調べていない日。※はリフト代が入っていない金額。", "Chạm vào ngày để chuyển. ※ = chưa gồm vé.")}</p>
    <div class="tablewrap"><table class="cmp mat"><tr><th>{T("プラン", "Gói")}</th>{mat_th}</tr>{mat_rows}</table></div>
    <div class="note"><b>{T("日程の結論：12/19〜24出発が値段と雪のバランスが良い", "Kết luận: đi 19–24/12 cân bằng nhất")}</b>{T(
      "新潟のスキー場は多くが12/18〜19オープン予定で、それより前は長野（軽井沢・白馬）だけ。12/19〜24出発は同じ値段（平日にしても安くならない。バスだけ1人¥1,000安い日あり）。12/25（金）から年末料金で、12/26・27は1人¥5,000〜15,000高くなり、人気の宿は満室。平日は子どもが学校を休む必要があります（埼玉の公立校の終業式は12/24ごろ）。",
      "Niigata mở cửa 18–19/12. Đi 19–24/12 cùng giá. Từ 25/12 là giá cuối năm, đắt hơn 5.000–15.000 yên/người.")}</div>
  </section>
  <section id="school"><h2>{T("スキースクール（5人で受けた場合）", "Trường trượt tuyết (5 người)")}</h2>
    <div class="tablewrap"><table class="cmp sch"><tr><th>{T("スキー場", "Khu trượt")}</th><th>{T("大人・中学生", "NL/THCS")}</th><th>{T("小学生", "Tiểu học")}</th><th>{T("5人の合計", "Tổng 5 người")}</th><th>{T("今回の日程", "Ngày đi")}</th></tr>
      <tr><td>軽井沢プリンス（半日）</td><td>¥7,000 × 3</td><td>¥7,000 × 2</td><td>¥35,000</td><td>{T("全日程OK（12/1〜）", "OK")}</td></tr>
      <tr><td>石打丸山（一般2時間）</td><td>¥6,000 × 3</td><td>¥6,000 × 2</td><td>¥30,000</td><td>{T("子ども専用は12/30から", "Lớp trẻ em từ 30/12")}</td></tr>
      <tr><td>上越国際（90分）</td><td>¥4,000 × 3</td><td>¥4,000 × 2</td><td>¥20,000</td><td>{T("12/19〜（開業後）", "từ 19/12")}</td></tr>
      <tr><td>白馬五竜（グループ半日）</td><td>¥8,000 × 3</td><td>¥8,000 × 2</td><td>¥40,000</td><td>{T("年度不明の参考値", "tham khảo")}</td></tr>
      <tr><td>志賀高原 焼額山（家族プライベート2時間）</td><td colspan="2">{T("5人まとめて", "cả 5 người")}</td><td>¥20,500</td><td>{T("予約制", "cần đặt")}</td></tr>
      <tr><td>NASPA・GALA・苗場・舞子・野沢</td><td colspan="2">{T("スクールはあるが料金未確認", "chưa rõ giá")}</td><td>-</td><td>-</td></tr>
    </table></div>
    <p class="muted">{T("全員初心者なら、初日の午前にグループレッスンを受けるのがおすすめ。スクール代は現地払いが多く、上の金額には入っていません。石打・軽井沢は昨季（25-26）やツアー会社掲載の料金です。", "Người mới nên học buổi sáng ngày đầu. Phí học chưa gồm trong giá trên.")}</p>
  </section>
  <section id="schedule"><h2>{T("日程", "Lịch trình")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b>・<span data-seldate></span></div>{"".join(sched(p) for p in P)}</section>
  <section id="cancel"><h2>{T("キャンセル料", "Phí hủy")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b>・<span data-seldate></span></div>{"".join(cancel(p) for p in P)}</section>
  <section id="notes"><h2>{T("注意", "Lưu ý")}</h2><div class="notes">{TIRE}{notes}</div></section>
  <section id="more"><h2>{T("詳細", "Chi tiết")}</h2>
    <div class="more">
      <details><summary>{T("除外した候補と理由", "Các gói bị loại")}</summary><ul>{excl}</ul></details>
      <details><summary>{T("調べきれなかったこと", "Chưa xác nhận được")}</summary><ul>
        <li>ツアーの小学生のこども代金（予約画面に進まないと出ない）。ビッグホリデーのキャンセル料とリフト券の扱い</li>
        <li>志木周辺のレンタカーのスタッドレス料金・在庫、正確な高速代、ガソリン代・駐車場代</li>
        <li>NASPA・石打・上越国際・GALAの今季のオープン日とリフト・レンタル料金（昨季の値や参考値を使用）</li>
        <li>志木からの電車賃は2026年10月の運賃改定前の値（駅探）。大宮〜軽井沢の新幹線は改定前の参考額</li>
        <li>NASPA・軽井沢ウエストは一部の日の料金のみ調査（「未調査」の日）</li>
      </ul></details>
      <details><summary>{T("出典URL", "Nguồn")}</summary><ul>{src}<li><a href="https://ekitan.com/transit/fare/sf-2225/st-1728" target="_blank" rel="noopener">志木〜大宮の運賃（駅探）</a></li><li><a href="https://niigata-kankou.or.jp/ski/detail_10688.html" target="_blank" rel="noopener">NASPAスキーガーデン（25-26料金）</a></li><li><a href="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=3021&c3=004001&br=5G" target="_blank" rel="noopener">上越国際スクール・レンタル（トラベルイン）</a></li><li><a href="https://www.princehotels.co.jp/ski/karuizawa/winter/school/" target="_blank" rel="noopener">軽井沢プリンス スクール</a></li><li><a href="https://www.upgarage.com/studless-tire-rental/" target="_blank" rel="noopener">アップガレージ タイヤレンタル</a></li></ul></details>
      <p class="muted">{T("調査量（合計）：約80サイト・検索とページ取得など約400回", "Khối lượng khảo sát: ~80 trang, ~400 lượt")}</p>
    </div>
  </section>
  <footer>{T("料金は2026/11/13時点のものです。予約前に各サイトで確認してください。", "Giá tại thời điểm 13/11/2026.")}</footer>
</div>
<script>window.TRIP = {json.dumps({"data": DATA, "def": "1219"}, ensure_ascii=False)};</script>
'''
page = "<!doctype html>\n<html lang=\"ja\" data-lang=\"ja\">\n<head>\n" + css + "\n</head>\n<body>" + body + "<script>\n" + js + "\n</script>\n</body>\n</html>\n"
open(OUT, "w", encoding="utf-8").write(page)
print("written", OUT, len(page))
