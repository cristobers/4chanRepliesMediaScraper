import sys, os, asyncio, aiofiles, aiohttp
from urllib.request import urlopen
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("usage: 4chanImageRipper.py <thread URL>")
    exit(1)

update_from_thread = False

async def grab_media(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(path, mode='wb')
                await f.write(await resp.read())
                await f.close()

async def parse_media_links(post_image, img_dir):
    for _, image in enumerate(post_image):
        try:
            href_element = image['href']
            thread_media = href_element.split('/')[-1]
            if update_from_thread:
                if thread_media in os.listdir(img_dir):
                    print(f"Already downloaded {thread_media}, skipping...")
                    continue
            print(f"Grabbing: {thread_media}")
            url = f"https://{href_element.split('//')[-1]}"
            directory_path = f"{img_dir}/{thread_media}"
            await grab_media(url, directory_path)
        except Exception as e:
            print(e)

def attempt_to_open_url():
    try:
        html = urlopen(sys.argv[1])
        return html
    except Exception as e:
        print(e)

async def main():
    html = attempt_to_open_url()
    bs4 = BeautifulSoup(html.read(), 'html.parser') 
    post_image = bs4.findAll("a", {"class":"fileThumb"})
    length = len(post_image)
    img_dir = sys.argv[1].split('/')[-1]

    print(f"making dir {img_dir}/ and checking {length} replies...")
    try:
        os.mkdir(img_dir)
    except FileExistsError:
        print(f"Folder already exists for this thread.")
        update_from_thread = True

    A, B = post_image[:length//2], post_image[length//2:]
    task_1 = asyncio.create_task(parse_media_links(A, img_dir))
    task_2 = asyncio.create_task(parse_media_links(B, img_dir))
    await asyncio.gather(task_1, task_2)
asyncio.run(main())