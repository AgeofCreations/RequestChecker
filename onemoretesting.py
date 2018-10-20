
"""
URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()
"""
# We can use a with statement to ensure threads are cleaned up promptly
"""
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
"""

            # def loop(self):
            #    loop = asyncio.get_event_loop()
            #   tasks = [loop.create_task(self.load_url())]
            #  wait_tasks = asyncio.wait(tasks)
            # loop.run_until_complete(wait_tasks)
            # loop.close()

           # class MyAsyncCheckUrls(QThread):
            #    about_check_url = pyqtSignal(str)  # Проверка ответов
             #   good_requested_url = pyqtSignal(str)  # Запись хороших ответов
              #  bad_requested_url = pyqtSignal(str)  # Запись плохих ответов
               # status_bar_info = pyqtSignal(int)  # Контроль прогресс-бара

                #def __init__(self, urls):
                #    super().__init__()
                 #   self.urls = urls

import aiohttp
import asyncio
async def pizdec():

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.github.com/events') as resp:
            print(resp.status)
            print(await resp.text())



