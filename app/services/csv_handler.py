import csv
import json
import os
import time
from pathlib import Path
from typing import List

from app.consts.csv import Csv


class CSVHandler:
    def __init__(self):
        self.csv_folder = Csv.CSV_FOLDER
        self.header_file = Csv.HEADER_FILE

    def ensure_directory_exists(self, filename: str):
        """ディレクトリが存在しない場合に作成"""
        csv_filename = self.get_csv_path(filename)
        csv_filename.parent.mkdir(parents=True, exist_ok=True)  # ディレクトリ作成

    def load_headers(self, data_type: str) -> List[str]:
        """ヘッダー情報をJSONから読み込む"""
        f = open(self.header_file, "r")
        headers = json.load(f)
        return headers[data_type]

    def read_csv(self, filename: str) -> List[List[str]]:
        """CSVの内容をリストで取得"""
        csv_filename = self.get_csv_path(filename)
        if not csv_filename.exists():
            return []

        with csv_filename.open(mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)

    def load_csv_headers(self, csv_filename: str) -> List[str]:
        """CSVファイルからヘッダー情報を取得"""
        headers = []
        with open(csv_filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader)
        return headers

    def initialize_csv(self, filename: str, data_type):
        """CSVファイルが存在しない場合、新規作成してヘッダーを書き込む"""
        headers = self.load_headers(data_type)
        csv_filename = self.get_csv_path(filename)
        if not csv_filename.exists():
            with csv_filename.open(mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

    def save_to_csv(self, filename: str, data: List[str]):
        """CSVにデータを追加"""
        csv_filename = self.get_csv_path(filename)
        headers = self.load_csv_headers(csv_filename)

        if len(data) != len(headers) - 1:
            raise ValueError(f"データの項目数がヘッダーと一致しません: {headers}")

        with csv_filename.open(mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S")] + data)

    def read_csv(self, filename: str) -> List[List[str]]:
        """CSVの内容をリストで取得"""
        csv_filename = self.get_csv_path(filename)
        if not csv_filename.exists():
            return []

        with csv_filename.open(mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)

    def delete_selected_rows(self, filename, rows_to_delete: List[List[str]]):
        """指定した行を削除"""
        csv_filename = self.get_csv_path(filename)
        data = self.read_csv(filename)
        if not data:
            return

        headers = data[0]  # ヘッダーを保持
        filtered_data = [row for row in data[1:] if row not in rows_to_delete]  # 行をフィルタ

        with csv_filename.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(filtered_data)

    def delete_csv(self, filename: str):
        """CSVファイルを削除"""
        csv_filename = self.get_csv_path(filename)
        if csv_filename.exists():
            csv_filename.unlink()

    def get_csv_path(self, filename: str) -> Path:
        """CSVパスを取得"""
        if not filename.endswith(".csv"):
            filename += ".csv"
        return Path(os.path.join(self.csv_folder, filename))

    def is_exist_csv(self, filename: str) -> bool:
        """CSVの存在確認"""
        if not filename.endswith(".csv"):
            filename += ".csv"
        return os.path.exists(os.path.join(self.csv_folder, filename))

    def get_csv_list(self) -> List[str]:
        """CSVフォルダ内のCSVを取得"""
        return [f for f in os.listdir(self.csv_folder) if f.endswith(".csv")]
