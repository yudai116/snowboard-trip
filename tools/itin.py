# ツアー会社の行程表の文章を、駅・乗り物・宿の段に分ける
import re

def _clean(s):
    s = re.sub(r"朝\s*[×〇○]\s*昼\s*[×〇○]\s*夕\s*[×〇○].*$", "", s)
    s = re.sub(r"＜記号＞.*$", "", s)
    s = re.sub(r"[^。\s]*≫", "", s)
    s = re.sub(r"\(2\).*?(?=(到着後|【宿泊】|チェックアウト|\S+駅\s*##))", "", s)   # 2つめの経路は省く
    s = s.replace("(1)", "")
    s = re.sub(r"※?\d+/\d+現在", "", s)
    return s

def leg_kind(t):
    if "新幹線" in t: return "train"
    if re.search(r"バス|シャトル|送迎|タクシー", t): return "bus"
    if "徒歩" in t: return "walk"
    return "other"

def steps(text):
    text = _clean(text)
    parts = re.split(r"\s*(?:##\s*)+|\s*==\s*=\s*|…", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p: continue
        if re.search(r"山手線|東京23区|^上野駅|^東京駅|上野駅）|東京駅\)|^\(上野駅|^各地発シャトルバス", p): continue
        if p[0] in "(（":
            t = p.strip("()（） ")
            t = re.sub(r"※\d", "", t)
            out.append(["leg", leg_kind(t), t.strip()])
            continue
        # 宿・フリータイム・注意書きを分ける
        hm = re.search(r"【宿泊】", p)
        notes = re.findall(r"※[^※]{2,80}", p)
        main = re.split(r"※", p)[0].strip()
        main = re.sub(r"【宿泊】.*$", "", main).strip()
        tm = re.search(r"(\d{1,2})[：:](\d{2})", main)
        time = f"{tm.group(1)}:{tm.group(2)}" if tm else ""
        main = re.sub(r"[^。]*(下記|ご参照|リンク|ＨＰ|HP)[^。]*。?", "", main).strip()
        free = "到着後フリータイム" in main
        main = main.replace("到着後フリータイム", "").strip()
        main = re.sub(r"^宿泊施設\s*", "", main)
        main = re.sub(r"(\S+) \1", r"\1", main)
        if main in ("宿泊施設",): main = ""
        if main:
            kind = "free" if "フリータイム" in main and len(main) < 40 else "stop"
            out.append(["stop", kind, main[:90], time])
        if free: out.append(["stop", "free", "到着後は自由行動（すぐ滑れる）", ""])
        if hm: out.append(["stop", "hotel", "HOTEL", ""])
        for n in notes[:1]:
            if "下記" in n or "リンク" in n: continue
            out.append(["note", "", n[:90]])
    return out

def parse(itin, mode):
    t = itin or ""
    d = re.split(r"2日目", t, maxsplit=1)
    d1 = steps(re.sub(r"^\s*1日目", "", d[0]))
    d2 = steps(d[1]) if len(d) > 1 else []
    first = ["stop", "home", "志木駅", ""]
    if mode == "train":
        pre = [first, ["leg", "local", "東武東上線→武蔵野線→京浜東北線 約40分（大人¥420）"]]
        post = [["leg", "local", "京浜東北線→武蔵野線→東武東上線 約40分"], ["stop", "home", "志木駅", ""]]
    elif mode == "bus":
        pre = [first, ["leg", "local", "東武東上線＋JR（池袋乗り換え）約40分＋新宿駅から都庁まで徒歩約10分"]]
        post = [["leg", "local", "JR＋東武東上線 約40分"], ["stop", "home", "志木駅", ""]]
    else:
        pre, post = [], []
    legs = sum(1 for s in d1 if s[0] == "leg" and s[1] not in ("walk", "local"))
    if mode == "bus": legs = max(legs, 1)
    return {"d1": pre + d1, "d2": d2 + post, "legs": legs}

def slope_min(sub, icon, toslope):
    s = (sub or "") + " " + (toslope or "")
    m = re.search(r"まで：\s*([^\s　]+)", s)
    t = m.group(1) if m else (toslope or "")
    w = re.match(r"徒歩(\d+)分", t)
    if w: return int(w.group(1)), t
    o = re.search(r"(シャトル|送迎|路線バス|バス)(\d+)分", t)
    if o: return int(o.group(2)) + 10, t
    if icon and "徒歩0分" in icon: return 0, "徒歩0分"
    if icon and "徒歩5分以内" in icon: return 5, "徒歩5分以内"
    return 60, (t if t and "アクセス" not in t else "")
