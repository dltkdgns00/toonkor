import os
import concurrent.futures
from lib.extract_links import get_episode_links
from lib.extract_img import extract_episode_images

# 설정 변수
BASE_URL = os.getenv("BASE_URL")
WEBTOON_NAME = os.getenv("WEBTOON_NAME")
DOWNLOADS_ROOT = "downloads"       # 최상위 다운로드 폴더


def main():
    # 웹툰 폴더 생성: downloads/<웹툰 이름>
    webtoon_folder = os.path.join(DOWNLOADS_ROOT, WEBTOON_NAME)
    os.makedirs(webtoon_folder, exist_ok=True)
    
    # 메인 페이지 URL 구성 (예: "<툰코 baseUrl>/<웹툰 이름>")
    main_url = f"{BASE_URL}/{WEBTOON_NAME.replace(' ', '-')}"
    
    # 에피소드 링크 추출 (폴더용 제목은 옵션에 따라 웹툰 이름 제거됨, URL은 원본 제목 기반)
    episodes = get_episode_links(main_url, BASE_URL, webtoon_name_to_remove=WEBTOON_NAME)
    
    print("에피소드 링크 리스트:")
    for title, link in episodes:
        print(f"폴더명: {title} / URL: {link}")
    
    # ProcessPoolExecutor를 사용해 병렬로 이미지 추출 실행
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        futures = []
        for folder_title, link in episodes:
            # 각 에피소드별 폴더는 폴더용 제목(띄어쓰기는 그대로 유지)으로 생성
            episode_folder = os.path.join(webtoon_folder, folder_title)
            os.makedirs(episode_folder, exist_ok=True)
            print(f"\n이미지 추출 시작: {link} -> 저장 폴더: {episode_folder}")
            # 각 작업을 executor에 제출 (프로세스 병렬 처리)
            futures.append(executor.submit(extract_episode_images, link, episode_folder))
        
        # 모든 작업이 완료될 때까지 대기 및 결과 처리
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                # 각 작업의 결과(다운로드된 이미지 파일 목록)를 사용할 수 있습니다.
            except Exception as exc:
                print(f"에피소드 처리 중 에러 발생: {exc}")

if __name__ == '__main__':
    main()