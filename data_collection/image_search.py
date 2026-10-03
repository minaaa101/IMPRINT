import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("SERPAPI_KEY가 설정되지 않았습니다.")


SEARCH_QUERIES = {
    "ghibli": [
        "Ghibli movie still",
        "Studio Ghibli animation scene",
        "Ghibli film scene",
    ],
    "disney": [
        "Disney animation movie still",
        "Disney animated film scene",
        "Disney cartoon movie scene",
    ],
    "simpsons": [
        "The Simpsons episode still",
        "The Simpsons animation scene",
        "Simpsons cartoon scene",
    ],
}


def search_images(query, num_results=20):
    params = {
        "engine": "google_images",
        "q": query,
        "api_key": API_KEY,
        "ijn": 0,
    }

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("images_results", [])[:num_results]


def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)

            return True

    except requests.RequestException:
        pass

    return False


if __name__ == "__main__":

    for style, queries in SEARCH_QUERIES.items():

        save_dir = os.path.join("dataset", style)
        os.makedirs(save_dir, exist_ok=True)

        image_count = 0

        print(f"\n===== {style.upper()} =====")

        for query in queries:

            print(f"검색 중: {query}")

            results = search_images(query, num_results=20)

            for result in results:

                image_url = result.get("original")

                if not image_url:
                    continue

                filename = f"{style}_{image_count:04d}.jpg"
                save_path = os.path.join(save_dir, filename)

                print(f"다운로드: {filename}")

                if download_image(image_url, save_path):
                    image_count += 1

        print(f"{style}: 총 {image_count}개 다운로드 완료")