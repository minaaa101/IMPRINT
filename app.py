from flask import Flask, render_template, request, jsonify
from pathlib import Path
import uuid

from src.analyzer import analyze_image


app = Flask(__name__)


# =========================
# 업로드 폴더
# =========================

UPLOAD_FOLDER = Path("static/uploads")

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ABOUT
# =========================

@app.route("/about.html")
def about():
    return render_template("about.html")


# =========================
# ANALYSIS PAGE
# =========================

@app.route("/analysis.html")
def analysis_page():

    return render_template(
        "analysis.html"
    )


# =========================
# UPLOAD
# =========================

@app.route("/analyze", methods=["POST"])
def analyze():

    image = request.files.get("image")

    if image is None or image.filename == "":
        return "이미지를 선택해주세요."

    extension = Path(
        image.filename
    ).suffix.lower()

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png"
    }

    if extension not in allowed_extensions:
        return "JPG, JPEG, PNG 파일만 업로드할 수 있습니다."

    # UUID 파일명
    filename = f"{uuid.uuid4()}{extension}"

    image_path = UPLOAD_FOLDER / filename

    # 이미지 저장
    image.save(image_path)

    # 분석 페이지로 이동
    return render_template(
        "analysis.html",
        image_path=f"/static/uploads/{filename}"
    )


# =========================
# ACTUAL ANALYSIS
# =========================

@app.route("/run-analysis", methods=["POST"])
def run_analysis():

    image_path = request.form.get("image_path")

    if not image_path:

        return jsonify({
            "success": False,
            "message": "이미지 경로가 없습니다."
        })


    try:

        # /static/uploads/xxx.png
        # ↓
        # static/uploads/xxx.png

        relative_path = image_path.lstrip("/")


        # 실제 이미지 분석
        result = analyze_image(
            relative_path
        )


        return jsonify({

            "success": True,

            "result": result,

            "image_path": image_path

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# =========================
# RESULT
# =========================

@app.route("/result")
def result_page():

    return render_template(
        "result.html"
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )