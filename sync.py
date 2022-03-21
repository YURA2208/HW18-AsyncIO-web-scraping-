import asyncio
import aiohttp
from bs4 import BeautifulSoup


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Connection": "keep-alive"
}

async def get_site_page(session, url):
    try:
        async with session.get(url) as r:
            return await r.text()
    except aiohttp.ClientConnectorError:
        print(f"Unable to access site - {url}")
    except aiohttp.ClientResponseError:
        print(f"404 Not Found - {url}")


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_site_page(session, url))
        tasks.append(task)
    return await asyncio.gather(*tasks)


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data


def parse(results):
    for result in results:
        if result:
            bs = BeautifulSoup(result["html"], "html.parser")
            title = bs.find("title")
            if title:
                print(f"{result['url']} - {title.text.strip()}")


if __name__ == "__main__":
    with open("news_sites.txt") as file:
        content = file.read().split("\n")
    all_urls = content

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(all_urls))

    parse(html_results)

