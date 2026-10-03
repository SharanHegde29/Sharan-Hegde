import requests
from bs4 import BeautifulSoup
import smtplib
import time

# --- CONFIGURATION ---
PRODUCT_URL = 'https://www.amazon.in/dp/B0789LZTCJ'

TARGET_PRICE = 37000

# CREDENTIALS
sender_email = 'sharan.may29@gmail.com'
app_password = 'ukez rovf selx ewjl'
reciever_email = 'sharan.290505@gmail.com'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/"
}

def get_products_price():
    print(f"DEBUG: Trying to open -> {PRODUCT_URL}")
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error loading page. Status Code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        title_element = soup.find(id='productTitle')
        price_whole = soup.find(class_='a-price-whole')

        if not title_element or not price_whole:
            print("Error: Could not find the title or price tags.")
            return None
        
        title = title_element.get_text().strip()

        # --- FIX IS HERE ---
        # 1. replace(",", "") removes commas (37,000 -> 37000)
        # 2. replace(".", "") removes the trailing dot often found in Amazon prices
        current_price_str = price_whole.get_text().replace(",", "").replace(".", "").strip()
        
        current_price = float(current_price_str)

        return title, current_price
    
    except Exception as e:
        print(f"Error Occurred: {e}")
        return None
    
def send_alert_email(product_title, price):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender_email, app_password)

        subject = "PRICE DROP ALERT!"
        body = f"Good news!\n\nThe price for '{product_title[0:30]}...' has dropped to {price}.\n\nBuy it here: {PRODUCT_URL}"
        
        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail(sender_email, reciever_email, msg)
        print("SUCCESS: Email Sent")

        server.quit()
    except Exception as e:
        print(f"Email not sent: {e}")

def main():
    print("Price Tracking...")
    print("Checking Price...")

    data = get_products_price()

    if data:
        title, price = data
        print(f"Product: {title[0:40]}...")
        print(f"Current Price: {price}")
        print(f"Target Price: {TARGET_PRICE}")

        if price <= TARGET_PRICE:
            print("Target Met! Sending Email...")
            send_alert_email(title, price)
        else:
            print("Price is still too high. Checking again later.")
    
    else:
        print("Failed to retrieve the product data.")

if __name__ == "__main__":
    main()       