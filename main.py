from bs4 import BeautifulSoup
import requests
import shutil
import time
import os
import logging

logging.basicConfig(filename='out.log', encoding='utf-8', level=logging.INFO)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


# Only Modify this
# url = 'https://www.slideshare.net/MushtaqAhmed7/neuromuscular-blocking-agents-reversal-in-anesthesia'

# Returns Array of picture urls to download
def get_picture_urls(url, class_name):
    # Requesting page
    req = requests.get(url, headers)

    # Creating the soup ;p
    soup = BeautifulSoup(req.content, 'html.parser')

    # navigating to the slides div#slide-container>img
    main_ppt_div = soup.find("div", {"id": class_name})
    img_nodes = list(main_ppt_div.findAll("img"))
    logging.info("Total Slides" + str(len(img_nodes)))
    # print("Main PPT", img_nodes[0]['srcset'].split(',')[-1].split()[0])

    # Iterate Thru each picture node, and get the best looking image
    picture_urls = []

    for img in img_nodes:
        src_attr = img['srcset'].split(',')[-1].split()[0]
        # print(i , " : ", src_attr)
        picture_urls.append(src_attr)

    return picture_urls


def download_picture_urls(url_array, download_folder):
    # iterating
    slide = 1
    for pic_url in url_array:
        # Set up the image URL and filename
        time.sleep(1)
        filename = "Slide_" + str(slide) + '.png'

        # Checking Sub Dir
        sub_folder = os.path.join(os.getcwd(), download_folder)
        sub_folder_exists = os.path.exists(sub_folder)
        if not sub_folder_exists:
            logging.info('Subfolder doesnt exist, so creating: ' + download_folder)
            os.makedirs(sub_folder)

        file_path = os.path.join(os.getcwd(), download_folder, filename)

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(pic_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Slide downloaded', filename)
        else:
            logging.error('Slide Failed to download ' + filename + ' URL: ' + pic_url)

        slide += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Parse the page and fetch all urls

    url = input('Enter page URL: ')
    download_folder = input('Enter Download Folder name: ')

    logging.info('########## START ##########')
    logging.info('Starting URL: ' + url)
    url_array = get_picture_urls(url, 'slide-container')
    # print('URL: ', len(url_array))

    # download all urls
    download_picture_urls(url_array, download_folder)
    logging.info('########## END ##########')
