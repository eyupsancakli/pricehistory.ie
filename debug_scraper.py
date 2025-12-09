from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import json
import re
import time

url = "https://www.donedeal.ie/cars-for-sale/volvo-xc60-plus-dark-t6-recharge-awd-great-spec/36855140"

print(f"Fetching {url}...")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("window-size=1280,800")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

try:
    driver.get(url)
    time.sleep(5)
    
    print(f"Page Title: {driver.title}")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        print("FOUND __NEXT_DATA__")
        try:
            data = json.loads(next_data.string)
            props = data.get('props', {}).get('pageProps', {}).get('ad', {})
            if not props:
                print("No 'ad' in pageProps, checking 'advert'...")
                props = data.get('props', {}).get('pageProps', {}).get('advert', {})
            
            if props:
                print("Found 'props' data:")
                print(f"Header: {props.get('header')}")
                print(f"Make: {props.get('make')}")
                print(f"Price: {props.get('price')}")
                print(f"Previous Price: {props.get('previousPrice')}") # Hypothesis
                print(f"Currency: {props.get('currency')}")
                print(f"Display Attributes: {len(props.get('displayAttributes', []))} items")
                
                # Check display attributes for price info
                for attr in props.get('displayAttributes', []):
                    if 'price' in attr.get('name', '').lower():
                        print(f"Price Attribute: {attr}")
            else:
                print("Could not find 'ad' or 'advert' in props.")
                # Print keys to debug
                print(f"Keys in pageProps: {data.get('props', {}).get('pageProps', {}).keys()}")
        except Exception as e:
            print(f"JSON Error: {e}")
    else:
        print("NO __NEXT_DATA__ found.")
        
    # Check HTML fallback
    h1 = soup.find('h1')
    print(f"H1 Tag: {h1.get_text() if h1 else 'None'}")
    
    prices = soup.find_all(class_=re.compile(r'price|Price'))
    print(f"Price candidates: {[p.get_text() for p in prices]}")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
