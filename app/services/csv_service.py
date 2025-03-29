import os
from typing import List

from app.consts.csv import Csv
from app.services.csv_handler import CSVHandler


class CSVService:
    def __init__(self):
        """CSVサービスクラス"""
        self.csv_handler = CSVHandler()

    def save_data(self, filename, data: List[str]):
        """データをCSVに保存"""
        self.csv_handler.save_to_csv(filename, data)

    def read_data(self, filename):
        """CSVデータを読み込む"""
        return self.csv_handler.read_csv(filename)

    def delete_selected_rows(self, filename: str, rows_to_delete: List[List[str]]):
        """選択した行を削除"""
        self.csv_handler.delete_selected_rows(filename, rows_to_delete)

    def delete_csv(self, filename: str):
        """CSVファイルを削除"""
        self.csv_handler.delete_csv(filename)

    def get_csv_list(self) -> List[str]:
        """CSVフォルダ内のCSVを取得"""
        return self.csv_handler.get_csv_list()

    def is_exist_csv(self, filename: str) -> bool:
        """CSVの存在確認"""
        return self.csv_handler.is_exist_csv(filename)

    def create_new_csv_bounus(self, filename: str):
        """新しいCSVを作成"""
        self.csv_handler.initialize_csv(filename, "bonus")
