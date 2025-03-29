import glob
from pathlib import Path

import cv2
import numpy as np


class ImageProcessor:
    MATCH_THRESHOLD = 0.95  # テンプレートマッチングのしきい値

    def __init__(self, x1=1530, y1=470, x2=1900, y2=670):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.templates = self.load_templates()

    def load_templates(self):
        """テンプレート画像を読み込む"""
        TEMPLATE_DIR = Path("data/templates")
        name_map = {
            "kireazi": "斬れ味強化",
            "zokusei": "属性強化",
            "kaisin": "会心率強化",
            "kisokougekiryoku": "基礎攻撃力強化",
        }
        templates = {}
        for img_path in TEMPLATE_DIR.glob("*.png"):
            name = img_path.stem  # ファイル名部分のみ取得
            jp_name = name_map.get(name, name)
            template = cv2.imread(str(img_path), 0)
            if template is not None:
                templates[jp_name] = template
        return templates

    def process_frame(self, frame):
        """フレームを処理し、ROIを取得"""
        roi = frame[self.y1 : self.y2, self.x1 : self.x2]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return gray

    def match_templates(self, frame_gray):
        """テンプレートマッチングを実行"""
        matched_bonuses = []
        for name, template in self.templates.items():
            res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= self.MATCH_THRESHOLD)
            for pt in zip(*loc[::-1]):
                matched_bonuses.append((name, (pt[0], pt[1])))
        return matched_bonuses
