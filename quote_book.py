import requests, os
from bs4 import BeautifulSoup
import random
"""The purpose of the program is to parse through the GoodReads website using Beautiful Soup to 
collect all the quotes from a given author (The one currently is Brandon Sanderson) and compile
the list into a text document that will oder them by quote and what book the quote is from. 
Afterward run the print_quote() function to display a random quote from the text file. Set that 
function to be the only one to run and change your bashrc file to run this script on boot so 
every time you open the terminal you are greeted with a quote from your favorite author/authors"""

#Bash color options for print out
bold = '\033[1m'
cyan = '\033[1;36m'
blue = '\033[1;31m'

#Function to parse website and retrive quote list for the given page
def site_parse(page):
	#Change the URL here to the URL of the Author you would like to get quotes from
	URL = 'https://www.goodreads.com/author/quotes/38550.Brandon_Sanderson?page=' + str(page)
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	quote = soup.find_all("div",{"class":"quote"})
	return quote
#Function that goes through quote list and returns the quote without hyperlink text
def quote_parse(quote_element):
	
	quote = quote_element.find('div', {'class': 'quoteText'}).get_text("|", strip=True)
	# first element is always the quote
	quote = quote.split('|')
	return quote
#Opens a text file and adds the list of quotes and books
def get_quotes():
	path_save = os.path.join(os.getcwd(), "list.txt")
	f = open(path_save, 'w',encoding='utf-8')
	#below is a list of books you would like excluded from the list, I have not read these
	#books so I do not want spoilers
	books = ["Alcatraz Versus the Evil Librarians","El camino de los reyes","Skyward","The Rithmatist","Alcatraz Versus the Knights of Crystallia","Juramentada","Palabras radiantes","Perfect State","Skyward"]
	#Language is a list of odd characters to exclude other languages, this is not a perfect system so you may have to parse the text after
	language = ["φ","ú","ä","ó"]
	for i in range(1,118):
		quote = site_parse(i)
		for e in quote:
			quote = quote_parse(e)
			print("saving")
			try:
				if not (quote[-1] in books):
					for i in range(len(quote) - 2):
						f.write(quote[i])
					f.write("BOOK")
					f.write(quote[-1])
					f.write("\n")
			except:
				pass
	f.close()
	print("done")
#After the text file is created you can call this function to parse the file for different languages
#That made its way through the original function and delete them
def delete_quotes():
	f = open("list.txt", 'r')
	quotes = f.readlines()
	f.close()
	language = ["φ","ú","ä","ó","é","í","š","ž","è","á","д"]
	f = open("list.txt", 'w')
	check = True
	for quote in quotes:
		for q in quote:
			if q in language:
				print("found")
				check = False
				quote = ""
				break
		if check == True:
			f.write(quote)
		else:
			check = True
	
	f.close()

#The funciton simply prints a random quote from the text file in the terminal, add this program to 
# the bashrc file and everytime it opens on terminal it will post a quote
def print_quote():
		#change file location to the location of the list of books text file
		f = open("/mnt/c/Users/PATHTOFILE",'r')
		quotes = f.readlines()
		number = random.randint(0,len(quotes))
		quote = quotes[number].split("BOOK")
		print(bold + blue + quote[0] + "\n" + cyan + quote[1])
		f.close()
print_quote()
