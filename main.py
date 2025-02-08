import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup


async def get_main_news(url: str, src: list, name: str):

    timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as respond:
                respond.raise_for_status()
                site = await respond.text()
                soup = BeautifulSoup(site, 'lxml')
                print(f"{name}'s news contains following information")
                for i in src:
                    news = soup.find_all(i[0], class_=i[1])
                    if news:
                        for j in news:
                            if j.text:
                                print(f'   -->   {j.text}')
                    else:
                        print(f'Headline not found on {url}')
                    print()

        except aiohttp.ClientError as e:
            print(f"Request failed for {url}: {e}")
        except asyncio.TimeoutError:
            print(f"Request timed out: {url}")


async def main():
    bbs_src = [['h2', 'sc-8ea7699c-3 kwWByH'], ['h2', "sc-8ea7699c-3 dhclWg"]]
    cnn_src = [['h2', 'container__title_url-text container_lead-package__title_url-text'], ['div', "container__text container_lead-package__text"]]

    ex1 = asyncio.create_task(get_main_news('https://www.bbc.com/news', bbs_src, 'BBS'))
    ex2 = asyncio.create_task(get_main_news('https://edition.cnn.com/', cnn_src, 'CNN'))

    await asyncio.gather(ex1, ex2)

start = time.time()
asyncio.run(main())
print(f"Execution time - {str(time.time() - start)[:5]} sec.")
