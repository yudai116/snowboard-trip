# トラベルインの詳細ページ（テキスト）から、全部込みの計算に使う項目を読む
import re, json, os, glob
S = os.path.dirname(os.path.abspath(__file__))
def num(s): return int(s.replace(",", "").replace("，", ""))
def rng(s):  # "￥4,100〜￥5,400" -> (4100, 5400)
    v = [num(x) for x in re.findall(r"￥\s*([\d,]+)", s)]
    return (min(v), max(v)) if v else None

def parse(t):
    r = {}
    m = re.search(r"大宮駅の乗下車は往復でおとな\s*￥([\d,]+)割引\s*、こども\s*￥([\d,]+)割引", t)
    r["omiya"] = (num(m.group(1)), num(m.group(2))) if m else None
    # リフト券メニュー
    lm = re.search(r"リフト券メニュー(.{0,1500}?)(予約へ進む|スキー場メニュー)", t)
    lift = lm.group(1) if lm else ""
    r["lift_text"] = lift[:400]
    m = re.search(r"2日券付\s*旅行代金より\s*おとな(￥[\d,]+(?:〜￥[\d,]+)?)\s*UP(?:・こども(￥[\d,]+(?:〜￥[\d,]+)?)\s*UP)?", lift)
    m2 = re.search(r"2日券付\s*旅行代金より\s*おとな・こどもともに(￥[\d,]+(?:〜￥[\d,]+)?)\s*UP", lift)
    if m2:
        r["lift2_ad"] = rng(m2.group(1)); r["lift2_ch"] = r["lift2_ad"]
    elif re.search(r"リフト(入場)?\s*2日券", lift) or re.search(r"リフト\s*2日券付", lift):
        r["lift2_ad"] = (0, 0); r["lift2_ch"] = (0, 0)
    elif m:
        r["lift2_ad"] = rng(m.group(1)); r["lift2_ch"] = rng(m.group(2)) if m.group(2) else (0, 0)
        if "こどもの割増はございません" in lift: r["lift2_ch"] = (0, 0)
    elif re.search(r"2日券付", lift) and "UP" not in lift:
        r["lift2_ad"] = (0, 0); r["lift2_ch"] = (0, 0)      # 2日券が最初から付いている
    else:
        r["lift2_ad"] = None; r["lift2_ch"] = None
    # スクール（スキー）
    sec = re.search(r"スキー場メニュー(.{0,1500}?)ステイメニュー", t)
    r["school"] = None
    if sec:
        m = re.search(r"(スキースクール|スクール)(.*)", sec.group(1))
        if m and "￥" in m.group(2):
            txt = m.group(1) + m.group(2)
            txt = re.split(r"スクール対応先|開講時間|受付場所|※こども|\s2\.|予約へ進む", txt)[0]
            mm = re.match(r"^(.*(?:現地払い|事前決済|払い|。|ください|ます))", txt.strip(), re.S)
            r["school"] = (mm.group(1) if mm else txt).strip()
    # レンタル：スキーセットとウェア（1日あたり。2日間の設定があればそちら）
    rent = re.search(r"レンタルメニュー クラス(.{0,4000}?)(ゴーグル・|ステイメニュー|旅行条件|行程表)", t)
    rt = rent.group(1) if rent else ""
    def item(label):
        m = re.search(label + r"[^￥無]{0,120}?(1日間：\s*￥([\d,]+)\s*2日間：\s*￥([\d,]+)|￥([\d,]+)|無料)", rt)
        if not m: return None
        if m.group(1) == "無料": return 0
        if m.group(3): return num(m.group(3))
        return num(m.group(4)) * 2
    r["rent_ski"] = item(r"(?<!ジュニア)カービングスキーセット")
    r["rent_wear"] = item(r"(?<!ジュニア)ウエア")
    r["rent_jski"] = item(r"ジュニアカービングスキーセット") or r["rent_ski"]
    r["rent_jwear"] = item(r"ジュニアウエア") or r["rent_wear"]
    r["rent_onsite"] = "現地払い" in rt[:600] or "現地申込" in rt[:600]
    # 行程表：各自負担（最初の経路だけ）
    im = re.search(r"行程表 日程 行程表 食事(.*?)(行程表をご確認の上|旅行代金：おとな1名様あたり（税込）・お申し込み)", t)
    it = im.group(1) if im else ""
    loc = 0; parts = re.split(r"2日目", it, maxsplit=1)
    for p in parts:
        p = re.split(r"\(2\)", p)[0]
        loc += sum(num(x) for x in re.findall(r"各自負担￥([\d,]+)", p))
    r["local"] = loc
    r["itin"] = it
    g = re.search(r"(ゲレンデ|スキー場)まで：?([^ ]{1,30})", t)
    r["toslope"] = g.group(2) if g else None
    m = re.search(r"夕食：「([^」]{1,40})」", t); r["dinner"] = m.group(1) if m else None
    return r

out = {}
for f in glob.glob(os.path.join(S, "tind2t", "*.txt")):
    k = os.path.basename(f)[:-4]
    out[k] = parse(open(f, encoding="utf-8").read())
json.dump(out, open(os.path.join(S, "tin_detail.json"), "w"), ensure_ascii=False, indent=0)
import collections
print(len(out), "lift2 None:", sum(1 for v in out.values() if v["lift2_ad"] is None), "rent None:", sum(1 for v in out.values() if v["rent_ski"] is None),
      "omiya:", sum(1 for v in out.values() if v["omiya"]), "local>0:", sum(1 for v in out.values() if v["local"]))
