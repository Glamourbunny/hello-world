import requests
from bs4 import BeautifulSoup

# 定义函数获取页面内容并存储到文件
def get_content(url):
# 获取页面内容
    # url = "https://youzhiyouxing.cn/materials/659"
    response = requests.get(url)
    html_content = response.content

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取标题和内容
    title = soup.find('title').text.strip()
    sections = soup.find_all(['h2', 'p'])

    # 将提取的内容写入文本文件
    with open('content.txt', 'a', encoding='utf-8') as f:
        f.write(f"Title: {title}\n\n")

        current_heading = None
        for section in sections:
            if section.name == 'h2':
                current_heading = section.text.strip()
                f.write(f"\nSubTitle:{current_heading}\n")
            elif section.name == 'p':
                if current_heading:
                    f.write(f"{section.text.strip()}\n")

    print(url + "Content has been extracted and saved to content.txt")


# 定义函数获取页面内容
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch page content.")
        return None

# 爬取并提取链接
def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    materials_links = []
    for link in links:
        href = link['href']
        if 'materials' in href:
            materials_links.append(href)
    return materials_links

# 获取链接中的内容并保存到文本文件
def save_content_to_file(url, filename):
    content = get_page_content(url)
    print(content)
    if content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content.decode('utf-8'))
        print(f"Content saved to {filename}")
    else:
        print("Failed to save content to file.")

# 主程序
if __name__ == "__main__":
    base_url = "https://youzhiyouxing.cn"
    topic_pages = ["/topics/ezone/nodes/2", "/topics/ezone/nodes/14", "/topics/ezone/nodes/18"]

    for topic_page in topic_pages:
            url = base_url + topic_page
            page_content = get_page_content(url)
            if page_content:
                links = extract_links(page_content)
                print(links)
                for link in links:
                    full_link = base_url + link
                    get_content(full_link)


