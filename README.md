# IMPRINT

**IMPRINT — 이미지 기반 애니메이션 화풍 유사도 분석 웹 애플리케이션**

IMPRINT는 이미지의 색상 분포, 시각적·의미적 특징, 국소 질감 패턴을 분석하여 입력 이미지와 기준 데이터셋 사이의 화풍 유사도를 비교하는 웹 애플리케이션입니다.

Disney, Ghibli, Simpsons의 세 가지 애니메이션 화풍을 대상으로 분석하며, 각 범주별 유사도 점수와 가장 높은 점수를 얻은 화풍을 제공합니다.

**웹사이트:** https://imprint-production-694a.up.railway.app/

## 1. 프로젝트 소개

생성형 AI를 활용한 이미지 제작과 화풍 변환이 확산되면서, 생성 이미지와 기존 창작물 사이의 시각적 관계를 정량적으로 분석할 필요성이 커지고 있습니다.

본 프로젝트는 세 가지 이미지 분석 기법을 결합하여 입력 이미지가 기준 이미지 데이터셋과 어느 정도 시각적으로 유사한지 비교하는 것을 목적으로 합니다.

분석 대상 화풍은 다음과 같습니다.

- Disney
- Ghibli
- Simpsons

## 2. 이미지 분석 방법

IMPRINT는 세 가지 분석 기법을 사용합니다.

| 분석 기법 | 설명 | 가중치 |
|---|---|---|
| Color Histogram | RGB 색상 분포 비교 | 60% |
| CLIP | 이미지 임베딩을 이용한 시각적·의미적 유사도 비교 | 30% |
| LBP (Local Binary Patterns) | 이미지의 국소 질감 패턴 비교 | 10% |

각 기법에서 산출한 점수를 가중 결합하여 화풍별 종합 유사도 점수를 계산합니다.

**종합 점수 = 색상 유사도 × 0.6 + CLIP 유사도 × 0.3 + LBP 유사도 × 0.1**

각 점수는 프로그램의 계산 방식에 따라 동일한 백분율 척도로 환산하여 결합합니다.

가장 높은 종합 점수를 얻은 화풍을 최종 결과로 제시하며, 개별 분석 기법의 결과도 함께 확인할 수 있습니다.

본 프로그램의 유사도 점수는 기준 데이터셋과의 시각적 근접성을 나타내는 지표이며, 특정 화풍에 속할 확률을 의미하지 않습니다.

## 3. 주요 기능

- JPG, JPEG, PNG 이미지 업로드
- Disney, Ghibli, Simpsons 화풍별 유사도 분석
- Color Histogram, CLIP, LBP 분석 결과 제공
- 가중치를 적용한 종합 유사도 점수 산출
- 가장 유사한 화풍 표시
- 웹 브라우저 기반 분석 결과 시각화

## 4. 개발 및 실행 환경

- Python 3.13
- Flask
- PyTorch (CPU)
- OpenCLIP
- OpenCV
- scikit-image
- Pillow
- Gunicorn (배포 환경)

로컬 개발 환경은 Windows를 기준으로 하며, 웹 애플리케이션은 Railway를 통해 배포하였습니다.

## 5. 프로젝트 설치

### 5.1 저장소 다운로드

GitHub 저장소를 Clone하거나 ZIP 파일로 다운로드합니다.

```powershell
git clone https://github.com/minaaa101/IMPRINT.git
cd IMPRINT
```

### 5.2 가상환경 생성 및 활성화

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5.3 라이브러리 설치

```powershell
python -m pip install -r requirements.txt
```

설치 상태를 확인합니다.

```powershell
python -m pip check
```

## 6. 환경변수 설정

프로젝트 최상위 폴더에 `.env` 파일을 생성합니다.

```dotenv
SECRET_KEY=your_random_secret_key
```

비밀키는 다음 명령어로 생성할 수 있습니다.

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

생성한 값을 `SECRET_KEY`에 설정합니다.

보안을 위해 `.env` 파일은 GitHub에 업로드하지 않습니다.

## 7. CLIP 임베딩 캐시

IMPRINT는 기준 데이터셋 이미지의 CLIP 임베딩을 미리 계산하여 저장하는 캐시 방식을 사용합니다.

이를 통해 이미지 분석을 실행할 때마다 기준 데이터셋 전체의 CLIP 임베딩을 다시 계산할 필요가 없습니다.

캐시 파일은 다음 위치에 저장됩니다.

```text
models/
└── clip_embeddings/
    ├── disney.pt
    ├── ghibli.pt
    └── simpsons.pt
```

저장소에 캐시 파일이 포함되어 있다면 별도의 캐시 생성 과정 없이 사용할 수 있습니다.

기준 데이터셋을 변경하거나 캐시를 다시 생성해야 하는 경우 다음 명령어를 실행합니다.

```powershell
python -m src.build_clip_cache
```

CLIP 모델 가중치가 로컬에 저장되어 있지 않다면 최초 실행 시 인터넷 연결이 필요할 수 있습니다.

## 8. 웹 애플리케이션 실행

### 8.1 온라인 실행

다음 주소에 접속하여 프로그램을 사용할 수 있습니다.

https://imprint-production-694a.up.railway.app/

온라인 서비스는 Railway 서버의 운영 상태에 따라 접속 가능 여부가 달라질 수 있습니다.

### 8.2 로컬 실행

프로젝트 최상위 폴더에서 다음 명령어를 실행합니다.

```powershell
python app.py
```

웹 브라우저에서 다음 주소로 접속합니다.

http://127.0.0.1:5000

## 9. 사용 방법

1. Home 화면에서 JPG, JPEG 또는 PNG 이미지를 업로드합니다.
2. Analysis 화면에서 이미지 분석을 실행합니다.
3. Result 화면에서 가장 유사한 화풍과 종합 유사도 점수를 확인합니다.
4. Color Histogram, CLIP, LBP의 개별 분석 결과를 확인합니다.
5. 다른 이미지를 업로드하여 다시 분석할 수 있습니다.

업로드 가능한 이미지의 최대 크기는 10MB입니다.

## 10. 학술제 시연

학술제에서는 Railway에 배포된 웹사이트를 통해 IMPRINT를 시연합니다.

온라인 서비스에 문제가 발생하는 상황에 대비하여 로컬 실행 환경을 예비 수단으로 준비할 수 있습니다.

로컬 시연을 위해 다음 사항을 확인합니다.

- Python 및 필수 라이브러리 설치
- CLIP 모델 가중치 준비
- CLIP 임베딩 캐시 파일 확인
- 기준 이미지 데이터셋 준비
- 이미지 업로드 및 분석 결과 출력 테스트

인터넷 연결 없이 실행하려면 필요한 모델 파일을 사전에 준비하고 오프라인 환경에서 별도로 검증해야 합니다.

## 11. 연구의 한계 및 주의사항

- 본 프로그램은 입력 이미지와 기준 데이터셋 사이의 시각적 유사도를 비교합니다.
- 유사도 점수는 특정 제작사나 원작자가 이미지를 제작했을 확률을 의미하지 않습니다.
- 분석 결과만으로 저작권 침해 여부를 판단할 수
