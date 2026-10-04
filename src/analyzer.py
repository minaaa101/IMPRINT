from pathlib import Path

from src.preprocessing import preprocess_image
from src.color.colorhistogram import compare_with_dataset


# 프로젝트 루트
BASE_DIR = Path(__file__).resolve().parent.parent

# 데이터셋 폴더
DATASET_DIR = BASE_DIR / "dataset"


# 분석할 화풍과 데이터셋 폴더
STYLE_DATASETS = {
    "Ghibli": DATASET_DIR / "ghibli",
    "Disney": DATASET_DIR / "disney",
    "Simpsons": DATASET_DIR / "simpsons",
}


def analyze_image(image_path):
    """
    입력 이미지를 각 화풍 데이터셋과 비교하여
    Color Histogram 기반 유사도를 계산한다.

    Parameters
    ----------
    image_path : str
        분석할 이미지 경로

    Returns
    -------
    dict
        화풍별 유사도와 가장 높은 화풍
    """

    # 1. 입력 이미지 전처리
    query_image = preprocess_image(image_path)

    scores = {}

    # 2. 각 화풍 데이터셋과 비교
    for style, dataset_path in STYLE_DATASETS.items():

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"데이터셋 폴더를 찾을 수 없습니다: {dataset_path}"
            )

        score = compare_with_dataset(
            query_image,
            str(dataset_path)
        )

        scores[style] = round(score, 2)

    # 3. 가장 높은 유사도의 화풍 선택
    best_style = max(
        scores,
        key=scores.get
    )

    return {
        "scores": scores,
        "best_style": best_style
    }