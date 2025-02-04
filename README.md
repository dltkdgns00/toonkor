# ToonKor Webtoon Image Scraper

이 프로젝트는 툰코 웹사이트에서 웹툰 에피소드별 이미지를 자동으로 추출하여 로컬에 저장하는 파이썬 스크립트입니다.

## 기능

- **웹툰 메인 페이지에서 에피소드 제목 및 링크 추출**  
  메인 페이지에서 각 에피소드 제목을 추출하고, 띄어쓰기를 언더스코어("\_")로 치환하여 에피소드 페이지 URL을 구성합니다.
- **에피소드 페이지에서 이미지 추출 및 다운로드**  
  각 에피소드 페이지에 포함된 `id="toon_img"`인 div 내부의 이미지를 추출하여,  
  `downloads/<웹툰 이름>/<에피소드 폴더>` 구조로 저장합니다.
- **환경변수(.env)로 설정 관리**  
  BASE_URL, WEBTOON_NAME 등 주요 설정 값들을 `.env` 파일에서 관리하여 쉽게 변경할 수 있습니다.
- **병렬 처리 (ProcessPoolExecutor 사용)**  
  에피소드별 이미지 추출 작업을 병렬로 처리하여 속도를 향상시킵니다.

## 폴더 구조

```
toonkor/
├── lib/
│ ├── extract_img.py        # 에피소드 페이지에서 이미지 추출 및 다운로드 함수
│ └── extract_links.py      # 메인 페이지에서 에피소드 제목 및 링크 추출 함수
├── downloads/                # 다운로드 받을 이미지가 저장될 폴더 (실행 시 자동 생성)
├── .env                      # 환경변수 파일 (BASE_URL, WEBTOON_NAME 등)
├── main.py                   # 메인 실행 스크립트
└── README.md                 # 프로젝트 개요 및 사용법
```

## 요구사항

- Python 3.6 이상
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Requests-HTML](https://github.com/psf/requests-html)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## 설치 방법

1. 이 레포지토리를 클론합니다.

   ```bash
   git clone https://github.com/dltkdgns00/toonkor.git
   cd toonkor
   ```

2. 가상 환경을 생성하고 활성화합니다.

   ```bash
   python3 -m venv venv
   source venv/bin/activate # macOS/Linux
   venv\Scripts\activate # Windows
   ```

3. 필요한 패키지를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```

   requirements.txt 파일이 없다면, 아래와 같이 직접 설치할 수 있습니다.

   ```bash
   pip install requests-html beautifulsoup4
   ```

4. 프로젝트 루트에 .env 파일을 생성하고, 아래 예시와 같이 설정합니다.

   ```.env
   BASE_URL=<툰코 baseUrl>
   WEBTOON_NAME=<웹툰 이름>
   ```

## 사용 방법

1. main.py 파일 내의 환경변수는 .env 파일에서 관리되므로, 필요한 설정(예: BASE_URL, WEBTOON_NAME)을 수정합니다.
2. 스크립트를 실행합니다.
   ```bash
   python main.py
   ```

## 참고 사항

- 렌더링 시간 조정
  페이지에 따라 JavaScript가 동적으로 데이터를 로드하므로,
  render() 함수 호출 시의 sleep 및 timeout 값은 필요에 따라 조정해야 합니다.
- 병렬 처리
  이미지 다운로드 작업은 ProcessPoolExecutor를 통해 병렬로 처리되며,
  동시에 여러 프로세스에서 작업을 수행하여 속도를 향상시킵니다.
- 에러 처리
  일부 에피소드 페이지에서 id="toon_img"를 찾지 못하거나 이미지 다운로드에 실패할 수 있습니다.
  해당 경우 로그 메시지를 통해 문제를 파악하고 수정하세요.

## 라이선스

MIT License
