#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
from config import *
import smtplib
import requests
import sys
import time
import logging

# Setting up logging information to save to separate file
logging.basicConfig(
    filename='/home/ec2-user/python_bot/bot_logs.log',
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.info("Script has started running.")

# creates SMTP session
server = smtplib.SMTP('smtp.gmail.com', 587)
logging.info("Email Server Started.")
# start TLS for security
server.starttls()
# Authentication
server.login(sender_email, sender_password)

# Setting the URL of the webpage we want to scrape
url = "https://www.nzxt.com/products/h1-matte-white"

# Using requests.get to retrieve the webpage
page = requests.get(url)

# Initializing our BeautifulSoup Object to parse the HTML
soup = bs(page.text, 'html.parser')

# Finding the add to cart button (returns None if not found)
addToCartButton = soup.find("button", attrs={"class": "add-to-cart"})

# Variable to tell us if the item is in stock or not
inStock = False

try:
    # If the add to cart button exists, check its text
    if addToCartButton:
        # If the button text is not "OUT OF STOCK", the item must be in stock
        if addToCartButton.text != "OUT OF STOCK":
            inStock = True
# Handle errors due to not finding the Add to Cart button
except:
    logging.error("There was an error finding the Add to Cart button.")
    subject = "BOT ERROR: CAN'T FIND ADD TO CART BUTTON"
    body = "FIX ASAP"
    message = 'Subject: {}\n\n{}'.format(subject, body)
    server.sendmail(sender_email, receiver_email, message)
    logging.error("Error Email Sent.")
    logging.error("Shutting Down the Email Server.")
    server.quit()
    logging.error("Shutting down program.")
    sys.exit(1)

# If the case is not in stock, log the info and end
if not inStock:
    logging.info("Item is still out of stock. Will check again in 2 minutes")
    sys.exit(0)
# If the case is in stock, send me an email right away and end the program
else:
    # message to be sent
    subject = "BUY THE NZXT H1 CASE NOW!"
    body = "Here's the link: https://www.nzxt.com/products/h1-matte-white"
    message = 'Subject: {}\n\n{}'.format(subject, body)
    # sending the mail
    server.sendmail(sender_email, receiver_email, message)
    logging.info("Case is in stock. Notification email Sent.")
    # terminating the session
    server.quit()
    logging.info("Email Server Shutting Down.")
    logging.info("Exiting Program Successfully.")
    sys.exit(0)
