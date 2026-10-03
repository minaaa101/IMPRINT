import os
import cv2

def validate_image_file(image_path):
    """
    지원하는 이미지 파일 형식인지 확인하는 함수.

    Args:
        image_path (str): 이미지 파일 경로

    Raises:
        ValueError: 지원하지 않는 파일 형식일 경우
    """
    allowed_extensions = {".jpg", ".jpeg", ".png"}

    _, extension = os.path.splitext(image_path)
    extension = extension.lower()

    if extension not in allowed_extensions:
        raise ValueError(
            f"지원하지 않는 이미지 형식입니다: {extension} "
            f"(지원 형식: JPG, JPEG, PNG)"
        )
    
def load_image(image_path):
    """
    이미지 파일을 OpenCV로 불러오는 함수.

    Args:
        image_path (str): 이미지 파일 경로
    
    Returns:
        numpy.ndarray: 불러온 이미지
    """
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"이미지 파일을 찾을 수 없습니다: {image_path}")
    
    return image

def resize_image(image, size=(224, 224)):
    """
    이미지를 지정된 크기로 변경하는 함수.

    Args:
        image (numpy.ndarray): 원본 이미지
        size (tuple): (width, height) 형태의 목표 크기

    Returns:
        numpy.ndarray: 리사이즈된 이미지
    """
    resized_image = cv2.resize(image, size)

    return resized_image

def convert_to_rgb(image):
    """
    OpenCV의 BGR 이미지를 RGB 형식으로 변환하는 함수.

    Args:
        image (numpy.ndarray): BGR 형식의 이미지

    Returns:
        numpy.ndarray: RGB 형식의 이미지
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return rgb_image

def preprocess_image(image_path, size=(224, 224)):
    """
    이미지 전처리를 수행하는 함수.

    1. 파일 형식 검사
    2. 이미지 불러오기
    3. 이미지 크기 변경
    4. BGR → RGB 변환

    Args:
        image_path (str): 이미지 파일 경로
        size (tuple): (width, height) 형태의 목표 크기

    Returns:
        numpy.ndarray: 전처리가 완료된 RGB 이미지
    """

    validate_image_file(image_path)

    image = load_image(image_path)
    image = resize_image(image, size)
    image = convert_to_rgb(image)

    return image

if __name__ == "__main__":
    image = preprocess_image("nothing.jpg")

    print("전처리 완료!")
    print("이미지 크기:", image.shape)
    print("데이터 타입:", image.dtype)