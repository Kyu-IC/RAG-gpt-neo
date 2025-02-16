import wikipediaapi

def get_wiki_page(page_title, max_chars=2000):
    # สร้าง Wikipedia instance โดยกำหนดภาษาและ user_agent
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='MyGreenTeaBot/1.0 (https://example.com)')
    
    # ดึงหน้าที่ต้องการ
    page = wiki_wiki.page(page_title)
    
    if page.exists():
        return page.text[:max_chars]
    else:
        raise ValueError("Page does not exist")