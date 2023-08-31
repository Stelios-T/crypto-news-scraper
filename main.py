from bs4 import BeautifulSoup
import aiohttp
import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

base_url = "https://cointelegraph.com"
tags_url = f"{base_url}/tags/markets"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
]

last_article_date = None
old_link = None

async def fetch_url(session, url):
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def check_and_print_new_articles():
    global last_article_date
    global old_link
    
    async with aiohttp.ClientSession() as session:
        try:
            html_content = await fetch_url(session, tags_url)
            
            soup = BeautifulSoup(html_content, 'html.parser')
            articles = soup.find_all('div', class_='post-card-inline__content')

            if not articles:
                logging.info("No articles found.")
                return

            for article in articles:
                link_element = article.find('a', class_='post-card-inline__title-link')
                if link_element and 'href' in link_element.attrs:
                    link = base_url + link_element['href']
                    if old_link != link:
                        old_link = link
                        print(link, flush=True)
                    # You can perform further processing or scraping on the new article
                    return

        except aiohttp.ClientError as client_error:
            logging.error('A client error occurred:', client_error)
        except Exception as e:
            logging.error('An error occurred:', e)

async def main():
    while True:
        await check_and_print_new_articles()
        await asyncio.sleep(600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
