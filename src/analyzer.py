from pathlib import Path

from src.preprocessing import preprocess_image
from src.color.colorhistogram import compare_with_dataset
from src.clip import analyze_clip_image

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


# 가중치
COLOR_WEIGHT = 0.3
CLIP_WEIGHT = 0.7


def analyze_image(image_path):
    """
    Color Histogram과 CLIP을 결합하여
    화풍별 최종 유사도를 계산한다.
    """

    # -------------------------
    # 1. Color Histogram
    # -------------------------

    query_image = preprocess_image(image_path)

    color_scores = {}

    for style, dataset_path in STYLE_DATASETS.items():

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"데이터셋 폴더를 찾을 수 없습니다: {dataset_path}"
            )

        score = compare_with_dataset(
            query_image,
            str(dataset_path)
        )

        color_scores[style] = score


    # -------------------------
    # 2. CLIP
    # -------------------------

    clip_scores = analyze_clip_image(image_path)

    # -------------------------
    # 3. 최종 점수 계산
    # -------------------------

    final_scores = {}

    for style in STYLE_DATASETS:

        color_score = color_scores[style]

        # CLIP이 0~1 범위라면 0~100으로 변환
        clip_score = clip_scores[style] * 100

        final_score = (
            color_score * COLOR_WEIGHT
            + clip_score * CLIP_WEIGHT
        )

        final_scores[style] = round(final_score, 2)

    # -------------------------
    # 4. 가장 유사한 화풍
    # -------------------------

    best_style = max(
        final_scores,
        key=final_scores.get
    )

    return {
        "color_scores": color_scores,
        "clip_scores": clip_scores,
        "final_scores": final_scores,
        "best_style": best_style
    }