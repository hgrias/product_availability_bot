# Product Availability Bot

As I started building my first PC, I really wanted a SFF build. It just so happened that the NZXT H1 released a couple weeks prior, and supply has been short. So I created this python bot to scrape the NZXT H1 web page via an AWS EC2 instance running the script via cron job every 2 minutes. My method uses Beautiful Soup to parse the HTML, check the add to cart button, and if it says "OUT OF STOCK", then do nothing and run the script again in 2 minutes.

There is error handling, so if something unexpected happens, the script will terminate and email me immediately. 

If the item comes back in stock or is available for pre-order, it will notify me via email immediately.
