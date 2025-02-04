# lib/extract_img.py
import os
import requests
import asyncio  # 추가
from requests_html import HTMLSession
from urllib.parse import urljoin

def extract_episode_images(episode_url, save_dir="images", timeout=20):
    """
    주어진 에피소드 URL에서 'id="toon_img"' div 내의 이미지를 추출하고 저장합니다.
    
    Parameters:
        episode_url (str): 에피소드 페이지의 URL
        save_dir (str): 이미지를 저장할 폴더 (기본값: "images")
        timeout (int): JavaScript 렌더링 대기 시간 (초)
        
    Returns:
        list: 다운로드한 이미지 파일의 경로 리스트
    """
    # 현재 스레드에 이벤트 루프가 없으면 새 이벤트 루프를 생성해서 설정합니다.
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    session = HTMLSession()
    response = session.get(episode_url)
    
    # JavaScript 렌더링 (필요시 timeout 값을 조절)
    response.html.render(timeout=timeout)
    
    # id가 'toon_img'인 div 찾기
    toon_img_div = response.html.find('div#toon_img', first=True)
    if not toon_img_div:
        print(f"'{episode_url}' 에서 id='toon_img'인 div를 찾지 못했습니다.")
        return []
    
    # div 내의 모든 <img> 태그의 src 추출
    img_elements = toon_img_div.find('img')
    image_urls = [urljoin(episode_url, img.attrs.get('src', ''))
                  for img in img_elements if img.attrs.get('src')]
    
    if not image_urls:
        print(f"'{episode_url}' 에서 이미지 태그를 찾지 못했습니다.")
        return []
    
    os.makedirs(save_dir, exist_ok=True)
    downloaded_images = []
    for idx, img_url in enumerate(image_urls, start=1):
        try:
            img_data = requests.get(img_url).content
            filename = os.path.join(save_dir, f"image_{idx}.jpg")
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"이미지 {idx} 저장 완료: {filename}")
            downloaded_images.append(filename)
        except Exception as e:
            print(f"이미지 {idx} 저장 실패: {img_url}\n에러: {e}")
    return downloaded_images