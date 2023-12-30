# Wiki Art Genre Scraper
A re-implementation of the genre-scraper Robbie Barrat included in [art-DCGAN](https://github.com/robbiebarrat/art-DCGAN/tree/master). 
Wikiart has since updated their website so that images are dynamically loaded. This repo uses selenium to gather links to individual artworks and requests to download the images. 

## Instructions
`pip install -r requirements.txt `

Set `pages` on line 27 to the number of pages you want to scrape. 
There are 60 images per page, and the max number of pages is also 60. 

Change `genre-to-scrape` on line 27 to any one of the genre names commented below. 

Run using `python3 genre-scraper.py`. 

### Coming soon
- Progress bar for monitoring downloader's progress
- Command-line arguments for setting genre, style and output dir