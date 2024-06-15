from bs4 import BeautifulSoup
import requests
import csv


def populate(book_name):
    HEADERS = ({'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                               'Accept-Language': 'en-US, en;q=0.5'})
    searchurl = requests.get("https://www.goodreads.com/search?q=" + book_name.replace(" ", "+"), headers=HEADERS)
    soup = BeautifulSoup(searchurl.content, "lxml")
    first_result = soup.find('a', class_='bookTitle')
    book_url = "https://www.goodreads.com" + first_result['href']

    htmldata = requests.get(book_url).text
    initsoup = BeautifulSoup(htmldata,"lxml")
    ratingsstats = initsoup.find('div',class_="RatingStatistics__meta")
    averagerating = initsoup.find('div',class_='RatingStatistics__rating')
    ratings = int(ratingsstats.text.split()[0].replace(',',''))
    avgrating = float(averagerating.text)
    ratingscount = int(ratings)
    popularityquotient = avgrating*ratingscount
    return avgrating,popularityquotient,book_url

filedata = []
with open("main.csv") as file:
    reader = csv.DictReader(file)
    for var in reader:
        filedata.append(var)

with open("ratings.csv","w") as file:
    writer = csv.DictWriter(file,["Book Name","Author","Rating","Popularity Quotient","Link"])
    writer.writeheader()
    for var in filedata:
        rating,popquo, link = populate(var['title'])
        print("Done !")
        writer.writerow({"Book Name":var['title'],"Author":var['author'],"Popularity Quotient":popquo,"Rating":rating,"Link":link})
