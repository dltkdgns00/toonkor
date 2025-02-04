# lib/extract_links.py
from requests_html import HTMLSession
from bs4 import BeautifulSoup

def get_episode_links(main_url, base_url, sleep=10, timeout=30, webtoon_name_to_remove=None):
    """
    메인 페이지에서 에피소드 제목과 해당 링크를 추출합니다.
    
    Parameters:
        main_url (str): 메인 페이지 URL
        base_url (str): 웹툰의 base URL
        sleep (int): render() 시 대기 시간
        timeout (int): render()의 최대 대기 시간
        webtoon_name_to_remove (str, optional): 에피소드 제목에서 폴더명용으로 제거할 웹툰 이름
        
    Returns:
        list of tuples: 각 튜플은 (폴더용 제목, full_url) 형태입니다.
                         - full_url은 원본 제목을 기반으로 띄어쓰기를 '_'로 치환하여 구성합니다.
                         - 폴더용 제목은 옵션에 따라 웹툰 이름이 제거된 제목입니다.
    """
    session = HTMLSession()
    response = session.get(main_url)
    response.html.render(sleep=sleep, timeout=timeout)
    
    soup = BeautifulSoup(response.html.html, 'html.parser')
    # 에피소드 제목이 들어있는 td 요소 선택
    episode_elements = soup.select("td.content__title")
    
    episodes = []
    for td in episode_elements:
        original_title = td.get_text(strip=True)
        # 폴더용 제목: 옵션에 따라 웹툰 이름 제거
        folder_title = original_title
        if webtoon_name_to_remove and folder_title.startswith(webtoon_name_to_remove):
            folder_title = folder_title[len(webtoon_name_to_remove):].strip()
        # URL 구성용 제목: 원본 제목에서 띄어쓰기를 '_'로 치환 (웹툰 이름은 그대로 유지)
        url_title = original_title.replace(" ", "_")
        full_url = f"{base_url}/{url_title}.html"
        episodes.append((folder_title, full_url))
    return episodes