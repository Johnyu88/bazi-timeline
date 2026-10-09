import unittest
from src.core.bazi import get_shishen

class TestShishenMapping(unittest.TestCase):
    def test_basic_shishen(self):
        self.assertEqual(get_shishen("甲", "甲"), "日主")
        self.assertEqual(get_shishen("甲", "乙"), "劫財")
        self.assertEqual(get_shishen("甲", "丙"), "食神")
        self.assertEqual(get_shishen("甲", "丁"), "傷官")
        self.assertEqual(get_shishen("甲", "戊"), "偏財")
        self.assertEqual(get_shishen("甲", "己"), "正財")
        self.assertEqual(get_shishen("甲", "庚"), "七殺")
        self.assertEqual(get_shishen("甲", "辛"), "正官")
        self.assertEqual(get_shishen("甲", "壬"), "偏印")
        self.assertEqual(get_shishen("甲", "癸"), "正印")

if __name__ == "__main__":
    unittest.main()
