## re-building Robbie Barrat's wiki art genre scraper since it seems to not be working

# For a list of stuff you can scrape - go to https://www.wikiart.org/en/paintings-by-genre/ and look at the categories there. Usually you'll need about 1000 images for a good GAN.

import os
import requests
import time
from time import perf_counter


from bs4 import BeautifulSoup

from multiprocessing import cpu_count, Pool

## import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# how many pages you want to scrape
# maximum is currently 60
pages = 2


# Change this value! 

genre_to_scrape = "portrait"

# genre_to_scrape can be any one of the below values.
"""
portrait
landscape
genre-painting
abstract
religious-painting
cityscape
sketch-and-study
figurative
illustration
still-life
design
nude-painting-nu
mythological-painting
marina
animal-painting
flower-painting
self-portrait
installation
photo
allegorical-painting
history-painting
"""
# at this point - there might not be enough images for good results - but if you'd like to mix and match the images you're training and pull from multiple genres, go ahead
"""
interior
literary-painting
poster
caricature
battle-painting
wildlife-painting
cloudscape
miniature
veduta
yakusha-e
calligraphy
graffiti
tessellation
capriccio
advertisement
bird-and-flower-painting
performance
bijinga
pastorale
trompe-loeil
vanitas
shan-shui
tapestry
mosaic
quadratura
panorama
architecture
"""



driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install())) 

def get_painting_links(count, genre=genre_to_scrape):
    """
    loads results page of paintings by genre
    and retruns a list of links to each individual painting
    """

    try:
        url = "https://www.wikiart.org/en/paintings-by-genre/"+ genre+ "/" + str(count)
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, features="html.parser")

        links = [tag['href'] for tag in soup.css.iselect(".artwork-name")]
        return(links)
    
    except Exception as e:
        print(e)
        pass


def get_painting_src(link):
    """
    Takes the link to an individual artwork as an argument
    and returns the src of its photo
    """
    try: 
        r = requests.get(f"https://www.wikiart.org{link}")
        soup = (BeautifulSoup(r.text, features="html.parser"))
        print(f"{r.status_code} -- {soup.css.select('img')[1]['src']}")
        downloader(soup.css.select('img')[1]['src'])
        # return soup.css.select('img')[1]['src']
    
    except Exception as e:
        print(f"{e} -- on image {link}")
    
def downloader(link, genre=genre_to_scrape, output_dir=None):

    output_dir = output_dir or f"./{genre}/images"

    filename = link.split('/')[-1]
    savepath = f"{output_dir}/{filename}"
    try:
        time.sleep(0.2)
        r = requests.get(link).content
        with open(savepath, 'wb') as file:
            file.write(r)
    except Exception as e: 
        print(f"failed downloading {link} - {e}")


def main(genre=genre_to_scrape):

    start = perf_counter()

    old_links = []
    links = []

     # create filepaths for downloading images
    if not os.path.exists("./" + genre_to_scrape):
        os.mkdir(genre_to_scrape)

    if not os.path.exists("./" + genre_to_scrape + "/images"):
        os.mkdir(genre_to_scrape + "/images/")

    
    # For pages = 60, adding more that 10 processes has diminishing returns
    if (cpu_count() >= 10):
        num_processes = 10
    else:
        num_processes = cpu_count()-1

    
    pool = Pool(num_processes)
    results = pool.map(get_painting_links, range(1, pages+1))
    pool.close()
    pool.join()

    # add all results into one list
    for list in results:
        old_links.extend(list)

    # filter out repetitions
    for item in old_links:
        if item not in links:
            links.append(item)


    pool = Pool(cpu_count()-1)
    print("Downloading inidvidual artworks")
    results2 = pool.map(get_painting_src, links)
    pool.close()
    pool.join()
    print("POOL CLOSED")

    finish = perf_counter()

    print(f"Found {len(links)} in {round(finish-start, 2)} secs")

   

if __name__ == "__main__":
    main()