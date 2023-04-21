# import requests and BeautifulSoup libraries
import requests
from bs4 import BeautifulSoup
import time
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


MAX_COST_WEEKLY = 120
start_time = time.time()
#Load variables
url = os.getenv("url")



def function():
    counter = 0
    for location, domain in domain_dict.items():
        with open(f"./data/{datetime.datetime.now().strftime('%d-%m-%Y')}_{MAX_COST_WEEKLY}.txt", "a") as f:
            f.write("-" * 100)
            f.write(f"\nPlaces found at {location} under ${MAX_COST_WEEKLY}\n")
            f.write(f"Time logged: {time.strftime('%d/%m/%Y %H:%M', time.localtime())}\n")


        # make a GET request to the URL and store the response
        curr_link = url + domain
        # parse the response content as HTML using BeautifulSoup
        response = requests.get(curr_link)
        next_page_bool = True

        # check if the response status code is 200 (OK)
        if response.status_code == 200:
            while next_page_bool: # while there is a next page
                soup = BeautifulSoup(response.content, "html.parser")
                results = soup.find("div", {"class": "styles__searchResults___1EbiP"})
                results = results.find("div", {"class": "styles__listings___4DNLo"})
                results = results.findAll("div", {"class": "styles__listingTileBox___2r9Cb"})
                # print(results)
                for div in results:
                    if div.find("div", {"class": "styles__listingTile___2OrNd styles__basic___1wkWM"}) == None:
                        nextdiv = div.find("div", {"class": "styles__listingTile___2OrNd styles__premium___1ms0b"})
                    else:
                        nextdiv = div.find("div", {"class": "styles__listingTile___2OrNd styles__basic___1wkWM"}) 
                    price = nextdiv.find("p", {"class": "styles__price___3Jhqs"}).text.split()[0].strip("$")
                    # print("hello")
                    price = int(price) if "-" not in price else int(price.split("-")[-1])

                    # FILTER
                    if price < MAX_COST_WEEKLY:
                        link = nextdiv.find("a", {"aria-label": "Flatmates listing"})['href']
                        link = url+link
                        # print(link)
                        with open(f"./data/{datetime.datetime.now().strftime('%d-%m-%Y')}_{MAX_COST_WEEKLY}.txt", "a") as f:
                            f.write(f"${price} \t {link}\n")
                        
                    counter += 1
                    # print(counter, price)
                    
                    # break


                if BeautifulSoup(response.content, "html.parser").find("a", {"aria-label": "Go to next page"}) == None:
                    next_page_bool = False
                    break
                # go to next link
                nextdomain = BeautifulSoup(response.content, "html.parser").find("a", {"aria-label": "Go to next page"})['href']
                response = url + nextdomain
                response = requests.get(response)
                # print(response)
                        
            

        else:
            # handle the error if the response status code is not 200
            print(f"Error: {response.status_code}")

    print(f"{counter} accommodations searched in {(time.time() - start_time):.2f} seconds")
        # break ## comment to run through both domains

if __name__ == "__main__":
    function()