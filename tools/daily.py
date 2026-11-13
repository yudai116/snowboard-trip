# 日ごとの「全部込み」料金（交通＋志木からの電車＋宿2食＋リフト2日＋レンタル2日）を計算する
import json, os, datetime
S = os.path.dirname(os.path.abspath(__file__))
DAYS = [datetime.date(2026, 12, d) for d in range(12, 28)]
WD_JA = "月火水木金土日"; WD_VI = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
def key(d): return d.strftime("%m%d")
def lab(d): return (f"{d.month}/{d.day}（{WD_JA[d.weekday()]}）", f"{d.day}/{d.month} ({WD_VI[d.weekday()]})")
def deadline(d, days):
    x = d - datetime.timedelta(days=days); return (f"{x.month}/{x.day}", f"{x.day}/{x.month}")

TIN = {k: {int(dd): v for dd, v in vals.items()} for k, vals in json.load(open(os.path.join(S, "tin_daily.json"))).items()}
BHC = json.load(open(os.path.join(S, "bh_cal_new.json")))["calendars"]
def bh(tid, d):
    for x in BHC[tid]["priceStocks"]:
        if x["date"] == "2026" + key(d): return x["priceFrom"] if x["priceFrom"] > 0 and x["stock"] != 0 else None
    return None
HD = {}
p = os.path.join(S, "hotel2", "daily", "result.json")
if os.path.exists(p): HD = json.load(open(p))
KNOWN = {"naspa": {"1219": 98952, "1223": 92268, "1226": "満室"}, "west": {"1212": 164628, "1216": 145640, "1219": "2食なし", "1223": "2食なし", "1226": "満室"}}
def hotel(name, d):
    v = HD.get(name, {}).get("2026" + key(d))
    if v is not None: return v[0], (v[1] if len(v) > 1 else "")
    v = KNOWN[name].get(key(d))
    return (v, "") if v is not None else ("未調査", "")

ST = {"未販売": ("販売なし", "không bán"), "満室": ("満室", "hết phòng"), "2食なし": ("2食付きなし", "không có 2 bữa"),
      "未調査": ("未調査", "chưa khảo sát"), "closed": ("オープン前（予定）", "chưa mở cửa"), "full": ("満室", "hết phòng")}

# 共通の小計
OMIYA_RAIL = ("志木⇔大宮の電車（往復）", "Tàu Shiki ⇔ Omiya (khứ hồi)", "朝霞台・北朝霞・武蔵浦和経由 大人¥420・こども¥210 × 往復", "người lớn 420, trẻ em 210 yên × 2 chiều", 3360)
SHINJUKU_RAIL = ("志木⇔新宿の電車（往復・参考）", "Tàu Shiki ⇔ Shinjuku (tham khảo)", "東武東上線＋JR 大人約¥500・こども約¥260 × 往復", "~500 / ~260 yên × 2 chiều", 4040)
RENT700 = ("レンタル 2日（全員）", "Thuê đồ 2 ngày", "スキーセット¥700＋ウェア¥700 × 2日 × 5人（予約時に申込）", "700 + 700 × 2 ngày × 5", 14000)
RENT_PRINCE = ("レンタル 2日（スキー場・Web事前決済）", "Thuê đồ 2 ngày (đặt web)", "大人（中学生含む）セット¥6,500＋ウェア¥4,500 × 3人、小学生 ¥5,500＋¥3,500 × 2人 × 2日", "NL 11.000 × 3, TE 9.000 × 2, × 2 ngày", 102000)

def tin_rows(a, unit_note, disc, lift2, extra_rows):
    rows = [("ツアー代金 大人（中学生を含む）", "Giá tour người lớn (gồm THCS)", f"¥{a:,} × 3人（{unit_note}）", f"{a:,} × 3", a * 3),
            ("ツアー代金 小学生（上限）", "Giá tour trẻ em (tối đa)", f"こども代金は予約画面で確定するため大人代金で計算 ¥{a:,} × 2人", f"tính bằng giá NL {a:,} × 2", a * 2)]
    if disc: rows.append(("大宮乗車割引", "Giảm giá lên tàu ở Omiya", disc[1], disc[2], -disc[0]))
    rows.append(lift2)
    return rows + extra_rows

def west_lift(d):
    def one(x):
        if x <= datetime.date(2026, 12, 18): return 7500
        if datetime.date(2026, 12, 26) <= x <= datetime.date(2026, 12, 28): return 11500
        return 9500
    a, b = one(d), one(d + datetime.timedelta(days=1))
    return ("リフト 2日（大人・中学生）", "Vé 2 ngày (NL, THCS)", f"1日目¥{a:,}＋2日目¥{b:,}（無料会員の窓口料金）× 3人。小学生は無料", f"({a:,} + {b:,}) × 3; tiểu học miễn phí", (a + b) * 3)

def plan_day(pid, d):
    k = key(d); dl21 = deadline(d, 21)
    if pid in ("p1", "p2", "p3", "p4", "p7", "p8"):
        src = {"p1": "p1", "p2": "p2", "p3": "p3", "p4": "p4", "p8": "p8"}.get(pid)
        if pid == "p7":
            c = [TIN["p7a"].get(d.day), TIN["p7b"].get(d.day)]; c = [x for x in c if x]; a = min(c) if c else None
        else:
            a = TIN[src].get(d.day)
        if a is None: return {"status": ST["未販売"]}
        if pid == "p2" and d.day < 19: return {"status": ST["closed"], "note": ("上越国際は12/19オープン予定のため除外", "")}
        if pid == "p1":
            rows = tin_rows(a, "往復新幹線・宿2食・リフト1日券", (3200, "大人 −¥800 × 3、こども −¥400 × 2", "NL −800 × 3, TE −400 × 2"),
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (đổi vé 2 ngày, tối đa)", "大人 +¥5,400 × 3、こども +¥3,000 × 2（日により¥4,100〜）", "NL +5.400 × 3, TE +3.000 × 2", 22200),
                [RENT700, OMIYA_RAIL, ("越後湯沢駅⇔石打", "Echigo-Yuzawa ⇔ Ishiuchi", "スキー場の無料シャトル（約20分）", "xe miễn phí", 0)])
        elif pid == "p2":
            rows = tin_rows(a, "往復新幹線・宿2食・リフト1日券", (3200, "大人 −¥800 × 3、こども −¥400 × 2", "NL −800 × 3, TE −400 × 2"),
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)", "大人 +¥3,400 × 3、こども +¥1,500 × 2", "NL +3.400 × 3, TE +1.500 × 2", 13200), [RENT700, OMIYA_RAIL])
        elif pid == "p3":
            rows = tin_rows(a, "往復バス・宿2食・リフト1日券", None,
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)", "大人 +¥3,400 × 3、こども +¥1,500 × 2", "NL +3.400 × 3, TE +1.500 × 2", 13200), [RENT700, SHINJUKU_RAIL])
        elif pid == "p4":
            rows = tin_rows(a, "往復バス・宿2食・リフト1日券", None,
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)", "大人 +¥5,400 × 3、こども +¥3,000 × 2", "NL +5.400 × 3, TE +3.000 × 2", 22200), [RENT700, SHINJUKU_RAIL])
        elif pid == "p7":
            rows = tin_rows(a, "往復新幹線・宿2食・リフト1日券", None,
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)", "大人 +¥12,000 × 3（日により¥6,000〜）。小学生は無料", "NL +12.000 × 3; tiểu học miễn phí", 36000),
                [RENT_PRINCE, OMIYA_RAIL, ("宿⇔軽井沢駅の送迎", "Xe khách sạn ⇔ ga", "無料（約40分・前日18時までに予約）", "miễn phí, cần đặt", 0)])
        else:  # p8
            rows = tin_rows(a, "往復新幹線・宿2食・リフト1日券", (8400, "大人 −¥2,800 × 3", "NL −2.800 × 3"),
                ("2日目のリフト（2日券に変更・上限）", "Vé ngày 2 (tối đa)", "大人 +¥4,900 × 3、こども +¥1,800 × 2", "NL +4.900 × 3, TE +1.800 × 2", 18300),
                [("長野駅⇔白馬の特急バス（往復・上限）", "Xe buýt Nagano ⇔ Hakuba", "¥3,500 × 2回 × 5人（こども運賃は未確認）", "3.500 × 2 × 5", 35000), RENT700, OMIYA_RAIL])
        return {"rows": rows, "deadline": dl21, "dlnote": ("21日前まで無料キャンセル", "hủy miễn phí đến 21 ngày trước")}
    if pid in ("p5", "p6"):
        tid = "S59164C62401" if pid == "p5" else "S59164C70701"
        a = bh(tid, d)
        if a is None: return {"status": ST["未販売"]}
        rows = [("ツアー代金（5人とも大人代金で上限計算）", "Giá tour (tối đa, tính bằng giá NL)", f"¥{a:,} × 5人", f"{a:,} × 5", a * 5),
                ("LINE友だち追加クーポン", "Phiếu giảm giá LINE", "−5%（誰でも使える）", "−5%", -round(a * 5 * 0.05))]
        if pid == "p5":
            rows += [("リフト券", "Vé cáp treo", "予約画面で「なし／1日券／2日券」を選ぶ。料金はこの合計に入っていない", "chưa gồm trong tổng", 0),
                     ("レンタル", "Thuê đồ", "スキーセット・ウェアが滞在中込み", "đã gồm", 0), OMIYA_RAIL]
            return {"rows": rows, "nolift": True, "warn": ("リフト代が未確認で合計に入っていません", "Chưa gồm vé cáp treo")}
        rows += [("2日目のリフト（参考）", "Vé ngày 2 (tham khảo)", "上越国際の25-26料金 大人¥5,800 × 3、小学生¥3,800 × 2", "NL 5.800 × 3, TE 3.800 × 2", 25000),
                 ("2日目のレンタル（参考）", "Thuê đồ ngày 2 (tham khảo)", "スキーセット¥1,500＋ウェア¥1,000 × 5人（宿のレンタル店）", "(1.500 + 1.000) × 5", 12500), OMIYA_RAIL]
        return {"rows": rows}
    if pid == "p9":
        if d.day < 19: return {"status": ST["closed"], "note": ("GALA湯沢・石打は12/19、NASPAは昨季12/28オープン", "")}
        h, site = hotel("naspa", d)
        if not isinstance(h, int): return {"status": ST.get(h, (h, h))}
        rows = [("宿（2食付き・禁煙・5人1室）", "Khách sạn (2 bữa, 5 người 1 phòng)", f"{site or '楽天/じゃらん'}の最安", "giá rẻ nhất", h),
                ("新幹線 大宮⇔越後湯沢（往復）", "Tàu Omiya ⇔ Echigo-Yuzawa", "指定席eチケット 大人¥6,160 × 3、こども¥3,070 × 2 × 往復", "NL 6.160 × 3, TE 3.070 × 2, × 2", 49240),
                ("リフト 2日（GALA湯沢）", "Vé 2 ngày (GALA)", "Web1日券 大人¥7,500 × 3、小学生¥4,000 × 2（小学生は個人ブログの情報）× 2日", "(7.500 × 3 + 4.000 × 2) × 2", 61000),
                ("レンタル 2日（参考）", "Thuê đồ 2 ngày (tham khảo)", "NASPAの25-26料金 大人 セット¥6,000＋ウェア¥6,000 × 3、子ども ¥5,000＋¥5,000 × 2 × 2日", "tham khảo", 92000),
                ("駅⇔ホテル⇔スキー場", "Xe ga ⇔ KS ⇔ khu trượt", "無料送迎・無料シャトル", "miễn phí", 0), OMIYA_RAIL]
        return {"rows": rows, "deadline": deadline(d, 3), "dlnote": ("宿は3日前まで無料キャンセル", "khách sạn hủy miễn phí đến 3 ngày trước"),
                "warn": ("NASPAスキーガーデンは昨季12/28オープン。それまでは無料シャトルでGALA湯沢・石打へ", "NASPA Ski Garden mở 28/12 mùa trước; trước đó đi xe miễn phí sang GALA/Ishiuchi")}
    if pid in ("p10", "p11"):
        h, site = hotel("west", d)
        if not isinstance(h, int): return {"status": ST.get(h, (h, h))}
        rows = [("宿（2食付き・禁煙・5人1室）", "Khách sạn (2 bữa)", f"{site or '楽天'}の最安", "giá rẻ nhất", h)]
        if pid == "p10":
            rows += [("新幹線 大宮⇔軽井沢（往復・参考）", "Tàu Omiya ⇔ Karuizawa (tham khảo)", "指定席 大人¥5,260 × 3、こども¥2,630 × 2 × 往復（運賃改定前の参考額）", "giá tham khảo", 42080), OMIYA_RAIL]
        else:
            rows += [("レンタカー W2クラス（ミニバン）", "Thuê xe W2 (minivan)", "24時間¥20,900＋次の24時間¥15,400（トヨタ一般料金）。スタッドレス代は未確認", "20.900 + 15.400", 36300),
                     ("高速 練馬IC⇔碓氷軽井沢IC（往復・参考）", "Cao tốc (tham khảo)", "普通車¥3,700 × 2", "3.700 × 2", 7400)]
        rows += [west_lift(d), RENT_PRINCE]
        return {"rows": rows, "deadline": deadline(d, 2), "dlnote": ("宿は2日前まで無料キャンセル", "khách sạn hủy miễn phí đến 2 ngày trước")}
    return {"status": ST["未調査"]}

def build(pids):
    data = {}
    for pid in pids:
        days = {}
        for d in DAYS:
            r = plan_day(pid, d)
            if "rows" in r:
                tot = sum(x[4] for x in r["rows"]); r["total"] = tot; r["pp"] = round(tot / 5)
            r["label"] = lab(d)
            days[key(d)] = r
        data[pid] = days
    return data

if __name__ == "__main__":
    D = build(["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11"])
    for pid, days in D.items():
        print(pid, [days[k].get("pp", days[k].get("status", ["?"])[0]) for k in sorted(days)])
