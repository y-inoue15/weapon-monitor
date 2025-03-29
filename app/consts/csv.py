import enum


class Csv(str, enum.Enum):
    CSV_FOLDER = "data/csv"
    HEADER_FILE = "data/json/header.json"
