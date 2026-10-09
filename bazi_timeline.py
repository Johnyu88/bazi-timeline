"""
八字时间轴 · 单文件版
依赖: pip install lunar-python
"""
from lunar_python import Solar

GAN_WUXING = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土",
              "己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
ZHI_WUXING = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火",
              "午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}
GAN_YINYANG = {"甲":"阳","乙":"阴","丙":"阳","丁":"阴","戊":"阳",
               "己":"阴","庚":"阳","辛":"阴","壬":"阳","癸":"阴"}
SHENG = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
KE    = {"木":"土","土":"水","水":"火","火":"金","金":"木"}


def get_shishen(day_gan, target_gan):
    dw, tw = GAN_WUXING[day_gan], GAN_WUXING[target_gan]
    same = GAN_YINYANG[day_gan] == GAN_YINYANG[target_gan]
    if dw == tw:        return "比肩" if same else "劫财"
    if SHENG[dw] == tw: return "食神" if same else "伤官"
    if KE[dw] == tw:    return "偏财" if same else "正财"
    if KE[tw] == dw:    return "七杀" if same else "正官"
    if SHENG[tw] == dw: return "偏印" if same else "正印"
    return "?"


def build_chart(year, month, day, hour, minute=0):
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
    ec = solar.getLunar().getEightChar()
    ygz, mgz, dgz, hgz = ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()
    day_gan = dgz[0]
    pillars = {
        "年": {"gan": ygz[0], "zhi": ygz[1]},
        "月": {"gan": mgz[0], "zhi": mgz[1]},
        "日": {"gan": dgz[0], "zhi": dgz[1]},
        "时": {"gan": hgz[0], "zhi": hgz[1]},
    }
    shishen = {pos: get_shishen(day_gan, p["gan"]) for pos, p in pillars.items()}
    return {
        "raw": {"年": ygz, "月": mgz, "日": dgz, "时": hgz},
        "day_master": day_gan,
        "day_master_wuxing": GAN_WUXING[day_gan],
        "pillars": pillars,
        "shishen": shishen,
    }


def wuxing_count(chart):
    c = {"木":0,"火":0,"土":0,"金":0,"水":0}
    for p in chart["pillars"].values():
        c[GAN_WUXING[p["gan"]]] += 1
        c[ZHI_WUXING[p["zhi"]]] += 1
    return c


def get_dayun(year, month, day, hour, gender="男", count=8):
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    ec = solar.getLunar().getEightChar()
    ec.setSect(2)
    yun = ec.getYun(1 if gender == "男" else 0)
    out = []
    for dy in yun.getDaYun()[:count]:
        out.append({"age": dy.getStartAge(),
                    "year": dy.getStartYear(),
                    "gz": dy.getGanZhi()})
    return out


def get_liunian(year, month, day, hour, gender, idx):
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    ec = solar.getLunar().getEightChar()
    ec.setSect(2)
    yun = ec.getYun(1 if gender == "男" else 0)
    dy = yun.getDaYun()[idx]
    return [{"year": ln.getYear(), "age": ln.getAge(), "gz": ln.getGanZhi()}
            for ln in dy.getLiuNian()]


def detect_interactions(chart, dy_gz, ln_gz):
    r = []
    he_gan = {("甲","己"),("乙","庚"),("丙","辛"),("丁","壬"),("戊","癸")}
    he_zhi = {("子","丑"),("寅","亥"),("卯","戌"),("辰","酉"),("巳","申"),("午","未")}
    chong  = {("子","午"),("丑","未"),("寅","申"),("卯","酉"),("辰","戌"),("巳","亥")}

    pairs = [("日干vs流年", chart["day_master"], ln_gz[0]),
             ("大运干vs流年干", dy_gz[0], ln_gz[0])]
    for label, a, b in pairs:
        if (a,b) in he_gan or (b,a) in he_gan:
            r.append(f"{label}:{a}{b}合")

    zp = [("大运支vs流年支", dy_gz[1], ln_gz[1])]
    for pos, p in chart["pillars"].items():
        zp.append((f"{pos}支vs流年", p["zhi"], ln_gz[1]))
    for label, a, b in zp:
        if (a,b) in he_zhi or (b,a) in he_zhi: r.append(f"{label}:{a}{b}合")
        if (a,b) in chong  or (b,a) in chong:  r.append(f"{label}:{a}{b}冲")
    return r


def make_judgment(ln_shen, inter):
    kw = {"比肩":"自我/合作/竞争","劫财":"破财/朋友/行动",
          "食神":"表达/享受/才华","伤官":"变动/创意/不服管",
          "偏财":"机会/流动/人脉","正财":"稳定收入/务实",
          "七杀":"压力/挑战/突破","正官":"责任/规则/晋升",
          "偏印":"思考/学习/孤独","正印":"贵人/庇护/成长"}
    base = kw.get(ln_shen, "")
    return f"主题:{base}" + (f"。注意:{','.join(inter)}" if inter else "")


def slice_liunian(chart, dy_gz, ln_gz, ln_year):
    ln_shen = get_shishen(chart["day_master"], ln_gz[0])
    dy_shen = get_shishen(chart["day_master"], dy_gz[0])
    mc = wuxing_count(chart)
    mc[GAN_WUXING[dy_gz[0]]] += 1; mc[ZHI_WUXING[dy_gz[1]]] += 1
    mc[GAN_WUXING[ln_gz[0]]] += 1; mc[ZHI_WUXING[ln_gz[1]]] += 1
    strong = max(mc, key=mc.get); weak = min(mc, key=mc.get)
    inter = detect_interactions(chart, dy_gz, ln_gz)
    return {
        "切片": f"{ln_year}年 {ln_gz} 流年",
        "大运": f"{dy_gz}大运({dy_shen})",
        "五行": f"最旺:{strong}({mc[strong]}) 最弱:{weak}({mc[weak]})",
        "十神": f"流年天干为{ln_shen}",
        "交互": inter if inter else "无",
        "判断": make_judgment(ln_shen, inter),
    }


def run(year, month, day, hour, gender="男"):
    print("=" * 50)
    print(f"出生: {year}-{month}-{day} {hour}时  性别:{gender}")
    print("=" * 50)

    chart = build_chart(year, month, day, hour)
    print("\n【本命四柱】")
    for pos in ["年","月","日","时"]:
        p = chart["pillars"][pos]
        print(f"  {pos}柱: {p['gan']}{p['zhi']}  十神:{chart['shishen'][pos]}")

    print(f"\n【日主】{chart['day_master']} ({chart['day_master_wuxing']})")
    print(f"【五行分布】{wuxing_count(chart)}")

    dayun = get_dayun(year, month, day, hour, gender)
    print("\n【大运】")
    for d in dayun:
        print(f"  {d['age']}岁起 ({d['year']}年): {d['gz']}")

    idx = 2
    if idx < len(dayun):
        print(f"\n【{dayun[idx]['gz']} 大运下的流年切片】")
        for ln in get_liunian(year, month, day, hour, gender, idx)[:8]:
            s = slice_liunian(chart, dayun[idx]["gz"], ln["gz"], ln["year"])
            print(f"\n  ▶ {s['切片']}  大运:{s['大运']}")
            print(f"    五行: {s['五行']}")
            print(f"    十神: {s['十神']}")
            print(f"    交互: {s['交互']}")
            print(f"    判断: {s['判断']}")


if __name__ == "__main__":
    BIRTH_YEAR = 1990
    BIRTH_MONTH = 6
    BIRTH_DAY = 15
    BIRTH_HOUR = 14
    GENDER = "男"

    run(BIRTH_YEAR, BIRTH_MONTH, BIRTH_DAY, BIRTH_HOUR, GENDER)
