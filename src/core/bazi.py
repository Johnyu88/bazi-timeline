from src.core.constants import GAN, ZHI, GAN_WUXING, ZHI_CANGGAN

SHISHEN_MAP = {
    "同我_同": "比肩", "同我_異": "劫財",
    "我生_同": "食神", "我生_異": "傷官",
    "我克_同": "偏財", "我克_異": "正財",
    "克我_同": "七殺", "克我_異": "正官",
    "生我_同": "偏印", "生我_異": "正印"
}

WUXING_RELATION = {
    ("木", "木"): "同我", ("木", "火"): "我生", ("木", "土"): "我克", ("木", "金"): "克我", ("木", "水"): "生我",
    ("火", "火"): "同我", ("火", "土"): "我生", ("火", "金"): "我克", ("火", "水"): "克我", ("火", "木"): "生我",
    ("土", "土"): "同我", ("土", "金"): "我生", ("土", "水"): "我克", ("土", "木"): "克我", ("土", "火"): "生我",
    ("金", "金"): "同我", ("金", "水"): "我生", ("金", "木"): "我克", ("金", "火"): "克我", ("金", "土"): "生我",
    ("水", "水"): "同我", ("水", "木"): "我生", ("水", "火"): "我克", ("水", "土"): "克我", ("水", "金"): "生我"
}

def get_shishen(day_master: str, target_gan: str) -> str:
    if day_master == target_gan:
        return "日主"
    
    dm_wuxing = GAN_WUXING[day_master]
    target_wuxing = GAN_WUXING[target_gan]
    
    relation = WUXING_RELATION[(dm_wuxing, target_wuxing)]
    
    dm_gender = GAN.index(day_master) % 2
    target_gender = GAN.index(target_gan) % 2
    gender_relation = "同" if dm_gender == target_gender else "異"
    
    return SHISHEN_MAP[f"{relation}_{gender_relation}"]

class BaziChart:
    def __init__(self, year_gan: str, year_zhi: str,
                 month_gan: str, month_zhi: str,
                 day_gan: str, day_zhi: str,
                 hour_gan: str, hour_zhi: str):
        self.year = (year_gan, year_zhi)
        self.month = (month_gan, month_zhi)
        self.day = (day_gan, day_zhi)
        self.hour = (hour_gan, hour_zhi)
        self.day_master = day_gan

    def parse_chart(self) -> dict:
        pillars = {"年柱": self.year, "月柱": self.month, "日柱": self.day, "時柱": self.hour}
        result = {}

        for name, (gan, zhi) in pillars.items():
            gan_shishen = get_shishen(self.day_master, gan) if name != "日柱" else "日主(元神)"
            
            canggan_info = []
            for cg, weight in ZHI_CANGGAN[zhi]:
                cg_shishen = get_shishen(self.day_master, cg)
                canggan_info.append({"藏干": cg, "十神": cg_shishen, "權重": weight})

            result[name] = {
                "干支": f"{gan}{zhi}",
                "天干": gan,
                "天干十神": gan_shishen,
                "地支": zhi,
                "地支藏干": canggan_info
            }
        return result
