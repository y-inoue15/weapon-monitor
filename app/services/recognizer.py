import threading
import time
from collections import defaultdict

import cv2
from flask import Response, stream_with_context

from app.services.csv_handler import CSVHandler
from app.services.image_processor import ImageProcessor


class BonusRecognizer:
    FRAME_DELAY = 1  # 一致確定後の待機時間（秒）
    CONFIRMATION_COUNT = 3  # ボーナス確定に必要な一致回数
    REQUIRED_BONUS_COUNT = 5  # 記録するボーナスの数

    # 監視対象エリアの座標 (左上 x, y, 右下 x, y)
    ROI_COORDS = (1530, 470, 1900, 670)

    def __init__(self):
        self.cap = None
        self.running = False
        self.thread = None
        self.stop_event = threading.Event()
        self.match_counts = defaultdict(int)
        self.prev_bonuses = []
        self.repeat_count = 0
        self.processor = ImageProcessor()
        self.csv_handler = CSVHandler()
        self.csv_filename = None

    def start(self, csv_filename: str):
        """画像認識を開始 (CSVのファイル名を指定)"""
        if self.running:
            return False  # すでに実行中なら何もしない

        self.csv_filename = csv_filename
        self.running = True
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return True

    def stop(self):
        """画像認識を停止"""
        if not self.running:
            return False

        self.running = False
        self.csv_filename = None
        if self.cap:
            self.stop_event.set()
            self.thread.join()
            self.cap.release()
        cv2.destroyAllWindows()
        return True

    def run(self):
        """カメラ映像を処理するループ"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("カメラから映像を取得できませんでした。")
                break

            # ROI領域を取得
            x1, y1, x2, y2 = self.ROI_COORDS
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 赤枠を描画

            gray_frame = self.processor.process_frame(frame)
            matched_bonuses = self.processor.match_templates(gray_frame)

            for bonus, (x, y) in matched_bonuses:
                self.match_counts[(bonus, x, y)] += 1

            confirmed_bonuses = [
                (b, x, y) for (b, x, y), count in self.match_counts.items() if count >= self.CONFIRMATION_COUNT
            ]
            confirmed_bonuses.sort(key=lambda item: item[2])  # Y座標でソート

            if len(confirmed_bonuses) == self.REQUIRED_BONUS_COUNT:
                bonus_names = [b for b, _, _ in confirmed_bonuses]

                if bonus_names == self.prev_bonuses:
                    self.repeat_count += 1
                else:
                    self.prev_bonuses = bonus_names
                    self.repeat_count = 1

                if self.repeat_count >= self.CONFIRMATION_COUNT:
                    self.csv_handler.save_to_csv(self.csv_filename, bonus_names)
                    self.match_counts.clear()
                    time.sleep(self.FRAME_DELAY)

    def generate_frames(self):
        """カメラ映像をJPEG画像としてストリーミング"""
        while self.running:
            success, frame = self.cap.read()
            if not success:
                break

            # 監視対象に赤枠を描画
            x1, y1, x2, y2 = self.ROI_COORDS
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    def video_feed(self):
        """Flask の Response を利用して映像をストリーミング"""
        return Response(
            stream_with_context(self.generate_frames()), mimetype="multipart/x-mixed-replace; boundary=frame"
        )
