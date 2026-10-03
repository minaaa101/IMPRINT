import cv2
import numpy as np
import os


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def extract_color_histogram(image: np.ndarray) -> np.ndarray:
    """
    RGB 이미지에서 HSV 기반 Color Histogram을 추출한다.

    Parameters
    ----------
    image : np.ndarray
        RGB 형식의 이미지

    Returns
    -------
    np.ndarray
        정규화된 Color Histogram
    """

    if image is None:
        raise ValueError("이미지가 없습니다.")

    if not isinstance(image, np.ndarray):
        raise TypeError("이미지는 numpy.ndarray 형식이어야 합니다.")

    # RGB → HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Hue + Saturation Histogram
    histogram = cv2.calcHist(
        [hsv],
        [0, 1],
        None,
        [50, 60],
        [0, 180, 0, 256]
    )

    # 정규화
    cv2.normalize(
        histogram,
        histogram,
        alpha=0,
        beta=1,
        norm_type=cv2.NORM_MINMAX
    )

    return histogram


def compare_histograms(
    histogram1: np.ndarray,
    histogram2: np.ndarray
) -> float:
    """
    두 Color Histogram의 유사도를 계산한다.

    Returns
    -------
    float
        0~100 범위의 Color Similarity Score
    """

    score = cv2.compareHist(
        histogram1,
        histogram2,
        cv2.HISTCMP_CORREL
    )

    # 0~1 범위로 제한
    score = max(0.0, min(1.0, score))

    return score * 100


def color_similarity(
    image1: np.ndarray,
    image2: np.ndarray
) -> float:
    """
    두 RGB 이미지의 색상 유사도를 계산한다.

    Parameters
    ----------
    image1 : np.ndarray
        첫 번째 RGB 이미지

    image2 : np.ndarray
        두 번째 RGB 이미지

    Returns
    -------
    float
        Color Similarity Score (0~100)
    """

    histogram1 = extract_color_histogram(image1)
    histogram2 = extract_color_histogram(image2)

    return compare_histograms(histogram1, histogram2)

def get_dataset_images(dataset_path):
    """
    데이터셋 폴더 안에 있는 모든 이미지 경로를 가져온다.
    """

    image_paths = []

    for root, _, files in os.walk(dataset_path):
        for filename in files:
            extension = os.path.splitext(filename)[1].lower()

            if extension in SUPPORTED_EXTENSIONS:
                image_paths.append(
                    os.path.join(root, filename)
                )

    return image_paths


def load_rgb_image(image_path):
    """
    이미지 파일을 RGB numpy 배열로 불러온다.
    한글 파일명도 처리할 수 있다.
    """

    data = np.fromfile(
        image_path,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        data,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise ValueError(
            f"이미지를 불러올 수 없습니다: {image_path}"
        )

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


def compare_with_dataset(query_image, dataset_path):
    """
    하나의 입력 이미지와 데이터셋 전체를 비교한다.

    Parameters
    ----------
    query_image : np.ndarray
        RGB 형식의 입력 이미지

    dataset_path : str
        비교할 데이터셋 폴더

    Returns
    -------
    float
        데이터셋 전체와의 평균 Color Similarity
    """

    image_paths = get_dataset_images(dataset_path)

    if not image_paths:
        raise ValueError(
            f"데이터셋에 이미지가 없습니다: {dataset_path}"
        )

    query_histogram = extract_color_histogram(query_image)

    scores = []

    for image_path in image_paths:

        dataset_image = load_rgb_image(image_path)

        dataset_histogram = extract_color_histogram(
            dataset_image
        )

        score = compare_histograms(
            query_histogram,
            dataset_histogram
        )

        scores.append(score)

    return float(np.mean(scores))