from flask import Flask, render_template, request
from pathlib import Path
import uuid

from src.analyzer import analyze_image


app = Flask(__name__)


# 업로드 폴더
UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # 업로드된 이미지 가져오기
    image = request.files.get("image")

    if image is None or image.filename == "":
        return "이미지를 선택해주세요."

    # 확장자 확인
    extension = Path(image.filename).suffix.lower()

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png"
    }

    if extension not in allowed_extensions:
        return "JPG, JPEG, PNG 파일만 업로드할 수 있습니다."

    # 파일 이름 충돌 방지를 위해 UUID 사용
    filename = f"{uuid.uuid4()}{extension}"

    image_path = UPLOAD_FOLDER / filename

    # 이미지 저장
    image.save(image_path)

    try:
        # 이미지 분석
        result = analyze_image(str(image_path))

    except Exception as e:
        return f"이미지 분석 중 오류가 발생했습니다: {e}"

    # 결과 페이지로 이동
    return render_template(
        "result.html",
        result=result,
        image_path=f"/static/uploads/{filename}"
    )


if __name__ == "__main__":
    app.run(debug=True)
