# ---------- 日程別の1人あたり（上限） ----------
DATES = [("12/12", "土", "T7"), ("12/16", "水", "T4"), ("12/19", "土", "T7"), ("12/23", "水", "T4"), ("12/26", "土", "T7")]
NO_SALE = ("販売なし", "không bán")
CLOSED = ("滑れない", "chưa mở")
NO_MEAL = ("2食なし", "không 2 bữa")
FULL = ("満室", "hết phòng")
UNK = ("未確認", "chưa rõ")
# 宿の5人1室2食付きの合計（日付順）。None は下の理由
H_NASPA = {"12/19": 98952, "12/23": 92268, "12/26": FULL}
H_WEST = {"12/12": 164628, "12/16": 145640, "12/23": NO_MEAL, "12/26": FULL}

def tin_train(a, disc=3200): return round((5 * a - disc) / 5)
def bh(a): return round(5 * a * 0.95 / 5)
def naspa(d):
    h = H_NASPA.get(d)
    return h if isinstance(h, tuple) else round((h + 49240 + 30600) / 5)
WEST_LIFT = {"12/12": 7500, "12/16": 7500, "12/23": 9500, "12/26": 11500}
def west(d, car=False):
    h = H_WEST.get(d)
    if isinstance(h, tuple): return h
    base = (36300 + 7400) if car else 42080
    return round((h + base + WEST_LIFT[d] * 3) / 5)

DT = {
  "p1": [NO_SALE, NO_SALE, tin_train(21800), tin_train(21800), tin_train(29900)],
  "p2": [NO_SALE, NO_SALE, tin_train(21200), tin_train(21200), tin_train(28300)],
  "p3": [NO_SALE, NO_SALE, 19900, 18900, 24200],
  "p4": [NO_SALE, NO_SALE, 20500, 19500, 25800],
  "p5": [NO_SALE, NO_SALE, bh(23800), bh(22900), bh(29200)],
  "p6": [NO_SALE, NO_SALE, bh(41900), bh(39400), bh(54300)],
  "p7": [32400, 29800, 34200, 31000, 46100],
  "p8": [32520, 32520, 37920, 35220, 44020],
  "p9": [CLOSED, CLOSED, naspa("12/19"), naspa("12/23"), naspa("12/26")],
  "p10": [west("12/12"), west("12/16"), NO_MEAL, west("12/23"), west("12/26")],
  "p11": [west("12/12", True), west("12/16", True), NO_MEAL, west("12/23", True), west("12/26", True)],
}
MAIN = {"p7": 0, "p8": 0, "p10": 0, "p11": 0}  # それ以外は 12/19（index 2）

def datetable(p):
    vals = DT[p["id"]]
    nums = [v for v in vals if isinstance(v, int)]
    lo = min(nums) if nums else None
    main = MAIN.get(p["id"], 2)
    th = "".join(f'<th>{d}<br>{T(j, v)}</th>' for d, j, v in DATES)
    td = ""
    for i, v in enumerate(vals):
        cls = []
        if i == main: cls.append("main")
        if isinstance(v, int):
            if v == lo: cls.append("best")
            td += f'<td class="{" ".join(cls)}">{v:,}</td>'
        else:
            cls.append("na"); td += f'<td class="{" ".join(cls)}">{T(*v)}</td>'
    return f'<div class="dt"><h4>{T("日程別 1人あたり（上限・円）", "Giá mỗi người theo ngày (yên)")}</h4><table><tr>{th}</tr><tr>{td}</tr></table><p class="muted">{T("青い欄が上の金額の日程。オレンジがいちばん安い日。", "Ô xanh = ngày của giá trên; cam = ngày rẻ nhất.")}</p></div>'

# ---------- スキースクール ----------
SCHOOL_BY_PLAN = {"p1": "ishiuchi", "p4": "ishiuchi", "p5": "ishiuchi", "p2": "joetsu", "p3": "joetsu", "p6": "joetsu",
                  "p7": "karuizawa", "p10": "karuizawa", "p11": "karuizawa", "p8": "hakuba", "p9": "naspa"}
SCHOOLS = {
 "ishiuchi": (("あり（SAJ石打丸山スキー学校など）", "Có (trường SAJ Ishiuchi)"),
   ("小学生以上の一般クラス 2時間¥6,000・4時間¥8,000（当日受付・現地払い）。子ども専用（5歳〜小6）2時間¥7,500は12/30から開講のため、今回の日程では受けられない。料金は25-26の情報。5人で2時間 約¥30,000（子どもが一般クラスに入れれば）",
    "Lớp chung từ tiểu học: 2 giờ 6.000 yên. Lớp riêng trẻ em chỉ từ 30/12. 5 người ~30.000 yên (giá mùa trước)")),
 "joetsu": (("あり（キッズは4歳から）", "Có (trẻ em từ 4 tuổi)"),
   ("料金・12月の開講日は未確認。電話 025-782-1028 で確認", "Chưa rõ giá – gọi 025-782-1028")),
 "naspa": (("あり（ナスパニューオータニ湯沢スキー学校・キッズスクール）", "Có (trường NASPA, lớp trẻ em)"),
   ("グループレッスン（要予約）。料金・開講日は未確認。予約 025-780-6888（10〜16時）", "Lớp nhóm (cần đặt). Chưa rõ giá – 025-780-6888")),
 "karuizawa": (("あり（SAJ軽井沢スキー学校 12/1〜、子ども向けパンダルマン 3〜9歳）", "Có (SAJ Karuizawa từ 1/12; Pandaruman cho trẻ 3–9 tuổi)"),
   ("小学生以上 半日¥7,000・1日¥14,000（現地受付9:00〜9:45／12:30〜13:15）。5人で半日 約¥35,000。パンダルマンは12/18までプライベートのみ（料金未確認）",
    "Từ tiểu học: nửa ngày 7.000, cả ngày 14.000 yên. 5 người nửa ngày ~35.000 yên")),
 "hakuba": (("あり（Hakuba Snowsports School）", "Có (Hakuba Snowsports School)"),
   ("グループ 半日¥8,000・1日¥14,000（大人子ども同額、キッズは5〜12歳）。年度不明の参考値。5人で半日 約¥40,000", "Nhóm: nửa ngày 8.000 yên (tham khảo). 5 người ~40.000 yên")),
}

def schooltable(p):
    k = SCHOOL_BY_PLAN.get(p["id"])
    if not k or k not in SCHOOLS: return ""
    (nj, nv), (bj, bv) = SCHOOLS[k]
    return f'<div class="school"><b>{T("スキースクール：", "Trường trượt tuyết: ")}{T(nj, nv)}</b>{T(bj, bv)}</div>'

SHORT = {"p1": ("石打 アーバンヒル（新幹線）", "Urban Hill (tàu)"), "p2": ("上越国際 ひろみ（新幹線）", "Hiromi (tàu)"),
  "p3": ("上越国際 ひろみ（バス）", "Hiromi (xe buýt)"), "p4": ("石打 アーバンヒル（バス）", "Urban Hill (xe buýt)"),
  "p5": ("石打 アーバンヒル（BH・レンタル込）", "Urban Hill (BH)"), "p6": ("グリーンプラザ上越（BH・レンタル込）", "Green Plaza Joetsu (BH)"),
  "p7": ("軽井沢 ホテル1130（新幹線）", "Karuizawa 1130 (tàu)"), "p8": ("白馬パークホテル（新幹線）", "Hakuba Park (tàu)"),
  "p9": ("NASPAニューオータニ（新幹線）", "NASPA (tàu)"), "p10": ("軽井沢プリンス ウエスト（新幹線）", "Prince West (tàu)"),
  "p11": ("軽井沢プリンス ウエスト（車）", "Prince West (ô tô)")}
DATE_VERDICT = ("結論：12/19（土）〜20（日）がいちばんバランスが良い", "Kết luận: 19–20/12 cân bằng nhất")
DATE_BODY = ("新潟のスキー場は多くが12/18〜19オープンなので、12/12・12/16は長野（軽井沢・白馬など）しか選べません。12/23（水）は12/19とほぼ同じ値段で、バスだけ大人1人¥1,000安くなる程度です。12/26（土）は年末料金で、12/19より大人1人¥5,000〜13,000高くなりますが、雪が増えてコースが多く開いている可能性が高くなります。",
  "Phần lớn khu trượt Niigata mở cửa 18–19/12. Ngày 23/12 (T4) giá gần như 19/12. Ngày 26/12 là giá cuối năm, đắt hơn 5.000–13.000 yên/người lớn, nhưng nhiều tuyết hơn.")
DATE_FOOT = ("平日（12/16・12/23）は子どもが学校を休む必要があります（埼玉の公立校は12/24ごろが終業式）。「販売なし」はツアーの設定がない日、「滑れない」はスキー場がオープン前の日。", "Ngày thường trẻ phải nghỉ học.")

SCHOOL_ALL = [
 ("軽井沢プリンス", "小学生以上 半日¥7,000・1日¥14,000。SAJ軽井沢スキー学校は12/1から開講。子ども向けパンダルマン（3〜9歳）は12/18までプライベートのみ", "全日程OK"),
 ("石打丸山", "一般（小学生以上）2時間¥6,000。子ども専用は12/30から（25-26情報）", "子ども専用は不可"),
 ("白馬五竜＆47", "グループ 半日¥8,000・1日¥14,000（大人子ども同額・年度不明）", "未確認"),
 ("志賀高原 焼額山", "グループは中学生以上のみ2時間¥5,000。家族プライベート（志鷹スクール）5人で2時間¥20,500・4時間¥34,000", "プライベートなら可"),
 ("湯沢中里", "ママミキーキッズ 半日¥8,200〜（年度不明・予約制）", "未確認"),
 ("上越国際・NASPA・苗場・野沢・GALA・舞子", "スクールはあるが今季の料金・開講日は未確認", "未確認"),
]
