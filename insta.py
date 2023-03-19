from instagrapi import Client
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from typing import Dict
import textwrap
from dotenv import load_dotenv
import os

load_dotenv()

# Get the environment variables
insta_username = os.getenv('insta_username')
insta_password = os.getenv('insta_password')
kton_username = os.getenv('kton_username')
kton_password = os.getenv('kton_password')

# ##Logging in (No need to login until system is working)
# cl = Client()
# cl.login(username=insta_username, password=insta_password)


##Retrieve a random quote
def getQuote():
    ##Log into KTON and recieve token
    login_url = "https://kindle-notes-manager-reloaded.fly.dev/login"
    body = {'username': kton_username, 'password': kton_password}
    
    try:
        response=requests.post(login_url, json=body)
        response.raise_for_status()  # raise an exception if the status code is not 2xx
        token = response.json()['token']
        
        ##Retrieve random quote
        quote_url = "https://kindle-notes-manager-reloaded.fly.dev/books/random-highlight"
        headers = {'x-auth-token': token}
        
        try: 
            quote_response = requests.get(quote_url,headers=headers)
            quote_response.raise_for_status()  # raise an exception if the status code is not 2xx
            randomHighlight = quote_response.json()
            return randomHighlight
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
            
            
            
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    
def getImage():
    ##Using Dall-e
    ##Requests Unsplash
    random_url="https://api.unsplash.com/photos/random"
    access_key = "QyIVMq6A6fL2y7WlNE9XsU2X7F40JUSTj-nsCaX_MYI"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {'query': 'modern building black', 'orientation': 'squarish'}
    
    try:
        unsplash_response = requests.get(random_url,headers=headers,params=params)
        unsplash_response.raise_for_status() #Anything thats not 200
        random_image = unsplash_response.json()["urls"]["raw"]
        
        ##Saving the file
        response = requests.get(random_image)
        with open('image.jpg', 'wb') as f:
            # Write the contents of the response to the file
            f.write(response.content)
            
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

def createPost():
        # Open image
    img = Image.open("image.jpg")
    draw = ImageDraw.Draw(img)
    font_size = 300
    font = ImageFont.truetype("font.ttf", 300)
    
    # Get quote information
    quote = getQuote()['randomHighlight']
    title, author = quote['title'], quote['author']
    text = quote['highlight']['Text']
    
    # Set background color
    bg_color = (0, 0, 0, 108)
    

    
    # Wrap text and calculate total height
    wrapped_text = textwrap.wrap(text, width=40) #Maximum 20 characters per line, splits into array of strings
    line_height = font.getsize('hg')[1] #random string to get rough height of a single line (returns a tuple of (height,width))
    total_height = len(wrapped_text) * line_height #jsut multiply each line by their heights
    
    # center vertically
    y = (img.height - total_height) / 2
    
    # Draw each line of wrapped text on the image
    for line in wrapped_text:
        # Center horizontally
        line_width = font.getsize(line)[0] #width
        line_x = (img.width - line_width) / 2
        
        # Draw background rectangle (defining top left and bottom right point)
        bg_x1, bg_y1 = line_x - 10, y - 10
        bg_x2, bg_y2 = line_x + line_width + 10, y + line_height + 10
        draw.rectangle((bg_x1, bg_y1, bg_x2, bg_y2), fill=bg_color)
        
        # Draw text
        draw.text((line_x, y), line, font=font, fill=(255, 255, 255))
        
        # Move to next line
        y += line_height
    
    # Save modified image
    img.save("overlay.jpg")
    
    


getImage()
createPost()
        
    
    
    
    
    
    
# getQuote()
    
    
# caption="first post"
# cl.photo_upload('tests.png',caption)