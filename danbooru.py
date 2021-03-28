
import re
import requests
from bs4 import BeautifulSoup 
import os
from requests.exceptions import HTTPError
import time
from functools import wraps

'''
to use the downloader
    - change title and url
    -
'''

title = 'sweat'
number_of_images = 5
# endpoint = '&tags=kamurai_%28armor%29'

endpoint = '&tags=sweat'

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        with open(log_name, 'a') as f:
            f.write("@timefn:" + fn.__name__ + " took " + str(t2 - t1) + " seconds \n")
        print ("@timefn:" + fn.__name__ + " took " + str(t2 - t1) + " seconds")
        return result
    return measure_time

def create_log_file(name, page_url=False, img_url=False):
    idx = 0 

    prefix = 'logs'

    if page_url:
        postfix = 'page_url'
    elif img_url:
        postfix = 'img_url'
    else:
        postfix = 'time'
        
    
    log_file_base = f'_{prefix}_{idx}_{name}_{postfix}_'
    log_file_name = f'{log_file_base}.txt'

    file_exits = os.path.isfile(log_file_name)
    while file_exits:
        idx += 1
        temp_base = f'_{prefix}_{idx}_{name}_{postfix}_' + '.txt'
        log_file_name = temp_base
        file_exits = os.path.isfile(temp_base)
    

    complete_log_file_name = log_file_name
    open(complete_log_file_name, 'x').close()
    
    return complete_log_file_name

@timefn
def get_urls_from_page(endpoint, page_num=1, end_page=1000):
   
   # <a class="paginator-next" rel="next" data-shortcut="d right" href="/posts?page=2&amp;tags=scenery" title="Shortcut is d or right"><i class="icon fas fa-chevron-right "></i></a>
    ext = 'page=8&tags=scenery'
    pages_left = True
    final = []
    counter = 0
    while pages_left: 
        #urls = f'https://danbooru.donmai.us/posts?page={page_num}&tags=scenery'
        #urls2 = f'https://danbooru.donmai.us/posts?page={page_num}&tags=mulan'
        if page_num == end_page:
            break
        time.sleep(1)
        base_url = 'https://danbooru.donmai.us/posts'
        get_url = base_url + f'?page={page_num}' +endpoint
        r = requests.get(get_url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        
        pattern = ' data-id="(\d+)"'
        for a in soup.find_all('article'):
            #print(a) 
            post_id = re.search(pattern, str(a))

            if post_id:
                val = post_id.group(1)
                generated_url = base_url + '/' +str(val)
                #print(generated_url)
                final.append(generated_url)
                counter += 1

        found = False
        for a in soup.find_all('a', {"class": "paginator-next"}):
            found = True

        if not found:
            pages_left = False
        
        print(f'fetching from page number: {page_num}')
        page_num += 1
        print(get_url)
        print('')

    print('\n\n')
    print(f'downloading images: {counter}')

    log_name = create_log_file(title, page_url=True)

    with open(log_name, 'a') as f:
        for url in final:
            f.write(f'{url}\n')

    return final

@timefn
def get_main_url(urls):

    final = []
    img_count = 0
    counter = len(urls)
    print(f'should be fetching {counter} images')
    for url in urls:
        print(f'getting from url: {url}')
        time.sleep(1)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for a in soup.find_all('li', {"id": "post-info-size"}):
            #pattern = 'https:\/\/danbooru.donmai.us\/data\/original\/.{2}\/.{2}\/[a-zA-z0-9]+.(?:jpg|png)'
            # pattern = 'https:\/\/(?:cdn|danbooru).donmai.us\/.+.(?:jpg|png)"'
            pattern = 'href="(https:\/\/(?:cdn|danbooru).donmai.us\/.+.(?:jpg|png))"'
            image_url  = re.search(pattern, str(a))

            if image_url:
                val = image_url.group(1)
                final.append(val)
                img_count += 1
    
    log_name = create_log_file(title, img_url=True)

    with open(log_name, 'a') as f:
        for url in final:
            f.write(f'{url}\n')

    return final, log_name, img_count

@timefn
def create_folder(title):
    title = title[:len(title)-1]
    try:
        os.makedirs(title)
        folder_name = title
    except FileExistsError:
        path = str(os.getcwd())
        download_version = str(len(
            [i for i in os.listdir(path) if os.path.isdir(i)]))
        os.makedirs(title + ' v' + download_version)
        folder_name = title + ' v' + download_version

    return folder_name

@timefn
def image_downloader(img_logs, img_count, folder_name):

    left, right = 0, img_count
    with open(img_logs) as f:
        img = f.readline().splitlines()
        while img:
            uncompleted = []
            left += 1
            try:
    
                left += 1
                # print(f'Downloading: {img}')
                print(f'{round((left/right)*100)}% Complete')
                res = requests.get(img[0], stream=True)
                res.raise_for_status()

                imageFile = open(os.path.join(
                    folder_name, os.path.basename(img[0])), 'wb')

                for pic in res.iter_content(300000000):
                    imageFile.write(pic)
                    imageFile.close()
            
            except requests.exceptions.HTTPError as err:
                print(err)
            finally:
                img = f.readline().splitlines()



log_name = create_log_file(title)
all_post_urls = get_urls_from_page(endpoint, 1, number_of_images)
final_urls, img_logs, img_count = get_main_url(all_post_urls)
folder_name = create_folder(title)



image_downloader(img_logs, img_count, folder_name)

