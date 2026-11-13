# トラベルインの全ツアー＋手作りの候補をまとめ、日ごとの全部込み料金を計算して data.json を作る
import json, os, re, sys, datetime, collections
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import daily
TOURS = json.load(open(os.path.join(S, "tin_all_tours.json")))
DET = json.load(open(os.path.join(S, "tin_detail.json")))
STARS = {}
sp = os.path.join(S, "stars", "result.json")
if os.path.exists(sp): STARS = json.load(open(sp))
DAYS = [daily.key(d) for d in daily.DAYS]
RAIL = {"train": 3360, "bus": 4040}

def star_of(hotel):
    v = STARS.get(hotel)
    if not v or not v.get("score"): return 1, None
    sc, n, on = v["score"], v.get("count") or 0, v.get("onsen")
    if on and sc >= 3.5 and n >= 100: return 3, v
    if sc >= 3.0 and n >= 15: return 2, v
    return 1, v

def resort_of(t):
    a = t["area"].split(" ", 1)
    return a[1] if len(a) > 1 else t["area"]

# 12/19 より前に営業していると確かめたスキー場（それ以外は注意を出す）
EARLY_OK = ["軽井沢", "志賀高原", "焼額", "白馬五竜", "HAKUBA47", "Hakuba47"]

def tin_total(v, a):
    ad_l2 = v["l2"][1] if v["l2"] else 0
    ch_l2 = v["l2c"][1] if v["l2c"] else 0
    om = v["om"] or (0, 0)
    rent = (v["rent"][0] * 3 + v["rent"][1] * 2) if v["rent"] else 0
    return a * 5 - (om[0] * 3 + om[1] * 2) + ad_l2 * 3 + ch_l2 * 2 + rent + v["local"] * 5 + RAIL[v["mode"]]

groups = collections.OrderedDict()
for t in TOURS:
    if not (t["from"].startswith("関東 東京・上野・大宮") or t["from"].startswith("関東 新宿（バス）")): continue
    k = f'{t["tp"]}_{t["c1"]}_{t["c2"]}_{t["c3"]}_{t["br"]}'
    d = DET.get(k)
    if not d: continue
    mode = "train" if t["tp"] == "412" else "bus"
    v = {"id": k, "mode": mode, "name": t["name"], "om": d["omiya"] if mode == "train" else None,
         "l2": d["lift2_ad"], "l2c": d.get("lift2_ch"),
         "rent": None if d["rent_ski"] is None else (d["rent_ski"] + (d["rent_wear"] or 0), (d["rent_jski"] or d["rent_ski"]) + (d["rent_jwear"] or d["rent_wear"] or 0)),
         "local": d["local"], "school": d["school"], "toslope": d["toslope"], "dinner": d["dinner"],
         "url": f'https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp={t["tp"]}&c1={t["c1"]}&c2={t["c2"]}&c3={t["c3"]}&br={t["br"]}',
         "itin": d["itin"]}
    v["incomplete"] = [x for x, bad in (("2日目のリフト代", v["l2"] is None), ("レンタル代", v["rent"] is None)) if bad]
    gk = (t["hotel"], resort_of(t), mode)
    g = groups.setdefault(gk, {"hotel": t["hotel"], "resort": resort_of(t), "pref": t["area"].split(" ")[0], "mode": mode,
                               "icon": t["icon"], "sub": t["sub"], "variants": {}, "prices": {}})
    g["variants"][k] = v
    for dd, a in t["prices"].items():
        g["prices"].setdefault(int(dd), []).append((k, a))

plans = []
for i, (gk, g) in enumerate(groups.items()):
    pid = f"t{i}"
    days = {}
    for d in daily.DAYS:
        cands = g["prices"].get(d.day, [])
        best = None
        for vid, a in cands:
            v = g["variants"][vid]
            tot = tin_total(v, a)
            score = (1 if v["incomplete"] else 0, tot)
            if best is None or score < best[0]: best = (score, vid, a, tot)
        k = daily.key(d)
        if not best: days[k] = {"st": "nosale"}; continue
        _, vid, a, tot = best
        warn = []
        if g["variants"][vid]["incomplete"]: warn.append("inc")
        if d.day < 19 and not any(x in g["resort"] for x in EARLY_OK): warn.append("early")
        days[k] = {"v": vid, "a": a, "tot": tot, "pp": round(tot / 5), "w": warn}
    st, sv = star_of(g["hotel"])
    plans.append({"id": pid, "src": "tin", "hotel": g["hotel"], "resort": g["resort"], "pref": g["pref"], "mode": g["mode"],
                  "area": "niigata" if g["pref"] == "新潟県" else "nagano", "icon": g["icon"], "sub": g["sub"],
                  "star": st, "rev": sv, "variants": g["variants"], "days": days})

# 手作りの候補（ビッグホリデー・自分で手配・車）
import importlib
D2 = daily.build(["p5", "p6", "p9", "p10", "p11"])
EXTRA = {
  "p5": dict(hotel="アーバンヒル石打（ビッグホリデー・レンタル込み）", resort="石打丸山スキー場", pref="新潟県", mode="train", star=1, url="https://www.bigs.jp/tourDetail?tourId=S59164C62401", co="ビッグホリデー"),
  "p6": dict(hotel="ホテルグリーンプラザ上越（ビッグホリデー・ファミリー限定）", resort="上越国際スキー場", pref="新潟県", mode="train", star=3, url="https://www.bigs.jp/tourDetail?tourId=S59164C70701", co="ビッグホリデー"),
  "p9": dict(hotel="NASPAニューオータニ（自分で手配）", resort="GALA湯沢・石打（無料シャトル）", pref="新潟県", mode="train", star=3, url="https://www.jalan.net/yad330823/plan/", co="じゃらん・楽天"),
  "p10": dict(hotel="軽井沢プリンスホテル ウエスト（自分で手配）", resort="軽井沢プリンスホテルスキー場", pref="長野県", mode="train", star=2, url="https://hotel.travel.rakuten.co.jp/hotelinfo/plan/29249", co="楽天"),
  "p11": dict(hotel="軽井沢プリンスホテル ウエスト（レンタカー）", resort="軽井沢プリンスホテルスキー場", pref="長野県", mode="car", star=2, url="https://rent.toyota.co.jp/", co="トヨタレンタカー"),
}
for pid, e in EXTRA.items():
    days = {}
    for k, dd in D2[pid].items():
        if "pp" in dd:
            w = ["nolift"] if dd.get("nolift") else []
            days[k] = {"pp": dd["pp"], "tot": dd["total"], "rows": dd["rows"], "w": w, "note": dd.get("warn")}
        else:
            days[k] = {"st": "txt", "txt": dd["status"]}
    plans.append(dict(e, id=pid, src="extra", area="niigata" if e["pref"] == "新潟県" else "nagano", days=days, rev=None, icon="", sub=""))

# 明らかに高いものを外す：どの日も、その日の最安（完全に計算できたもの）の1.5倍を超えるもの
cheap = {}
for k in DAYS:
    vals = [p["days"][k]["pp"] for p in plans if "pp" in p["days"][k] and not p["days"][k]["w"]]
    cheap[k] = min(vals) if vals else None
kept, dropped = [], []
for p in plans:
    ok_days = [k for k in DAYS if "pp" in p["days"][k] and cheap[k] and p["days"][k]["pp"] <= cheap[k] * 1.5]
    if ok_days: kept.append(p)
    else:
        mins = [p["days"][k]["pp"] for k in DAYS if "pp" in p["days"][k]]
        dropped.append((p["hotel"], p["resort"], p["mode"], min(mins) if mins else None))
json.dump({"plans": kept, "cheap": cheap, "dropped": dropped}, open(os.path.join(S, "data.json"), "w"), ensure_ascii=False)
print("plans", len(plans), "kept", len(kept), "dropped", len(dropped))
print("cheapest by day", cheap)
print(sorted(dropped, key=lambda x: x[3] or 0)[:8])
c = collections.Counter((p["mode"], p["area"]) for p in kept); print(c)
