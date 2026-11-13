# -*- coding: utf-8 -*-
# 比較ページ（日本語・ベトナム語）を template.html の CSS/JS から生成する
import html, re, sys, os
S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

def T(ja, vi):
    return f'<span class="l-ja">{ja}</span><span class="l-vi" lang="vi">{vi}</span>'

def yen(n): return f"¥{n:,}"

TIN_CANCEL = [("〜21日前", "đến 21 ngày trước", "0%", ""), ("20〜8日前", "20–8 ngày", "20%", "mid"),
              ("7〜2日前", "7–2 ngày", "30%", "mid"), ("前日・当日", "hôm trước / hôm đi", "40〜50%", "hi")]

# ---------- プラン ----------
# total: 5人の合計（上限計算）、pp: 1人あたり
P = []

def plan(**k): P.append(k); return k

plan(id="p1", mode="train", area="niigata", star=1,
  name=("石打丸山＋アーバンヒル石打（新幹線ツアー）", "Ishiuchi Maruyama + Urban Hill Ishiuchi (tour tàu Shinkansen)"),
  date=("12/19（土）〜20（日）", "19/12 (T7) – 20/12 (CN)"),
  co="トラベルイン", pp=21160, total=105800, rentpp=2800,
  badges=[("best", "おすすめ", "Đề xuất"), ("", "新幹線", "Shinkansen"), ("", "ゲレンデ徒歩1分", "Ra dốc 1 phút")],
  pros=[("ゲレンデまで徒歩1分。温泉つき・全室禁煙", "Đi bộ 1 phút ra dốc. Có suối nóng, toàn bộ phòng cấm hút thuốc"),
        ("夕食は日替わり鍋の食べ放題", "Bữa tối: lẩu thay đổi mỗi ngày, ăn thoải mái"),
        ("レンタルが1日700円/点と格安（板・ウェア）", "Thuê đồ rất rẻ: 700 yên/món/ngày (ván trượt, quần áo)"),
        ("大宮から乗れて往復で¥3,200引き", "Lên tàu ở Omiya, giảm 3.200 yên cho cả nhà")],
  cons=[("子どものスキースクールは12/30から（大人クラスは小学生から参加可・2時間¥6,000）", "Lớp trượt cho trẻ em chỉ từ 30/12 (lớp người lớn nhận học sinh tiểu học, 2 giờ 6.000 yên)"),
        ("小学生のこども代金は予約画面でしか出ない（下の金額は上限）", "Giá trẻ em chỉ hiện khi đặt chỗ (số tiền dưới đây là mức tối đa)"),
        ("12/19が石打のオープン予定日か公式で未確認", "Chưa xác nhận chính thức 19/12 là ngày mở cửa của Ishiuchi")],
  rows=[("ツアー代金 大人（中学生を含む）", "Giá tour người lớn (gồm học sinh THCS)", "¥21,800 × 3人（往復新幹線・宿2食・リフト1日券）", "21.800 × 3 (tàu khứ hồi, 2 bữa, vé 1 ngày)", 65400),
        ("ツアー代金 小学生", "Giá tour học sinh tiểu học", "こども代金は未確認のため大人代金で上限計算 ¥21,800 × 2人", "Chưa rõ giá trẻ em, tạm tính bằng giá người lớn 21.800 × 2", 43600),
        ("大宮乗車割引", "Giảm giá lên tàu ở Omiya", "大人 −¥800 × 3、こども −¥400 × 2", "NL −800 × 3, TE −400 × 2", -3200),
        ("越後湯沢駅⇔石打 シャトル", "Xe đưa đón ga Echigo-Yuzawa ⇔ Ishiuchi", "スキー場の無料シャトル 約20分", "Xe miễn phí của khu trượt, ~20 phút", 0)],
  extra=[("2日目もリフトに乗る（2日券に変更）", "Nếu đổi sang vé 2 ngày", "大人 +¥4,100〜5,400 × 3、こども +¥2,400〜3,000 × 2", "NL +4.100–5.400 × 3, TE +2.400–3.000 × 2", "+¥17,100〜22,200"),
         ("レンタル（全員）", "Thuê đồ (cả nhà)", "スキーセット＋ウェア 各¥700 × 2日 × 5人（予約時に申込）", "Bộ ván + quần áo, 700 × 2 ngày × 5 người", "+¥14,000")],
  lift=("1日券込み（2日券は追加）。小学生はこども料金", "Đã gồm vé 1 ngày (vé 2 ngày trả thêm)"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=2821&c3=046001&br=5G",
  urlname="トラベルイン",
  sched=[("1日目 12/19（土）", "Ngày 1 – 19/12", [("7:00頃", "大宮駅から上越新幹線（列車は1か月前に決定）", "Đi tàu Joetsu Shinkansen từ ga Omiya (giờ tàu chốt trước 1 tháng)", True),
          ("8:00頃", "越後湯沢駅着 → 無料シャトルで石打へ（約20分）", "Đến Echigo-Yuzawa → xe miễn phí đến Ishiuchi (~20 phút)", False),
          ("9:00頃", "レンタル受け取り・滑走（宿で着替え可）", "Nhận đồ thuê, trượt tuyết", False),
          ("夕方", "アーバンヒル石打にチェックイン・温泉", "Nhận phòng, tắm suối nóng", False),
          ("夜", "鍋食べ放題の夕食", "Bữa tối lẩu ăn thoải mái", True)]),
         ("2日目 12/20（日）", "Ngày 2 – 20/12", [("朝", "和朝食 → 滑走（2日券にした場合）", "Ăn sáng kiểu Nhật → trượt (nếu mua vé 2 ngày)", False),
          ("15:00頃", "シャトルで越後湯沢へ", "Xe về ga Echigo-Yuzawa", False),
          ("17:00頃", "大宮駅着（列車は予約時に選択）", "Về ga Omiya", True)])],
  cancel=[("トラベルイン（ツアー全体）", "Travel-inn (toàn bộ tour)", TIN_CANCEL, ("無料で取り消せるのは 11/28（21日前）まで。申込は出発10日前14時まで", "Hủy miễn phí đến 28/11. Hạn đăng ký: 14h, 10 ngày trước"))],
  deadline=("11/28", "無料キャンセル期限（21日前）", "hạn hủy miễn phí"),
)

plan(id="p2", mode="train", area="niigata", star=1,
  name=("上越国際＋プチハウスひろみ（新幹線ツアー）", "Joetsu Kokusai + Petit House Hiromi (tour Shinkansen)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="トラベルイン", pp=20560, total=102800, rentpp=2800,
  badges=[("", "新幹線", "Shinkansen"), ("fast", "新幹線で最安", "Rẻ nhất bằng tàu")],
  pros=[("新幹線ツアーでいちばん安い", "Rẻ nhất trong các tour tàu"), ("上越国際は広く、初心者コースが多い", "Khu Joetsu Kokusai rộng, nhiều dốc cho người mới"), ("全室禁煙・レンタル1日700円/点", "Cấm hút thuốc toàn bộ, thuê đồ 700 yên/món/ngày")],
  cons=[("ペンションのため温泉・口コミは未確認", "Là nhà nghỉ nhỏ, chưa xác nhận suối nóng/đánh giá"), ("駅からの行き方・2日券の追加額は予約画面で確認", "Cách đi từ ga và giá vé 2 ngày cần xem khi đặt")],
  rows=[("ツアー代金 大人", "Giá tour người lớn", "¥21,200 × 3人", "21.200 × 3", 63600),
        ("ツアー代金 小学生（上限）", "Giá tour trẻ em (tối đa)", "¥21,200 × 2人（こども代金は未確認）", "21.200 × 2 (chưa rõ giá trẻ em)", 42400),
        ("大宮乗車割引", "Giảm giá Omiya", "大人 −¥800 × 3、こども −¥400 × 2", "NL −800×3, TE −400×2", -3200)],
  extra=[("レンタル（全員）", "Thuê đồ (cả nhà)", "板セット＋ウェア ¥700 × 2日 × 5人", "700 × 2 ngày × 5", "+¥14,000")],
  lift=("1日券込み（上越国際＆岩原）", "Đã gồm vé 1 ngày"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=3021&c3=021001&br=5G", urlname="トラベルイン",
  sched=[("1日目 12/19（土）", "Ngày 1 – 19/12", [("7:00頃", "大宮駅から上越新幹線", "Tàu Shinkansen từ Omiya", True), ("8:00頃", "越後湯沢駅着 → 上越国際へ（行き方は行程表で確認）", "Đến Echigo-Yuzawa → đi Joetsu Kokusai", False), ("夕方", "ペンションにチェックイン・夕食", "Nhận phòng, ăn tối", True)]),
         ("2日目 12/20（日）", "Ngày 2 – 20/12", [("朝", "朝食 → 滑走", "Ăn sáng → trượt", False), ("17:00頃", "大宮駅着", "Về Omiya", True)])],
  cancel=[("トラベルイン", "Travel-inn", TIN_CANCEL, ("無料で取り消せるのは 11/28 まで", "Hủy miễn phí đến 28/11"))],
  deadline=("11/28", "無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p3", mode="bus", area="niigata", star=1,
  name=("上越国際＋プチハウスひろみ（新宿発バスツアー）", "Joetsu Kokusai + Petit House Hiromi (tour xe buýt từ Shinjuku)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="トラベルイン", pp=19900, total=99500, rentpp=2800,
  badges=[("cheap", "最安", "Rẻ nhất"), ("", "バス", "Xe buýt")],
  pros=[("全候補でいちばん安い", "Rẻ nhất trong tất cả"), ("宿・リフト・往復バスが1回の申込で済む", "Một lần đặt gồm cả xe, chỗ ở, vé")],
  cons=[("新宿（都庁の大型バス駐車場）7:10発。志木からは6時台に出発", "Xuất phát 7:10 ở Shinjuku. Phải rời Shiki khoảng 6 giờ sáng"),
        ("新幹線ツアーとの差は1人¥600ほどで、移動は約3.5時間", "Chỉ rẻ hơn tàu khoảng 600 yên/người, đi mất ~3,5 giờ"), ("池袋・大宮発のバスは見つからず", "Không tìm thấy xe từ Ikebukuro/Omiya")],
  rows=[("ツアー代金 大人", "Giá tour người lớn", "¥19,900 × 3人（往復バス・宿2食・リフト1日券）", "19.900 × 3", 59700),
        ("ツアー代金 小学生（上限）", "Giá tour trẻ em (tối đa)", "¥19,900 × 2人（こども代金は未確認）", "19.900 × 2", 39800)],
  extra=[("レンタル（全員）", "Thuê đồ", "¥700 × 2点 × 2日 × 5人", "700 × 2 × 2 × 5", "+¥14,000"), ("志木⇔新宿の電車", "Tàu Shiki ⇔ Shinjuku", "各自（往復）", "tự trả", "別途")],
  lift=("1日券込み", "Đã gồm vé 1 ngày"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=410&c1=18&c2=3011&c3=021001&br=5G", urlname="トラベルイン",
  sched=[("1日目 12/19（土）", "Ngày 1 – 19/12", [("7:10", "新宿 都庁大型バス駐車場 発", "Xuất phát bãi xe buýt Tochō, Shinjuku", True), ("10:40頃", "現地着・滑走", "Đến nơi, trượt tuyết", False), ("夕方", "チェックイン・夕食", "Nhận phòng, ăn tối", False)]),
         ("2日目 12/20（日）", "Ngày 2 – 20/12", [("16:35頃", "現地発", "Rời khu trượt", False), ("20:50頃", "新宿着・解散", "Về Shinjuku, giải tán", True)])],
  cancel=[("トラベルイン", "Travel-inn", TIN_CANCEL, ("無料で取り消せるのは 11/28 まで", "Hủy miễn phí đến 28/11"))],
  deadline=("11/28", "無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p4", mode="bus", area="niigata", star=1,
  name=("石打丸山＋アーバンヒル石打（新宿発バスツアー）", "Ishiuchi + Urban Hill Ishiuchi (xe buýt từ Shinjuku)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="トラベルイン", pp=20500, total=102500, rentpp=2800,
  badges=[("", "バス", "Xe buýt"), ("", "ゲレンデ徒歩1分", "Ra dốc 1 phút")],
  pros=[("おすすめ（p1）と同じ宿をバスで。バス停から徒歩1分", "Cùng khách sạn với gói đề xuất, đi xe buýt"), ("温泉・鍋食べ放題・全室禁煙", "Suối nóng, lẩu ăn thoải mái, cấm hút thuốc")],
  cons=[("新幹線ツアーとの差は1人¥660ほど", "Chỉ rẻ hơn tàu khoảng 660 yên/người"), ("新宿7:10発・20:50着", "Đi 7:10, về 20:50")],
  rows=[("ツアー代金 大人", "Giá người lớn", "¥20,500 × 3人", "20.500 × 3", 61500), ("ツアー代金 小学生（上限）", "Giá trẻ em (tối đa)", "¥20,500 × 2人", "20.500 × 2", 41000)],
  extra=[("2日券に変更", "Đổi vé 2 ngày", "大人 +¥4,100〜5,400、こども +¥2,400〜3,000", "", "+¥17,100〜22,200"), ("レンタル（全員）", "Thuê đồ", "¥700 × 2点 × 2日 × 5人", "", "+¥14,000")],
  lift=("1日券込み", "Đã gồm vé 1 ngày"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=410&c1=18&c2=2811&c3=046001&br=5G", urlname="トラベルイン",
  sched=[("1日目 12/19（土）", "Ngày 1", [("7:10", "新宿発", "Xuất phát Shinjuku", True), ("10:40頃", "石打着・滑走", "Đến Ishiuchi, trượt", False), ("夜", "鍋食べ放題", "Lẩu ăn thoải mái", False)]),
         ("2日目 12/20（日）", "Ngày 2", [("16:35頃", "現地発", "Rời khu trượt", False), ("20:50頃", "新宿着", "Về Shinjuku", True)])],
  cancel=[("トラベルイン", "Travel-inn", TIN_CANCEL, ("無料で取り消せるのは 11/28 まで", "Hủy miễn phí đến 28/11"))],
  deadline=("11/28", "無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p5", mode="train", area="niigata", star=1,
  name=("石打丸山＋アーバンヒル石打（ビッグホリデー・レンタル込み）", "Ishiuchi + Urban Hill (Big Holiday, đã gồm thuê đồ)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="ビッグホリデー", pp=22610, total=113050, rentpp=0,
  badges=[("", "新幹線", "Shinkansen"), ("", "レンタル込み", "Gồm thuê đồ")],
  pros=[("スキーセットとウェアが滞在中ずっと込み", "Đã gồm ván và quần áo suốt thời gian ở"), ("LINE友だち追加で5%引き（誰でも可）", "Giảm 5% khi kết bạn LINE")],
  cons=[("リフト券が代金に入るか、キャンセル料が公式で未確認", "Chưa rõ đã gồm vé cáp treo chưa, và phí hủy"), ("こども代金は予約画面で確定", "Giá trẻ em chỉ rõ khi đặt")],
  rows=[("ツアー代金（5人とも大人代金で上限計算）", "Giá tour (tính tối đa theo giá NL)", "¥23,800 × 5人", "23.800 × 5", 119000),
        ("LINE友だち追加クーポン", "Phiếu giảm giá LINE", "−5%", "−5%", -5950)],
  extra=[("リフト券", "Vé cáp treo", "予約画面で選択（込みかどうか未確認）", "chọn khi đặt", "未確認")],
  lift=("予約画面で選択（未確認）", "Chọn khi đặt (chưa rõ)"),
  url="https://www.bigs.jp/tourDetail?tourId=S59164C62401", urlname="ビッグホリデー",
  sched=[("1日目 12/19（土）", "Ngày 1", [("朝", "大宮駅から新幹線（列車は1か月前に決定）", "Tàu từ Omiya", True), ("午前", "越後湯沢 → 石打。レンタル受け取り・滑走", "Đến Ishiuchi, nhận đồ, trượt", False)]),
         ("2日目 12/20（日）", "Ngày 2", [("午後", "石打 → 越後湯沢 → 大宮", "Về Omiya", True)])],
  cancel=[("ビッグホリデー", "Big Holiday", None, ("キャンセル料は公式の取得データに載っておらず未確認。予約前に旅行条件書で確認", "Chưa xác nhận phí hủy – xem điều kiện trước khi đặt"))],
  deadline=None)

plan(id="p6", mode="train", area="niigata", star=3,
  name=("上越国際＋ホテルグリーンプラザ上越（ファミリー限定・レンタル込み）", "Joetsu Kokusai + Hotel Green Plaza Joetsu (gói gia đình, gồm thuê đồ)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="ビッグホリデー", pp=39805, total=199025, rentpp=0,
  badges=[("", "新幹線", "Shinkansen"), ("fast", "ゲレンデ0分", "Sát dốc"), ("", "★★★", "★★★")],
  pros=[("ゲレンデ直結。駅から宿泊者用の無料送迎（約25分・前日までに予約）", "Sát dốc, xe miễn phí từ ga (~25 phút, đặt trước)"),
        ("リフト1日券＋スキーセット＋ウェア1日が込み", "Gồm vé 1 ngày + ván + quần áo 1 ngày"),
        ("縁日・プール・キッズパラダイス券つき。天然温泉", "Có lễ hội, hồ bơi, khu vui chơi trẻ em, suối nóng")],
  cons=[("ほかの新潟プランの約2倍の値段", "Giá gần gấp đôi các gói khác"), ("口コミでは建物の古さ・朝食の混雑（20分待ち）", "Đánh giá: tòa nhà cũ, bữa sáng đông")],
  rows=[("ツアー代金（5人とも大人代金で上限計算）", "Giá tour (tối đa)", "¥41,900 × 5人（往復新幹線・宿2食バイキング・リフト1日・レンタル1日）", "41.900 × 5", 209500),
        ("LINE友だち追加クーポン", "Phiếu LINE", "−5%", "−5%", -10475)],
  extra=[("2日目のリフト・レンタル", "Vé & thuê đồ ngày 2", "現地で追加（料金は未確認）", "", "未確認")],
  lift=("1日券込み（2日目は別）", "Gồm vé 1 ngày"),
  review=("楽天 3.70（1,851件）／部屋3.38・夕食3.78・風呂3.70・清潔3.42", "Rakuten 3,70 (1.851 đánh giá)"),
  url="https://www.bigs.jp/tourDetail?tourId=S59164C70701", urlname="ビッグホリデー",
  sched=[("1日目 12/19（土）", "Ngày 1", [("朝", "大宮駅から新幹線", "Tàu từ Omiya", True), ("午前", "越後湯沢から宿の無料送迎（約25分）→ 滑走", "Xe miễn phí ~25 phút → trượt", False), ("夜", "夕食バイキング・縁日", "Buffet tối, lễ hội", False)]),
         ("2日目 12/20（日）", "Ngày 2", [("午後", "送迎で越後湯沢 → 大宮", "Về Omiya", True)])],
  cancel=[("ビッグホリデー", "Big Holiday", None, ("キャンセル料は未確認（旅行条件書で確認）", "Chưa xác nhận phí hủy"))],
  deadline=None)

plan(id="p7", mode="train", area="nagano", star=1,
  name=("軽井沢プリンス＋ホテル軽井沢1130（新幹線ツアー）", "Karuizawa Prince + Hotel Karuizawa 1130 (tour Shinkansen)"),
  date=("12/12（土）〜13（日）", "12/12 – 13/12"), co="トラベルイン", pp=32400, total=162000, rentpp=20400,
  badges=[("", "新幹線", "Shinkansen"), ("fast", "12/12に滑れる", "Trượt được 12/12"), ("cheap", "小学生リフト無料", "Tiểu học miễn phí cáp treo")],
  pros=[("12/12の週末に確実に滑れる（10/31から人工雪で営業中）", "Chắc chắn trượt được cuối tuần 12/12 (mở từ 31/10, tuyết nhân tạo)"),
        ("全14コース中8コースが初心者向け。スキー学校は12/1から開講", "8/14 đường trượt cho người mới. Trường trượt mở từ 1/12"),
        ("大宮から新幹線で約45分", "Từ Omiya ~45 phút bằng tàu")],
  cons=[("宿はスキー場から送迎40分＋シャトル5分（送迎は前日18時までに予約）", "Khách sạn cách khu trượt 40 phút xe đưa đón (đặt trước 18h hôm trước)"),
        ("レンタルが高い（大人セット＋ウェア1日¥11,000）", "Thuê đồ đắt (NL 11.000 yên/ngày)"), ("宿の口コミは未調査", "Chưa kiểm tra đánh giá khách sạn")],
  rows=[("ツアー代金 大人（中学生を含む）", "Giá người lớn", "¥32,400 × 3人（往復新幹線・宿2食バイキング・リフト1日券）", "32.400 × 3", 97200),
        ("ツアー代金 小学生（上限）", "Giá trẻ em (tối đa)", "¥32,400 × 2人（こども代金は未確認）", "32.400 × 2", 64800)],
  extra=[("2日券に変更", "Đổi vé 2 ngày", "大人 +¥6,000〜12,000 × 3（こどもは追加なし）", "NL +6.000–12.000 × 3", "+¥18,000〜36,000"),
         ("レンタル（スキー場・Web事前決済）", "Thuê đồ (đặt trước trên web)", "大人 セット¥6,500＋ウェア¥4,500、こども ¥5,500＋¥3,500 × 2日", "NL 11.000, TE 9.000 × 2 ngày", "+¥102,000")],
  lift=("1日券込み。小学生までは無料", "Gồm vé 1 ngày; tiểu học miễn phí"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=5021&c3=011011&br=5G", urlname="トラベルイン",
  sched=[("1日目 12/12（土）", "Ngày 1 – 12/12", [("7:30頃", "大宮駅から北陸新幹線", "Tàu Hokuriku Shinkansen từ Omiya", True), ("8:15頃", "軽井沢駅着 → スキー場シャトル（約5分）・滑走", "Đến Karuizawa → xe 5 phút → trượt", False), ("16:30", "リフト終了 → 宿の送迎（約40分・要予約）", "Xe về khách sạn (~40 phút, cần đặt)", False), ("夜", "和洋中バイキング", "Buffet tối", True)]),
         ("2日目 12/13（日）", "Ngày 2 – 13/12", [("朝", "送迎で軽井沢駅 → スキー場（2日券の場合）", "Xe ra ga → trượt (nếu vé 2 ngày)", False), ("17:00頃", "軽井沢駅から新幹線 → 大宮", "Tàu về Omiya", True)])],
  cancel=[("トラベルイン", "Travel-inn", TIN_CANCEL, ("無料で取り消せるのは 11/21（21日前）まで", "Hủy miễn phí đến 21/11"))],
  deadline=("11/21", "無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p8", mode="train", area="nagano", star=1,
  name=("白馬五竜＆Hakuba47＋白馬パークホテル（新幹線ツアー）", "Hakuba Goryu & 47 + Hakuba Park Hotel (tour Shinkansen)"),
  date=("12/12（土）〜13（日）", "12/12 – 13/12"), co="トラベルイン", pp=32520, total=162600, rentpp=2800,
  badges=[("", "新幹線", "Shinkansen"), ("", "12/12に滑れる", "Trượt được 12/12")],
  pros=[("12/12の週末に販売あり。全室禁煙", "Có bán cho cuối tuần 12/12, cấm hút thuốc"), ("レンタル1日700円/点。大宮割引 大人¥2,800", "Thuê đồ 700 yên; giảm 2.800 yên ở Omiya")],
  cons=[("長野駅⇔白馬のバスが片道¥3,500（各自・要予約）", "Xe buýt Nagano ⇔ Hakuba 3.500 yên/lượt (tự đặt)"), ("片道3時間半近くかかる", "Mất gần 3,5 giờ mỗi chiều")],
  rows=[("ツアー代金（5人とも大人代金で上限計算）", "Giá tour (tối đa)", "¥27,200 × 5人", "27.200 × 5", 136000), ("大宮乗車割引（大人）", "Giảm Omiya (NL)", "−¥2,800 × 3人", "−2.800 × 3", -8400),
        ("長野駅⇔白馬の特急バス（往復・上限）", "Xe buýt Nagano ⇔ Hakuba", "¥3,500 × 2回 × 5人（こども運賃は未確認）", "3.500 × 2 × 5", 35000)],
  extra=[("レンタル（全員）", "Thuê đồ", "¥700 × 2点 × 2日 × 5人", "", "+¥14,000")],
  lift=("1日券込み（五竜＆47共通）", "Gồm vé 1 ngày"),
  url="https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=8521&c3=006001&br=5G", urlname="トラベルイン",
  sched=[("1日目 12/12（土）", "Ngày 1", [("7:00頃", "大宮駅から北陸新幹線", "Tàu từ Omiya", True), ("8:00頃", "長野駅 → 特急バス約70分 → 白馬五竜", "Nagano → xe buýt 70 phút", False), ("10:00頃", "滑走", "Trượt", False)]),
         ("2日目 12/13（日）", "Ngày 2", [("15:30頃", "白馬 → 長野駅（バス）", "Xe về Nagano", False), ("18:30頃", "大宮駅着", "Về Omiya", True)])],
  cancel=[("トラベルイン", "Travel-inn", TIN_CANCEL, ("無料で取り消せるのは 11/21 まで", "Hủy miễn phí đến 21/11"))],
  deadline=("11/21", "無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p9", mode="train", area="niigata", star=3,
  name=("NASPAスキーガーデン＋NASPAニューオータニ（自分で手配）", "NASPA Ski Garden + NASPA New Otani (tự đặt)"),
  date=("12/19（土）〜20（日）", "19/12 – 20/12"), co="じゃらん＋えきねっと", pp=35758, total=178792, rentpp=None,
  badges=[("", "新幹線", "Shinkansen"), ("", "★★★", "★★★"), ("", "スキー専用ゲレンデ", "Khu chỉ cho trượt ván đôi")],
  pros=[("口コミ4.42（2,250件）。広い部屋・ビュッフェ（寿司・ローストビーフ）", "Đánh giá 4,42 (2.250). Phòng rộng, buffet sushi, bò nướng"),
        ("スキー専用（スノボ不可）でぶつかりにくく、初心者の家族向き", "Chỉ dành cho trượt tuyết (không ván đơn), an toàn cho người mới"),
        ("源泉かけ流しの大浴場・露天、屋内プール。全室禁煙", "Suối nóng tự nhiên, hồ bơi trong nhà, cấm hút thuốc")],
  cons=[("ツアーより1人¥1.5万ほど高い", "Đắt hơn tour khoảng 15.000 yên/người"), ("NASPAの今季のリフト料金・オープン日・レンタル料金が未確認", "Chưa xác nhận giá vé, ngày mở cửa, giá thuê đồ mùa này")],
  rows=[("宿（2食付き・禁煙・5人1室）", "Khách sạn (2 bữa, 5 người 1 phòng)", "じゃらん 12/19泊（クーポン前）", "Jalan, đêm 19/12", 98952),
        ("新幹線 大宮⇔越後湯沢（往復）", "Tàu Omiya ⇔ Echigo-Yuzawa (khứ hồi)", "指定席eチケット 大人¥6,160 × 3、こども¥3,070 × 2 × 往復", "NL 6.160 × 3, TE 3.070 × 2, × 2 chiều", 49240),
        ("リフト1日券（25-26の料金で参考）", "Vé 1 ngày (giá mùa trước)", "大人¥7,000 × 3、子ども¥4,800 × 2", "NL 7.000 × 3, TE 4.800 × 2", 30600),
        ("駅⇔ホテルの送迎", "Xe ga ⇔ khách sạn", "無料送迎バス（約3分）", "miễn phí", 0)],
  extra=[("レンタル", "Thuê đồ", "NASPAの今季料金は未確認", "", "未確認")],
  lift=("1日券（25-26：大人¥7,000・子ども¥4,800、今季は未確認）", "Vé 1 ngày (giá mùa trước)"),
  review=("楽天 4.42（2,250件）／部屋4.45・夕食4.32・風呂4.36・清潔4.46", "Rakuten 4,42 (2.250)"),
  url="https://www.jalan.net/yad330823/plan/?stayYear=2026&stayMonth=12&stayDay=19&stayCount=1&roomCount=1&adultNum=3&child1Num=1&child2Num=1", urlname="じゃらん",
  url2=("https://www.eki-net.com/", "えきねっと（新幹線）"),
  sched=[("1日目 12/19（土）", "Ngày 1", [("7:30頃", "大宮駅から上越新幹線", "Tàu từ Omiya", True), ("8:30頃", "越後湯沢 → 無料送迎でNASPA（約3分）・荷物を預けて滑走", "Xe miễn phí đến NASPA, trượt", False), ("17:30〜", "ビュッフェ夕食（〜20:00）・温泉", "Buffet tối, suối nóng", False)]),
         ("2日目 12/20（日）", "Ngày 2", [("朝", "朝食ビュッフェ → 滑走", "Ăn sáng → trượt", False), ("16:00頃", "送迎で越後湯沢 → 大宮", "Về Omiya", True)])],
  cancel=[("NASPAニューオータニ（じゃらん）", "NASPA New Otani", [("〜3日前", "đến 3 ngày", "0%", ""), ("2日前・前日", "2–1 ngày", "20%", "mid"), ("当日", "hôm đi", "80%", "hi"), ("不泊", "không đến", "100%", "hi")], ("無料で取り消せるのは 12/16 まで", "Hủy miễn phí đến 16/12")),
          ("新幹線（えきねっと）", "Tàu (Eki-net)", None, ("払い戻しの手数料は えきねっとの規定で確認（未確認）", "Phí hoàn vé: xem quy định Eki-net"))],
  deadline=("12/16", "宿の無料キャンセル期限", "hạn hủy miễn phí khách sạn"))

plan(id="p10", mode="train", area="nagano", star=2,
  name=("軽井沢プリンス＋軽井沢プリンスホテル ウエスト（自分で手配）", "Karuizawa Prince + Prince Hotel West (tự đặt)"),
  date=("12/12（土）〜13（日）", "12/12 – 13/12"), co="楽天＋えきねっと", pp=45842, total=229208, rentpp=20400,
  badges=[("", "新幹線", "Shinkansen"), ("fast", "移動がいちばんラク", "Di chuyển dễ nhất"), ("cheap", "小学生リフト無料", "Tiểu học miễn phí")],
  pros=[("軽井沢駅から無料シャトル。宿からゲレンデが近い", "Xe miễn phí từ ga, gần khu trượt"), ("口コミ4.38（3,019件）・夕食4.58のブッフェ", "Đánh giá 4,38, buffet tối 4,58"), ("12/12に確実に滑れる・スキー学校あり", "Chắc chắn trượt được 12/12")],
  cons=[("宿代が高い（5人で約16.5万円）", "Khách sạn đắt (~165.000 yên/5 người)"), ("温泉が天然か未確認／新幹線の今の運賃が未確認", "Chưa rõ suối nóng tự nhiên; giá tàu chưa cập nhật")],
  rows=[("宿（2食付き・禁煙・5人1室）", "Khách sạn (2 bữa)", "楽天 12/12泊", "Rakuten 12/12", 164628),
        ("新幹線 大宮⇔軽井沢（往復・参考）", "Tàu Omiya ⇔ Karuizawa (tham khảo)", "指定席 大人¥5,260 × 3、こども¥2,630 × 2 × 往復（運賃改定前の参考額）", "giá tham khảo trước khi tăng", 42080),
        ("リフト 大人1日券", "Vé NL 1 ngày", "¥7,500（無料会員の窓口料金・初滑り期間）× 3人（中学生は大人）", "7.500 × 3", 22500),
        ("リフト 小学生", "Vé tiểu học", "無料", "miễn phí", 0)],
  extra=[("2日目のリフト（大人）", "Vé ngày 2 (NL)", "¥7,500 × 3人", "", "+¥22,500"), ("レンタル（スキー場・Web事前決済）", "Thuê đồ", "大人¥11,000、こども¥9,000 / 日 × 2日", "", "+¥102,000")],
  lift=("大人¥7,500（無料会員）・小学生まで無料", "NL 7.500, tiểu học miễn phí"),
  review=("楽天 4.38（3,019件）／部屋4.35・夕食4.58・風呂4.30・清潔4.40", "Rakuten 4,38 (3.019)"),
  url="https://hotel.travel.rakuten.co.jp/hotelinfo/plan/29249?f_nen1=2026&f_tuki1=12&f_hi1=12&f_nen2=2026&f_tuki2=12&f_hi2=13&f_heya_su=1&f_otona_su=3&f_s1=1&f_s2=1", urlname="楽天トラベル",
  url2=("https://www.princehotels.co.jp/ski/karuizawa/winter/lift/advance_tickets/", "リフト券（公式）"),
  sched=[("1日目 12/12（土）", "Ngày 1", [("7:30頃", "大宮駅から北陸新幹線", "Tàu từ Omiya", True), ("8:15頃", "軽井沢駅着 → 無料シャトル → 滑走", "Đến ga → xe miễn phí → trượt", False), ("17:30〜", "ブッフェ夕食（要予約）・温泉棟", "Buffet tối, suối nóng", True)]),
         ("2日目 12/13（日）", "Ngày 2", [("終日", "滑走・アウトレット", "Trượt, mua sắm outlet", False), ("17:00頃", "軽井沢 → 大宮", "Về Omiya", True)])],
  cancel=[("軽井沢プリンスホテル ウエスト（楽天）", "Prince Hotel West", [("〜2日前", "đến 2 ngày", "0%", ""), ("前日", "hôm trước", "20%", "mid"), ("当日", "hôm đi", "80%", "hi"), ("不泊", "không đến", "100%", "hi")], ("無料で取り消せるのは 12/10 まで", "Hủy miễn phí đến 10/12"))],
  deadline=("12/10", "宿の無料キャンセル期限", "hạn hủy miễn phí"))

plan(id="p11", mode="car", area="nagano", star=2,
  name=("軽井沢プリンス＋プリンスホテル ウエスト（レンタカー）", "Karuizawa Prince + Prince Hotel West (thuê ô tô)"),
  date=("12/12（土）〜13（日）", "12/12 – 13/12"), co="トヨタレンタカーほか", pp=46166, total=230828, rentpp=20400,
  badges=[("", "車", "Ô tô"), ("", "雪道が少ない", "Ít đường tuyết")],
  pros=[("軽井沢は高速の出口から近く、雪道を走る距離が短い", "Gần lối ra cao tốc, ít đường tuyết"), ("荷物が多くても家から直接行ける", "Đi thẳng từ nhà, mang nhiều đồ")],
  cons=[("埼玉の店舗はスタッドレスが標準でない。追加料金と在庫が未確認", "Cửa hàng ở Saitama không có sẵn lốp mùa đông; chưa rõ giá"),
        ("新幹線より高く、運転の負担がある", "Đắt hơn tàu, phải lái xe")],
  rows=[("レンタカー W2クラス（ミニバン）", "Thuê xe W2 (minivan)", "24時間¥20,900＋以降24時間¥15,400（トヨタ一般料金）", "20.900 + 15.400", 36300),
        ("高速 練馬IC⇔碓氷軽井沢IC（往復・参考）", "Cao tốc (khứ hồi, tham khảo)", "普通車¥3,700 × 2（平日通常料金の参考。休日割引は都市部除く30%）", "3.700 × 2", 7400),
        ("宿（2食付き・禁煙）", "Khách sạn (2 bữa)", "楽天 12/12泊", "Rakuten", 164628),
        ("リフト 大人1日券", "Vé NL 1 ngày", "¥7,500 × 3人（小学生は無料）", "7.500 × 3", 22500)],
  extra=[("スタッドレスタイヤ・免責補償・ガソリン・駐車場", "Lốp mùa đông, bảo hiểm, xăng, đỗ xe", "店舗の見積もりで確認", "", "未確認"),
         ("自家用車＋タイヤレンタルにする場合", "Nếu dùng xe nhà + thuê lốp", "レンタカー代の代わりにタイヤレンタル（例：2泊3日・脱着込み約¥13,000、サイズ次第）", "~13.000 yên", "−¥23,300前後"),
         ("レンタル（スキー場）", "Thuê đồ", "大人¥11,000、こども¥9,000 / 日 × 2日", "", "+¥102,000")],
  lift=("大人¥7,500・小学生まで無料", "NL 7.500, TE miễn phí"),
  review=("楽天 4.38（3,019件）", "Rakuten 4,38"),
  url="https://rent.toyota.co.jp/", urlname="トヨタレンタカー",
  url2=("https://hotel.travel.rakuten.co.jp/hotelinfo/plan/29249?f_nen1=2026&f_tuki1=12&f_hi1=12&f_nen2=2026&f_tuki2=12&f_hi2=13&f_heya_su=1&f_otona_su=3&f_s1=1&f_s2=1", "宿（楽天）"),
  sched=[("1日目 12/12（土）", "Ngày 1", [("6:00", "志木周辺の店舗で車を借りる", "Nhận xe ở Shiki", True), ("6:20頃", "所沢IC → 関越道 → 上信越道", "Lên cao tốc ở Tokorozawa", False), ("8:30頃", "碓氷軽井沢IC → スキー場（駐車場は宿泊者用を確認）", "Đến khu trượt", False), ("夜", "ホテルで夕食", "Ăn tối ở khách sạn", False)]),
         ("2日目 12/13（日）", "Ngày 2", [("15:30頃", "スキー場発", "Rời khu trượt", False), ("18:30頃", "店舗に返却（渋滞で遅れる場合あり）", "Trả xe", True)])],
  cancel=[("レンタカー", "Thuê xe", None, ("キャンセル料は店舗・会社の規定で確認（未確認）", "Phí hủy: xem quy định cửa hàng")),
          ("軽井沢プリンスホテル ウエスト", "Prince Hotel West", [("〜2日前", "đến 2 ngày", "0%", ""), ("前日", "hôm trước", "20%", "mid"), ("当日", "hôm đi", "80%", "hi"), ("不泊", "không đến", "100%", "hi")], ("無料で取り消せるのは 12/10 まで", "Hủy miễn phí đến 10/12"))],
  deadline=None,
  car=True)

exec(open(os.path.join(S,'add_dates.py'),encoding='utf-8').read())
# ★順 → 安い順
P.sort(key=lambda p: (-p["star"], p["pp"]))
BEST = "p1"

def stars(n): return "★" * n

def card(i, p):
    b = "".join(f'<span class="badge {c}">{T(j, v)}</span>' for c, j, v in p["badges"])
    sel = " selected" if p["id"] == BEST else ""
    rows = ""
    for j, v, nj, nv, amt in p["rows"]:
        rows += f'<tr><td>{T(j, v)}<small>{T(nj, nv or nj)}</small></td><td>{yen(amt) if amt >= 0 else "−" + yen(-amt)}</td></tr>'
    rows += f'<tr class="total"><td>{T("合計（5人・上限） ／ 1人あたり", "Tổng (5 người, tối đa) / mỗi người")}</td><td>{yen(p["total"])} ／ {yen(p["pp"])}</td></tr>'
    for j, v, nj, nv, amt in p["extra"]:
        rows += f'<tr class="rental"><td>{T(j, v)}<small>{T(nj, nv or nj)}</small></td><td>{amt}</td></tr>'
    pc = "".join(f'<p class="pro">{T(j, v)}</p>' for j, v in p["pros"]) + "".join(f'<p class="con">{T(j, v)}</p>' for j, v in p["cons"])
    rev = f'<p class="muted">{T("口コミ：", "Đánh giá: ")}{T(*p["review"])}</p>' if p.get("review") else f'<p class="muted">{T("口コミ：楽天で未調査（★は「確かめられた特長が少ない」という意味）", "Đánh giá: chưa kiểm tra")}</p>'
    btn2 = f'<a class="btn sub" href="{html.escape(p["url2"][0])}" target="_blank" rel="noopener">{T("予約ページ", "Trang đặt")} <small>{p["url2"][1]}</small></a>' if p.get("url2") else ""
    rent = "" if p["rentpp"] in (0, None) else f' {T("＋レンタル", "+ thuê đồ")} {yen(p["rentpp"])}'
    if p["rentpp"] == 0: rent = f' {T("（レンタル込み）", "(gồm thuê đồ)")}'
    return f'''
      <article class="card{sel}" id="card-{p["id"]}" data-mode="{p["mode"]}" data-area="{p["area"]}" data-plan="{p["id"]}">
        <div class="card-head"><div class="rank num">{i}</div><div>
          <h3>{T(*p["name"])}</h3>
          <div class="badges"><span class="badge viewing"{"" if sel else " hidden"}>{T("表示中", "Đang xem")}</span>{b}</div></div></div>
        <p class="muted"><span class="stars">{stars(p["star"])}</span> ・ {T(*p["date"])} ・ {p["co"]}</p>
        <div class="price-row"><div class="price-big num"><span class="yen">¥</span>{p["pp"]:,}</div><div class="price-unit">{T("1人あたり（上限）", "mỗi người (tối đa)")}{rent}</div></div>
        <p class="muted">{T("リフト：", "Vé: ")}{T(*p["lift"])}</p>
        {rev}
        <div class="pc">{pc}</div>
        <div class="bd"><h4>{T("料金の内訳（5人分）", "Chi tiết giá (5 người)")}</h4><table class="breakdown">{rows}</table></div>{datetable(p)}{schooltable(p)}
        <div class="btns">
          <a class="btn" href="{html.escape(p["url"])}" target="_blank" rel="noopener">{T("このプランを予約", "Đặt gói này")} <small>{p["urlname"]}</small></a>{btn2}
          <button class="btn show" type="button" data-show="{p["id"]}">{T("日程・キャンセル料を見る", "Xem lịch trình & phí hủy")}</button>
        </div>
      </article>'''

def sched(p):
    out = ""
    for (dj, dv, items) in p["sched"]:
        li = "".join(f'<li class="{"key" if k else ""}"><span class="t">{t}</span><span class="dot"></span><span class="what">{T(j, v)}</span></li>' for t, j, v, k in items)
        out += f'<div class="day"><h3>{T(dj, dv)}</h3><ol class="timeline">{li}</ol></div>'
    return f'<div class="plan-block" data-plan="{p["id"]}"{"" if p["id"] == BEST else " hidden"}>{out}<p class="muted">{T("時刻は目安です。新幹線の列車は乗車1か月前に決まります。", "Giờ chỉ là dự kiến.")}</p></div>'

def cancel(p):
    out = ""
    for nj, nv, steps, (mj, mv) in p["cancel"]:
        st = ""
        if steps:
            st = '<div class="steps">' + "".join(f'<div class="step {c}">{T(a, b)}<b>{pct}</b></div>' for a, b, pct, c in steps) + "</div>"
        out += f'<div class="cancel"><h3>{T(nj, nv)}</h3>{st}<p class="muted">{T(mj, mv)}</p></div>'
    return f'<div class="plan-block" data-plan="{p["id"]}"{"" if p["id"] == BEST else " hidden"}>{out}</div>'

def bar(i, p):
    best = " best" if p["id"] == BEST else ""
    return f'<button class="bar{best}" type="button" data-mode="{p["mode"]}" data-area="{p["area"]}" data-plan="{p["id"]}" data-value="{p["pp"]}" aria-pressed="{"true" if p["id"] == BEST else "false"}"><span class="name">{i}. {T(*p["name"])}</span><span class="val num">{yen(p["pp"])}</span><span class="track"><span class="fill" style="display:block;width:50%"></span></span></button>'

byid = {p["id"]: p for p in P}
def mn(mode): return min(p["pp"] for p in P if p["mode"] == mode)

def verdict(mode, pid, label, reasons, hidden):
    p = byid[pid]
    rs = "".join(f"<li>{T(j, v)}</li>" for j, v in reasons)
    dl = f'<div class="deadline">{T("予約するなら", "Nên đặt trước")} <span class="num">{p["deadline"][0]}</span> {T("まで（" + p["deadline"][1] + "）", "(" + p["deadline"][2] + ")")}</div>' if p.get("deadline") else ""
    return f'''
  <section class="verdict"{' id="best"' if mode == "all" else ""} data-mode="{mode}" data-plan="{pid}"{" hidden" if hidden else ""}>
    <span class="label">{T(*label)}</span>
    <h2>{T(*p["name"])}</h2>
    <p class="muted">{T(*p["date"])}</p>
    <div class="price-row"><div class="price-big num"><span class="yen">¥</span>{p["pp"]:,}</div><div class="price-unit">{T("1人あたり（5人・上限） 総額", "mỗi người · tổng 5 người")} {yen(p["total"])}</div></div>
    <ul class="reasons">{rs}</ul>{dl}
    <div class="btns"><a class="btn" href="{html.escape(p["url"])}" target="_blank" rel="noopener">{T("予約する", "Đặt ngay")} <small>{p["urlname"]}</small></a>
      <button class="btn show" type="button" data-show="{pid}">{T("日程・キャンセル料を見る", "Xem lịch trình & phí hủy")}</button></div>
  </section>'''

V = verdict("all", "p1", ("いちばんおすすめ", "Đề xuất số 1"), [
    ("新幹線ツアーで、宿2食・リフト1日券込み・レンタルも1日700円/点と安い", "Tour tàu rẻ, gồm 2 bữa và vé 1 ngày; thuê đồ chỉ 700 yên/món"),
    ("ゲレンデまで徒歩1分・温泉・全室禁煙・鍋食べ放題", "Ra dốc 1 phút, suối nóng, cấm hút thuốc, lẩu ăn thoải mái"),
    ("大宮から約1時間。12/19-20の週末で、21日前（11/28）まで無料キャンセル", "Từ Omiya ~1 giờ; hủy miễn phí đến 28/11")], False)
V += verdict("train", "p1", ("新幹線ならこれ", "Nếu đi tàu"), [("総合のおすすめと同じ", "Giống gói đề xuất"), ("12/12に行くなら軽井沢（p7・p10）", "Nếu đi 12/12 thì chọn Karuizawa")], True)
V += verdict("bus", "p3", ("バスならこれ", "Nếu đi xe buýt"), [("全候補で最安", "Rẻ nhất"), ("ただし新幹線ツアーとの差は1人¥600ほど", "Chỉ rẻ hơn tàu ~600 yên/người")], True)
V += verdict("car", "p11", ("車ならこれ", "Nếu đi ô tô"), [("雪道の運転に慣れていないなら、高速の出口から近い軽井沢", "Karuizawa gần lối ra cao tốc, ít đường tuyết"), ("ただしレンタカーのスタッドレス料金・在庫は店舗で確認", "Cần hỏi cửa hàng về lốp mùa đông")], True)

cards = "".join(card(i + 1, p) for i, p in enumerate(P))
bars = "".join(bar(i + 1, p) for i, p in enumerate(P))
scheds = "".join(sched(p) for p in P)
cancels = "".join(cancel(p) for p in P)
best = byid[BEST]

# 目的別の総評
GOALS = [
  ("総合", "Tổng thể", "p1", "石打＋アーバンヒル（新幹線）。安さ・宿の近さ・食事のバランスが良い", "Ishiuchi + Urban Hill (tàu): cân bằng giá, vị trí, bữa ăn"),
  ("安さ", "Giá rẻ", "p3", "上越国際＋ひろみ（バス）1人¥19,900〜。ただし新幹線版と¥600差", "Joetsu + Hiromi (xe buýt) từ 19.900 yên"),
  ("移動がラク", "Di chuyển dễ", "p10", "軽井沢（新幹線約45分・駅からシャトル）。12/12でも確実に滑れる", "Karuizawa: tàu 45 phút, chắc chắn có tuyết 12/12"),
  ("ご飯", "Bữa ăn", "p9", "NASPAニューオータニ（ビュッフェ 夕食4.32）", "NASPA New Otani (buffet 4,32)"),
  ("温泉・宿の評価", "Suối nóng & đánh giá", "p9", "NASPAニューオータニ（4.42・源泉かけ流し）。スキー専用ゲレンデで初心者向き", "NASPA New Otani (4,42, suối nóng tự nhiên)"),
]
goals = "".join(f'<div class="goal"><b>{T(a, b)}</b><span>{T(j, v)}</span><button class="link" type="button" data-show="{pid}">{T("見る", "Xem")}</button></div>' for a, b, pid, j, v in GOALS)

# 日程の比較（週末か平日か）
def _cell(v):
    return f"<td>{v:,}</td>" if isinstance(v, int) else f'<td class="na">{T(*v)}</td>'
_rows = "".join(f'<tr><td>{T(*SHORT[p["id"]])}</td>' + "".join(_cell(v) for v in DT[p["id"]]) + "</tr>" for p in P)
_th = "".join(f'<th>{d}<br>{T(j, v)}</th>' for d, j, v in DATES)
DATECMP = f"""
  <section id="dates">
    <h2>{T("日程で比べる（週末3回・平日2回）", "So sánh theo ngày")}</h2>
    <div class="note"><b>{T(DATE_VERDICT[0], DATE_VERDICT[1])}</b>{T(DATE_BODY[0], DATE_BODY[1])}</div>
    <div class="tablewrap"><table class="cmp"><tr><th>{T("プラン（1人あたり・上限・円）", "Gói (mỗi người, yên)")}</th>{_th}</tr>{_rows}</table></div>
    <p class="muted">{T(DATE_FOOT[0], DATE_FOOT[1])}</p>
  </section>"""
OTHERS = [
  ("志賀高原＋志賀ハイランドホテル（新幹線ツアー）", "大人¥27,200〜（12/12）。長野駅からのバス代が別で未確認", "https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=6021&c3=016001&br=5G"),
  ("野沢温泉＋ナイス信濃荘（新幹線ツアー）", "大人¥27,700〜（12/12）。駅からのバス代が別で未確認", "https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=7221&c3=031001&br=5G"),
  ("苗場＋シュプールイン苗場（新幹線ツアー）", "大人¥27,500〜（12/19）。苗場は小学生リフト無料・中学生は中高生料金", "https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=2721&c3=001001&br=5G"),
  ("上越国際＋グリーンプラザ上越（トラベルイン）", "大人¥31,900〜（12/19・1日券付き）。レンタルは別。BHのレンタル込み版（p6）と比べる", "https://www.jalan.net/yad378210/plan/"),
  ("湯沢東映ホテル（自分で手配）", "★★★ 4.09。5人1室 12/19 ¥87,780（じゃらん）。湯沢高原のリフト料金が未確認", "https://www.jalan.net/yad355725/plan/"),
  ("苗場プリンスホテル（自分で手配）", "★★★ 3.65。5人1室なし・2室で12/19 ¥130,881。小学生リフト無料", "https://hotel.travel.rakuten.co.jp/hotelinfo/plan/30694"),
  ("ホテルグリーンプラザ白馬（自分で手配）", "★★★ 4.25。12/12 ¥69,300（じゃらん・5人）。白馬乗鞍の12/12営業が未確認", "https://www.jalan.net/yad321447/plan/"),
]
others = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{n}</a>：{d}</li>' for n, d, u in OTHERS)

EXCL = [
  "新潟の宿の12/12・12/16泊（湯沢東映 ¥36,960など安い）：周りのスキー場がまだオープン前で滑れない",
  "エンゼルグランディア越後中里：湯沢中里は例年12/28ごろオープンで12月中旬は滑れない",
  "湯沢グランドホテル：12/12・12/19が満室（12/16の早割は11/16ごろが締切）",
  "GALA湯沢：12/12〜18は滑走不可。12/19からは南エリア休止。日帰り向きで宿のプランは見つからず",
  "舞子高原ホテル：冬のプランが未発売で料金・空きを確認できず",
  "かぐら：上級者寄りで初心者の家族には不向き",
  "ビッグホリデー 軽井沢プリンスウエスト：基本が食事なし（2食付きの条件に合わない）",
  "志賀高原プリンス・白馬シェラリゾートなど：同じエリアのツアーより大幅に高い（5人で11万〜14万円）",
  "池袋・大宮発のバス：今回の検索では見つからず",
  "12/26泊：NASPAニューオータニ・湯沢グランド・ホテル双葉・舞子高原ホテル・軽井沢プリンスウエスト・苗場プリンス（5人1室）が満室（11/13時点）",
  "12/23泊の湯沢の宿（湯沢グランド¥142,800・リブマックス¥148,377など5人）：ツアーより大幅に高い",
  "エンゼルグランディア越後中里 12/23（5人¥55,520と安い）：湯沢中里は例年12/28ごろオープンで、まだ滑れない可能性が高い",
  "タイムズカーシェア：志木周辺でスタッドレス付き・5人乗りの車があるか確認できず（ログインが必要）",
]
excl = "".join(f"<li>{x}</li>" for x in EXCL)

SRC = [
  ("軽井沢プリンスホテルスキー場 リフト料金", "https://www.princehotels.co.jp/ski/karuizawa/winter/lift/"),
  ("軽井沢プリンス レンタル", "https://www.princehotels.co.jp/ski/karuizawa/winter/info/"),
  ("苗場スキー場 リフト料金", "https://www.princehotels.co.jp/ski/naeba/winter/lift/"),
  ("トラベルイン アーバンヒル石打（新幹線）", "https://yoyaku.travel-inn.co.jp/dom_tour_tin/tintour/JP/detail?hcd=I0&tp=412&c1=18&c2=2821&c3=046001&br=5G"),
  ("ビッグホリデー ツアーAPI（dpf.bigs.jp）", "https://dpf.bigs.jp/tour/api/v1/tour/S59164C70701?lang=ja&paxPerRoom=5&goDate=20261219"),
  ("NASPAニューオータニ（じゃらん）", "https://www.jalan.net/yad330823/plan/"),
  ("軽井沢プリンスホテル ウエスト（楽天）", "https://hotel.travel.rakuten.co.jp/hotelinfo/plan/29249"),
  ("大宮〜越後湯沢の新幹線料金", "https://jr-group.jp/toki-ryokin/"),
  ("大宮〜軽井沢の新幹線料金（参考・改定前）", "https://shinkansen-kakuyasu.net/ohmiya-karuizawa-ryokin/"),
  ("トヨタレンタカー 料金表", "https://rent.toyota.co.jp/service/charge/pricelist.aspx?tab=H&carType=4"),
  ("ニッポンレンタカー スタッドレス", "https://www.nipponrentacar.co.jp/car_price/option/studless-tire.html"),
  ("練馬〜碓氷軽井沢の高速料金（参考）", "https://www.mapple.net/p_article/528139/"),
  ("休日割引（2026年度）", "https://jafmate.jp/car/traffic_topics_20260419_1198935.html"),
  ("スタッドレスのレンタル例", "https://bestcarweb.jp/news/car-accessory/368473?prd=2"),
  ("GALA湯沢 26-27シーズン", "https://tabiris.com/?p=66745"),
  ("軽井沢プリンス 26-27オープン", "https://www.princehotels.co.jp/press/202610_05/"),
  ("舞子スノーリゾート", "https://niigata-kankou.or.jp/spot/10694"),
  ("NASPAスキーガーデン（25-26）", "https://niigata-kankou.or.jp/spot/10688"),
]
src = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SRC)

NOTES = [
  ("warn", "12月中旬は雪が少ないことがある", "Giữa tháng 12 có thể ít tuyết", "オープン直後は一部のコースだけのことがあります。出発の数日前に各スキー場の公式サイトで積雪とコースを確認してください。人工雪の軽井沢がいちばん確実です。", "Ngay sau khi mở cửa có thể chỉ mở một phần. Hãy xem tình hình tuyết vài ngày trước. Karuizawa (tuyết nhân tạo) chắc chắn nhất."),
  ("warn", "車は雪道に注意", "Lái xe: chú ý đường tuyết", "関越道の湯沢周辺は12月でも大雪で通行止めになったことがあります。雪道の運転に慣れていないなら新幹線がおすすめ。車なら雪の少ない軽井沢へ。チェーン規制中はスタッドレスでもチェーンが必要です。", "Cao tốc Kan-etsu gần Yuzawa từng bị đóng vì tuyết. Nếu chưa quen lái trên tuyết, nên đi tàu."),
  ("", "こども料金について", "Về giá trẻ em", "ツアーは中学生が大人料金、小学生がこども料金です。こども代金は予約画面にしか出ないため、このページの金額は5人とも大人料金で計算した「上限」です。実際はもっと安くなります。", "Học sinh THCS tính giá người lớn, tiểu học tính giá trẻ em. Giá trẻ em chỉ hiện khi đặt, nên số tiền ở đây là mức tối đa."),
  ("", "スキースクール", "Lớp học trượt tuyết", "全員初心者なら、初日にスクール（2時間¥6,000〜7,500程度）がおすすめ。石打の子ども向けは12/30から、軽井沢は12/1から開講。", "Người mới nên học 2 giờ ngày đầu (~6.000–7.500 yên)."),
  ("", "手袋・ゴーグル・帽子", "Găng tay, kính, mũ", "多くのレンタルにはなく、あっても大人サイズのみ。子どもの分は持っていくと安心です。", "Thường không cho thuê cỡ trẻ em – nên mang theo."),
]
notes = "".join(f'<div class="note {c}"><b>{T(a, b)}</b>{T(j, v)}</div>' for c, a, b, j, v in NOTES)

css = open(os.path.join(S, "tpl_css.html"), encoding="utf-8").read()
css = css.replace('family=Barlow+Condensed', 'family=Noto+Sans:wght@400;700;900&family=Barlow+Condensed')
css = css.replace("<title>スノボ旅行 湯沢 12/20</title>", '<title>スキー旅行 家族5人 12月中旬</title>\n<meta name="robots" content="noindex,nofollow">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
EXTRA_CSS = '''
/* 言語の切り替え */
html[data-lang="ja"] .l-vi, html[data-lang="vi"] .l-ja { display: none; }
.langs { position: absolute; top: 14px; right: max(16px, env(safe-area-inset-right, 0px)); z-index: 2; display: flex; gap: 4px; background: rgba(255,255,255,.16); border-radius: 999px; padding: 3px; }
.langs button { border: 0; background: transparent; color: var(--night-ink); font-weight: 900; font-size: 14px; min-height: 36px; min-width: 52px; border-radius: 999px; cursor: pointer; }
.langs button[aria-pressed="true"] { background: var(--accent); color: var(--accent-ink); }
.areas { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; background: rgba(255,255,255,.12); border-radius: 12px; padding: 4px; position: relative; z-index: 1; margin-top: 6px; }
.area { border: 0; background: transparent; color: var(--night-ink); min-height: 40px; border-radius: 9px; font-weight: 700; font-size: 14px; cursor: pointer; }
.area[aria-pressed="true"] { background: var(--surface); color: var(--ink); }
.stars { color: var(--accent); letter-spacing: .05em; }
.goals { display: flex; flex-direction: column; gap: 8px; }
.goal { background: var(--surface); border-radius: 12px; padding: 10px 12px; display: grid; grid-template-columns: 92px 1fr auto; gap: 8px; align-items: center; font-size: 14px; }
.goal b { color: var(--accent); }
.link { border: 0; background: var(--ice-soft); color: var(--ice); font-weight: 700; border-radius: 8px; min-height: 36px; padding: 0 12px; cursor: pointer; }
.tablewrap { overflow-x: auto; background: var(--surface); border-radius: var(--radius); }
.cmp { width: 100%; border-collapse: collapse; font-size: 13px; }
.cmp th, .cmp td { padding: 8px 6px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; font-family: var(--font-num); font-size: 15px; }
.cmp th:first-child, .cmp td:first-child { text-align: left; white-space: normal; font-family: var(--font-body); font-size: 13px; }
.cmp th { font-size: 12px; color: var(--ink-2); }
.hero-band { padding-top: 64px; }
.plan-block[hidden], .verdict[hidden], .card[hidden], .bar[hidden], section[hidden] { display: none !important; }
.bd h4, .dt h4 { margin: 4px 0 0; font-size: 14px; }
.dt table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 6px; }
.dt th, .dt td { padding: 6px 4px; border-bottom: 1px solid var(--line); text-align: center; }
.dt th { font-size: 12px; color: var(--ink-2); font-weight: 700; }
.dt td { font-family: var(--font-num); font-size: 15px; font-weight: 600; }
.dt td.na { font-family: var(--font-body); font-size: 11px; color: var(--ink-2); font-weight: 400; }
.dt td.best { color: var(--accent); }
#dates .cmp { min-width: 600px; }
#dates .cmp td:first-child { min-width: 150px; }
.cmp td.na { font-family: var(--font-body); font-size: 11px; color: var(--ink-2); }
.dt td.main { background: var(--ice-soft); }
.school { background: var(--surface-2); border-radius: 10px; padding: 10px 12px; font-size: 13px; }
.school b { display: block; font-size: 14px; margin-bottom: 2px; }
@media (min-width: 960px) {
  .wrap { max-width: 1120px; }
  .hero-band > div { max-width: 760px; }
  .verdict { max-width: 760px; }
  .cards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); align-items: start; }
  .goals { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #schedule .plan-block, #cancel .plan-block { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
}
html[data-lang="vi"] body { font-family: "Noto Sans", system-ui, -apple-system, "Segoe UI", sans-serif; }
</style>'''
css = css.replace("</style>", EXTRA_CSS, 1)

js = open(os.path.join(S, "tpl_js.html"), encoding="utf-8").read()
# エリアの絞り込みと言語の切り替えを足す
js = js.replace('var state = { mode: "all", plan: null };', 'var state = { mode: "all", area: "all", plan: null };')
js = js.replace('function inMode(el) { return state.mode === "all" || el.dataset.mode === state.mode; }',
  'function inMode(el) { return (state.mode === "all" || el.dataset.mode === state.mode) && (state.area === "all" || el.dataset.area === state.area); }')
js = js.replace('var card = document.querySelector(\'.card[data-plan="\' + id + \'"] h3\');',
  'var card = document.querySelector(\'.card[data-plan="\' + id + \'"] h3 .l-\' + (document.documentElement.dataset.lang || "ja"));')
js = js.replace('if (count) count.textContent = (state.mode === "all" ? "おすすめ順・全" : "おすすめ順・") + shown + "件";',
  'if (count) count.textContent = (document.documentElement.dataset.lang === "vi" ? shown + " gói" : "★順・" + shown + "件");')
js = js.replace('$(".mode").forEach(function (b) { b.addEventListener("click", function () { setMode(b.dataset.mode); }); });',
  '''$(".mode").forEach(function (b) { b.addEventListener("click", function () { setMode(b.dataset.mode); }); });
  $(".area").forEach(function (b) { b.addEventListener("click", function () { state.area = b.dataset.area; $(".area").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); render(); }); });
  function setLang(l) { document.documentElement.dataset.lang = l; document.documentElement.lang = l; $(".langs button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.lang === l)); }); try { localStorage.setItem("lang", l); } catch (e) {} render(); }
  $(".langs button").forEach(function (b) { b.addEventListener("click", function () { setLang(b.dataset.lang); }); });
  try { var saved = localStorage.getItem("lang"); if (saved === "vi" || saved === "ja") { document.documentElement.dataset.lang = saved; document.documentElement.lang = saved; $(".langs button").forEach(function (x) { x.setAttribute("aria-pressed", String(x.dataset.lang === saved)); }); } } catch (e) {}''')

modes = f'''<button class="mode" type="button" data-mode="all" aria-pressed="true">{T("すべて", "Tất cả")}<small>{len(P)}{T("件", " gói")}</small></button>
        <button class="mode" type="button" data-mode="train" aria-pressed="false">{T("新幹線", "Tàu")}<small>{yen(mn("train"))}〜</small></button>
        <button class="mode" type="button" data-mode="bus" aria-pressed="false">{T("バス", "Xe buýt")}<small>{yen(mn("bus"))}〜</small></button>
        <button class="mode" type="button" data-mode="car" aria-pressed="false">{T("車", "Ô tô")}<small>{yen(mn("car"))}〜</small></button>'''

body = f'''
<div class="wrap">
  <header class="hero-band">
    <div class="langs" role="group" aria-label="Language"><button type="button" data-lang="ja" aria-pressed="true">日本語</button><button type="button" data-lang="vi" aria-pressed="false">Tiếng Việt</button></div>
    <div>
      <div class="eyebrow">SKI TRIP</div>
      <h1>{T("家族5人 スキー旅行 1泊2日", "Chuyến trượt tuyết gia đình 5 người, 2 ngày 1 đêm")}</h1>
      <div class="trip-meta">
        <span>{T("12月中旬〜下旬（12/12・16・19・23・26を比較）", "Tháng 12 (so sánh 12, 16, 19, 23, 26/12)")}</span>
        <span>{T("大人2・中学生1・小5・小3", "2 người lớn, 1 THCS, lớp 5, lớp 3")}</span>
        <span>{T("全員スキー初心者・フルレンタル", "Tất cả mới tập, thuê đồ đầy đủ")}</span>
        <span>{T("志木発／新幹線は大宮から", "Từ Shiki / tàu từ Omiya")}</span>
        <span>{T("2026/11/13 調査", "Khảo sát 13/11/2026")}</span>
      </div>
    </div>
    <div>
      <div class="mode-label" id="mode-label">{T("交通手段で選ぶ", "Chọn phương tiện")}</div>
      <div class="modes" role="group" aria-labelledby="mode-label">{modes}</div>
      <div class="mode-label" style="margin-top:10px">{T("エリアで選ぶ", "Chọn khu vực")}</div>
      <div class="areas" role="group"><button class="area" type="button" data-area="all" aria-pressed="true">{T("すべて", "Tất cả")}</button><button class="area" type="button" data-area="niigata" aria-pressed="false">{T("新潟", "Niigata")}</button><button class="area" type="button" data-area="nagano" aria-pressed="false">{T("長野", "Nagano")}</button></div>
    </div>
    <svg class="ridge" viewBox="0 0 400 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0 44 L0 30 L40 18 L70 26 L120 6 L160 22 L200 12 L250 28 L300 4 L340 20 L370 14 L400 24 L400 44 Z"/></svg>
  </header>
  {V}
  <nav class="toc" aria-label="目次">
    <a href="#best">{T("結論", "Kết luận")}</a><a href="#goals">{T("目的別", "Theo mục đích")}</a><a href="#dates">{T("週末/平日", "Ngày")}</a><a href="#compare">{T("候補", "Các gói")}</a>
    <a href="#school">{T("スクール", "Trường")}</a><a href="#schedule">{T("日程", "Lịch trình")}</a><a href="#cancel">{T("キャンセル料", "Phí hủy")}</a><a href="#notes">{T("注意", "Lưu ý")}</a><a href="#more">{T("詳細", "Chi tiết")}</a>
  </nav>
  <section id="goals"><h2>{T("目的別の総評", "Gợi ý theo mục đích")}</h2><div class="goals">{goals}</div></section>
  {DATECMP}
  <section id="compare">
    <h2>{T("候補を比べる", "So sánh các gói")} <small id="compare-count"></small></h2>
    <p class="muted">{T("★の多い順、同じ★なら安い順。★★★＝天然温泉の大浴場＋口コミ3.5以上・100件以上、★★＝3.0以上・15件以上、★＝確かめられた特長が少ない（悪いという意味ではない）。口コミは楽天トラベルでそろえています。金額は「交通＋宿2食＋リフト」の1人あたりで、小学生も大人料金で数えた上限です。レンタルは別に表示。", "Sắp xếp theo ★ rồi theo giá. Giá = đi lại + khách sạn 2 bữa + vé, mỗi người, tính tối đa (trẻ em tính như người lớn). Đánh giá theo Rakuten Travel. Thuê đồ ghi riêng.")}</p>
    <div class="bars" aria-label="1人あたりの費用">{bars}</div>
    <div class="cards">{cards}</div>
    <div class="more"><details><summary>{T("そのほかの候補（概要）", "Các lựa chọn khác")}</summary><ul>{others}</ul></details></div>
  </section>
  <section id="school"><h2>{T("スキースクール", "Trường trượt tuyết")}</h2>
    <div class="tablewrap"><table class="cmp"><tr><th>{T("スキー場", "Khu trượt")}</th><th>{T("料金など", "Giá")}</th><th>{T("今回の日程", "Ngày đi")}</th></tr>{"".join(f'<tr><td>{a}</td><td style="white-space:normal;text-align:left;font-family:var(--font-body);font-size:13px">{b}</td><td style="font-family:var(--font-body);font-size:12px;white-space:normal">{c}</td></tr>' for a,b,c in SCHOOL_ALL)}</table></div>
    <p class="muted">{T("全員初心者なら、初日の午前にグループレッスン（2時間〜半日）を受けるのがおすすめ。料金は現地払いが多く、上の旅行代金には入っていません。", "Người mới nên học nhóm buổi sáng ngày đầu. Phí học chưa gồm trong giá trên.")}</p>
  </section>
  <section id="schedule"><h2>{T("日程", "Lịch trình")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b></div>{scheds}</section>
  <section id="cancel"><h2>{T("キャンセル料", "Phí hủy")}</h2><div class="viewing-bar">{T("表示中：", "Đang xem: ")}<b data-plan-name></b></div>{cancels}</section>
  <section id="notes"><h2>{T("注意", "Lưu ý")}</h2><div class="notes">{notes}</div></section>
  <section id="more"><h2>{T("詳細", "Chi tiết")}</h2>
    <div class="more">
      <details><summary>{T("除外した候補と理由", "Các gói bị loại")}（{len(EXCL)}）</summary><ul>{excl}</ul></details>
      <details><summary>{T("調べきれなかったこと", "Chưa xác nhận được")}</summary><ul>
        <li>ツアーの小学生のこども代金（予約画面に進まないと出ない）</li>
        <li>ビッグホリデーのキャンセル料とリフト券の扱い（旅行条件書で確認）</li>
        <li>志木周辺のレンタカーのスタッドレス料金・在庫、正確な高速代（NEXCOの料金検索で確認）</li>
        <li>NASPA・石打・上越国際の今季のオープン日とリフト料金（公式サイトで確認）</li>
        <li>一休・Yahoo!トラベル・各宿公式の料金（今回は楽天・じゃらんで比較）</li>
      </ul></details>
      <details><summary>{T("出典URL", "Nguồn")}</summary><ul>{src}</ul></details>
      <p class="muted">{T("調査量（合計）：約60サイト・検索とページ取得など約200回", "Khối lượng khảo sát: ~60 trang web, ~200 lượt tìm kiếm")}</p>
    </div>
  </section>
  <footer>{T("料金は2026/11/13時点のものです。予約前に各サイトで確認してください。", "Giá tại thời điểm 13/11/2026. Vui lòng kiểm tra lại trước khi đặt.")}</footer>
</div>
'''
page = "<!doctype html>\n<html lang=\"ja\" data-lang=\"ja\">\n<head>\n" + css.replace("<style>", "<style>", 1) + "\n</head>\n<body>" + body + js + "\n</body>\n</html>\n"
# head/body を正しく分ける：css 部分には title, meta, link, style が入っている
open(OUT, "w", encoding="utf-8").write(page)
print("written", OUT, len(page))
