import cv2
import numpy as np

from src.preprocessing import preprocess_image
from src.color.colorhistogram import compare_with_dataset


input_image = preprocess_image(
    "test_images/쥐.jpg"
)


# 화풍별 데이터셋과 비교
disney_score = compare_with_dataset(
    input_image,
    "data/disney"
)

ghibli_score = compare_with_dataset(
    input_image,
    "data/ghibli"
)

simpsons_score = compare_with_dataset(
    input_image,
    "data/simpsons"
)


print(f"Disney Color Similarity: {disney_score:.2f}")
print(f"Ghibli Color Similarity: {ghibli_score:.2f}")
print(f"Simpsons Color Similarity: {simpsons_score:.2f}")