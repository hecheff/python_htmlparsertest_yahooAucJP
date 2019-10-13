#Experiment for parsing current values from user-generated-content found on website
#Generates CSV report of auction entries for bluetooth speakers (as sample) from Yahoo Auctions (Japanese)
#Uses BeautifulSoup library

from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup
import csv

filename = "productsList.csv"

#URL including search and display conditions.
#Change search output by replace this value with the URL of a set of search results
myUrl = 'https://auctions.yahoo.co.jp/search/search?p=bluetooth+%E3%82%B9%E3%83%94%E3%83%BC%E3%82%AB%E3%83%BC&auccat=23812&va=bluetooth+%E3%82%B9%E3%83%94%E3%83%BC%E3%82%AB%E3%83%BC&exflg=1&b=1&n=20&s1=score2&o1=d&rewrite_category=1'
#myUrl = 'https://www.newegg.com/global/jp-en/p/pl?d=Wireless+Speakers'

uClient = uReq(myUrl)			            #Set URL request 
page_html = uClient.read()		            #Declares contents of uClient action into variable
uClient.close()				                #Closes access to the file (no longer needed)

page_soup = soup(page_html, "html.parser")	#Parse page_html

#Extract all values. Max.20 (+3 for promoted items) results sorted by relevance/popularity
products = page_soup.findAll("div",{"class":"Product__detail"})

index = 1                       #Set index for labeling items below
errorTrigger_write = False      #Sets to true if problems encountered during writing of file

#Loop to display all items in extracted product list
with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
    headers = ["title", "currPrice", "freeShipping", "timeRemaining"]
    #writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONE, escapechar=' ')
    
    writer = csv.DictWriter(csv_file, fieldnames=headers, quoting=csv.QUOTE_NONE, lineterminator='\n', escapechar=' ')
    writer.writeheader()
    
    for product in products:
        #Get product title
        title_cont              = product.findAll("h3",{"class":"Product__title"})
        title                   = title_cont[0].text.strip()
        
        #Attempt to extract free shipping status from entries
        #If attenmpt to write to temp variable fails (i.e. nothing found), output "no" for status
        try:
            hasFreeShipping_cont    = product.findAll("span",{"class":"Product__icon--freeShipping"})
            hasFreeShipping         = hasFreeShipping_cont[0].text.strip()
            hasFreeShipping         = "Yes"
        except:
            hasFreeShipping         = "No"
        
        #Get current bid price
        currentPrice_cont       = product.findAll("span",{"class":"Product__priceValue u-textRed"})
        currentPrice            = currentPrice_cont[0].text.strip()
        
        #Get time remaining 
        #(Displays in Days, Hours or Minutes depending on text entry)
        timeRemaining_cont      = product.findAll("span",{"class":"Product__time"})
        timeRemaining           = timeRemaining_cont[0].text.strip()
        
        #Write temp entries to CSV file
        #Exception caught and loop interrupted if problems encountered with writing to CSV 
        try:
            #Remove commas from title and price to prevent CSV formatting conflicts
            #Not needed for hasFreeShipping and timeRemaining as commas not possible in those entries
            title           = title.replace(",","")
            currentPrice    = currentPrice.replace(",","")
            
            #Text data check: Display output text in console
            print("[" + str(index) + "]")
            print("Title: " + title)
            print("Current Price: " + currentPrice)
            print("Free Shipping: " + hasFreeShipping)
            print("Time Remaining: " + timeRemaining)
            print("\r\n")
            
            #Write current data row to new line in CSV file
            writer.writerow({"title":title, "currPrice":currentPrice, "freeShipping":hasFreeShipping, "timeRemaining":timeRemaining})
            index += 1  #Increment displayed index number
        except:
            errorTrigger_write = True   #Set error flag to True
            break                       #Interrupt exit for loop as error encountered


#Display message notifying user of output result (success or fail)
if errorTrigger_write == True:
    print("Process interrupted. Write failed...")
else:
    print("Write completed successfully!")


