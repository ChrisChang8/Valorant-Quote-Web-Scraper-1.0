from bs4 import BeautifulSoup
import requests
import os

#https://www.kingdomarchives.com/

agents = [
    "Brimstone",
    "Viper",
    "Omen",
    "Killjoy",
    "Cypher",
    "Sova",
    "Sage",
    "Breach",
    "Reyna",
    "Phoenix",
    "Jett",
    "Raze",
    "Skye",
    "Yoru",
    "Astra",
    "KayO",
    "Chamber",
    "Neon",
    "Fade",
    "Harbor",
    "Gekko",
    "Deadlock",
    "Iso"
]

def find_quotes():
    #Check if directory quotes exists, else make one
    directory = 'quotes'
    if not os.path.exists(directory):
        os.makedirs(directory)

    #for loop to keep track of the count of quotes
    for agent in agents:
        quote_counter = 1 

        #base url
        url = f'https://www.kingdomarchives.com/voicelines?agent={agent}&page=1'

        #Retrieves html info from url
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')


        #Find number of page html
        input_element = soup.find('input', class_='page-indicator')
        #If can't find the page-indicator class, skip agent
        if input_element is None:
            print(f"No page indicator found for {agent}. Skipping...")
            continue
        
        #Total pages equal to the end value of page-indicator class
        total_pages = int(input_element['value'].split(' of ')[-1])

        #Open and create file for the agent and store in the directory
        with open(os.path.join(directory, f'{agent}_All_Quotes.txt'), 'a', encoding='utf-8') as f:
            
            #Loop upto the amount of pages
            for page_index in range(1, total_pages + 1):
                url = f'https://www.kingdomarchives.com/voicelines?agent={agent}&page={page_index}'
                html_text = requests.get(url).text
                soup = BeautifulSoup(html_text, 'lxml')

                #Loop inside the <p> vl-p class, finding all quotes
                quotes = soup.find_all('p', class_='vl-p')

                #Assign quote and context to variable
                for quote in quotes:
                    context_elem = quote.find_next('td', class_='td-vl-context')
                    transcription_elem = quote.find_next('td', class_='td-vl-trans')

                    #If there's no element to be found, skip
                    if context_elem is None or transcription_elem is None:
                        #print(f"Skipping a quote for {agent} on page {page_index}: Context or Transcription not found.")
                        continue
                    
                    #Clean out the text
                    context = context_elem.text.strip()
                    transcription_with_share = transcription_elem.text.strip()
                    transcription = transcription_with_share.split('\n')[0]

                    # Skip quotes with less than 8 words
                    words = transcription.split()
                    words = [word for word in words if word]  # Remove empty strings
                    if len(words) < 8:
                        #print(f"Skipping a short quote for {agent} on page {page_index}.")
                        continue

                    #Ouput text to file
                    f.write(f"Quote {quote_counter} from page {page_index}:\n")
                    f.write(f"Context: {context}\n")
                    f.write(f"Transcription: {transcription}\n\n")
                    #print(f'Quote {quote_counter} for {agent} from page {page_index} added to file.')

                    #Increment quote counter
                    quote_counter += 1  # Increment the quote counter

        print(f"{agent}'s QUOTES SUCCESSFULLY SCRAPED")

find_quotes()

