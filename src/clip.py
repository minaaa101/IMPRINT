import os

import open_clip
import torch
from PIL import Image

"""
지금 코드는 데이터셋 이미지가 100장이면 CLIP을 100번 매번 다시 계산함
기능 확인용으로는 괜찮지만 최종 프로그램에서는 비효율적
후에 데이터셋을 미리 embedding으로 변환해두고 저장한 후, 
입력 이미지와 비교하는 방식으로 개선 필요
"""

STYLE_DATASETS = {
    "ghibli": "dataset/ghibli",
    "disney": "dataset/disney",
    "simpsons": "dataset/simpsons",
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def load_clip_model():
    """
    OpenCLIP의 ViT-B-32 모델과 이미지 전처리기를 불러오는 함수.
    
    Returns:
        model: CLIP 이미지 인코더
        processor: CLIP 전용 이미지 전처리기
    """
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='openai')

    model.eval()  # 모델을 평가 모드로 설정

    return model, preprocess

def get_image_embedding(image_path, model, preprocess):
    """
    이미지 한 장을 CLIP embedding 벡터로 변환하는 함수.

    Args:
        image_path (str): 이미지 파일 경로
        model: CLIP 이미지 인코더
        preprocess: CLIP 전용 이미지 전처리기

    Returns:
        torch.Tensor: 정규화된 이미지 embedding
    """
    image = Image.open(image_path).convert("RGB")

    image = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model.encode_image(image)

    # 벡터 정규화
    embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding

def calculate_clip_similarity(embedding1, embedding2):
    """
    두 CLIP embedding 사이의 cosine similarity를 계산하는 함수.

    Args:
        embedding1 (torch.Tensor): 첫 번째 이미지 embedding
        embedding2 (torch.Tensor): 두 번째 이미지 embedding

    Returns:
        float: 두 이미지의 CLIP 유사도
    """
    similarity = (embedding1 @ embedding2.T).item()

    return similarity


def compare_with_dataset(
    input_embedding,
    dataset_path,
    model,
    preprocess
):
    """
    입력 이미지와 특정 화풍 데이터셋의 모든 이미지를 비교하고
    평균 CLIP 유사도를 계산하는 함수.

    Args:
        input_embedding (torch.Tensor): 입력 이미지 embedding
        dataset_path (str): 데이터셋 폴더 경로
        model: CLIP 이미지 인코더
        preprocess: CLIP 전용 이미지 전처리기

    Returns:
        float: 데이터셋의 평균 CLIP cosine similarity
    """
    similarities = []

    for filename in os.listdir(dataset_path):

        extension = os.path.splitext(filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            continue

        image_path = os.path.join(
            dataset_path,
            filename
        )

        dataset_embedding = get_image_embedding(
            image_path,
            model,
            preprocess
        )

        similarity = calculate_clip_similarity(
            input_embedding,
            dataset_embedding
        )

        similarities.append(similarity)

    if not similarities:
        raise ValueError(
            f"분석 가능한 이미지가 없습니다: {dataset_path}"
        )

    average_similarity = (
        sum(similarities) / len(similarities)
    )

    return average_similarity

def compare_all_styles(
    input_embedding,
    model,
    preprocess
):
    """
    입력 이미지를 모든 화풍 데이터셋과 비교하는 함수.

    Returns:
        dict: 화풍별 평균 CLIP cosine similarity
    """
    results = {}

    for style, dataset_path in STYLE_DATASETS.items():

        score = compare_with_dataset(
            input_embedding,
            dataset_path,
            model,
            preprocess
        )

        results[style] = score

    return results


def analyze_clip_image(image_path):
    model, preprocess = load_clip_model()

    input_embedding = get_image_embedding(
        image_path,
        model,
        preprocess
    )

    results = compare_all_styles(
        input_embedding,
        model,
        preprocess
    )

    return {
        "Ghibli": results["ghibli"],
        "Disney": results["disney"],
        "Simpsons": results["simpsons"]
    }


if __name__ == "__main__":
    model, preprocess = load_clip_model()

    input_embedding = get_image_embedding(
        "test.jpg",
        model,
        preprocess
    )

    results = compare_all_styles(
        input_embedding,
        model,
        preprocess
    )

    print("\nCLIP 분석 결과")

    for style, score in results.items():
        print(f"{style}: {score:.4f}")

    # 가장 유사한 화풍 찾기
    best_style = max(
        results,
        key=results.get
    )

    print(
        "\n가장 유사한 화풍:",
        best_style
    )
