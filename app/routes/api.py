import json
import time

from flask import Blueprint, Response, jsonify, request

from app.services.csv_service import CSVService
from app.services.recognizer import BonusRecognizer

api_bp = Blueprint("api", __name__, url_prefix="/api")

recognizer = BonusRecognizer()


@api_bp.route("/start", methods=["POST"])
def start_recognition():
    """画像認識を開始"""
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"success": False, "message": "無効なCSVファイル名"}), 400
    if recognizer.start(filename):  # 認識開始
        return jsonify({"message": "Recognition started"}), 200
    return jsonify({"message": "Recognition is already running"}), 400


@api_bp.route("/stop", methods=["POST"])
def stop_recognition():
    """画像認識を停止"""
    if recognizer.stop():
        return jsonify({"message": "Recognition stopped"}), 200
    return jsonify({"message": "Recognition is not running"}), 400


@api_bp.route("/video_feed")
def video_feed():
    """カメラ映像ストリーミング"""
    return recognizer.video_feed()


@api_bp.route("/get_csv_list")
def get_csv_list_api():
    csv_service = CSVService()
    csv_list = csv_service.get_csv_list()
    return jsonify(csv_list)


@api_bp.route("/sse_csv_data")
def sse_csv_data():
    csv_service = CSVService()
    filename = request.args.get("filename")

    def generate_csv_data():
        while True:
            csv_data = csv_service.read_data(filename)
            yield f"data: {json.dumps(csv_data)}\n\n"
            time.sleep(1)

    return Response(generate_csv_data(), content_type="text/event-stream")


@api_bp.route("/get_csv_data", methods=["GET"])
def get_csv_data():
    """CSVデータを取得してJSONで返す"""
    csv_service = CSVService()
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"success": False, "message": "ファイル名が指定されていません"}), 400

    data = csv_service.read_data(filename)
    return jsonify(data)


@api_bp.route("/delete_selected_rows", methods=["POST"])
def delete_selected_rows():
    """選択された行を削除"""
    csv_service = CSVService()
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"success": False, "message": "ファイル名が指定されていません"}), 400
    rows_to_delete = request.json.get("rows", [])
    if not rows_to_delete:
        return jsonify({"success": False, "message": "削除する行が指定されていません"}), 400

    csv_service.delete_selected_rows(filename, rows_to_delete)
    return jsonify({"success": True})


@api_bp.route("/delete_csv", methods=["POST"])
def delete_csv():
    """CSVを削除"""
    csv_service = CSVService()
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"success": False, "message": "削除するCSVファイル名が指定されていません"}), 400

    csv_service.delete_csv()
    return jsonify({"message": f"{filename} CSV file deleted"}), 200


@api_bp.route("/create_new_csv", methods=["POST"])
def create_new_csv():
    """新規CSVを作成"""
    csv_service = CSVService()
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"success": False, "message": "CSVファイル名が指定されていません"}), 400

    if csv_service.is_exist_csv(filename):
        return jsonify({"success": False, "message": "既に存在するCSVです"}), 400

    csv_service.create_new_csv_bounus(filename)
    return jsonify({"success": True, "message": f"{filename} CSVファイルが作成されました"}), 201
