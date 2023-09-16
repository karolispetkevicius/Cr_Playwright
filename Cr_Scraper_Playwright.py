from playwright.sync_api import sync_playwright
import json
from playwright_stealth import stealth_sync
import time
import random




proxies = [
    'http://qflaraby:opz4w46ujvjw@185.199.229.156:7492',
    'http://qflaraby:opz4w46ujvjw@185.199.228.220:7300',
    'http://qflaraby:opz4w46ujvjw@185.185.199.231.45:8382',
    'http://qflaraby:opz4w46ujvjw@188.74.210.207:6286',
    'http://qflaraby:opz4w46ujvjw@185.188.74.183.10:8279',
    'http://qflaraby:opz4w46ujvjw@185.188.74.210.21:6100',
    'http://qflaraby:opz4w46ujvjw@45.155.68.129:8133',
    'http://qflaraby:opz4w46ujvjw@154.95.36.199:6893',
    'http://qflaraby:opz4w46ujvjw@45.94.47.66:8110',
]


search_input = "305485432"
login_url = "https://www.cr.lt/"
search_url = "https://www.cr.lt/imones/n/noriu/search/"


account_pool = [
    {"username": "karolispetkevicius", "password": "y5rAUZ2"}
]

def rotate_proxy():
    return random.choice(proxies)




def detect_captcha(page):
    captcha_element = page.query_selector('div.errors')

    if captcha_element:
        captcha_image = captcha_element.query_selector('img')
        captcha_input = captcha_element.query_selector('input[name="private_key"]')

        if captcha_image and captcha_input:
            return True

    return False


with sync_playwright() as p:

    for account in account_pool:
        
        selected_proxy = rotate_proxy()
        browser = p.chromium.launch(headless=False, slow_mo=50,  args=[f'--proxy-server={selected_proxy}'])
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
        stealth_sync(context)
        page = context.new_page()
        page.goto(login_url)

        # Wait for the login elements to appear
        page.wait_for_selector('input[name="ClientId"]', timeout=10000)
        page.wait_for_selector('input[name="ClientPassw"]', timeout=10000)


        page.wait_for_selector('input[value="Prisijungti"]', timeout=10000)

        page.fill('input[name="ClientId"]', account["username"])
        page.fill('input[name="ClientPassw"]', account["password"])

        page.evaluate('''() => {
            const button = document.querySelector('input[value="Prisijungti"]');
            if (button) {
                button.click();
            }
        }''')


        if page.url != login_url:
            print(f"Login successful for account: {account['username']}!")
            break
        else:
            print(f'Login in not successful for account: {account["username"]}.')
            browser.close()  

            time.sleep(3)  

            continue  

   
    # Capture cookies and store as a JSON file
    captured_cookies = page.context.cookies()

    with open('captured_cookies.json', 'w') as cookie_file:
        json.dump(captured_cookies, cookie_file)

    # Add the loaded cookies to the context
    with open('captured_cookies.json', 'r') as cookie_file:
        loaded_cookies = json.load(cookie_file)

        page.context.add_cookies(loaded_cookies)

        # Navigate to the search URL
        page.goto(search_url)

        # Detect if a captcha is present, if it is, solve it manually
        captcha_present = detect_captcha(page)

        if captcha_present:
            print("Captcha detected.")
            captcha_solution = input("Captcha solution:")
            page.fill('input[name="private_key"]', captcha_solution)

        # Enter data in the search bar
        page.fill('input[name="Company"]', '305485432')

        # Click the search button
        page.evaluate('''() => {
            const button = document.querySelector('input[value="Ieškoti"]');
            if (button) {
                button.click();
            }
        }''')

        try:
            # Wait for the handler to navigate to the redirected URL
            page.wait_for_selector('td:has-text("Įmonės kodas:")', timeout=100000)

            # Locate the <td> element containing the company code
            company_code_td = page.query_selector('td.bold:has-text("Įmonės kodas:") + td')
            company_code = company_code_td.inner_text() if company_code_td else None

            # Locate the <td> element containing the registration date
            registration_date_td = page.query_selector('td.bold:has-text("Registravimo data:") + td')
            registration_date = registration_date_td.inner_text() if registration_date_td else None

            if company_code and registration_date:
                print("Company Code:", company_code.strip())
                print("Registration Date:", registration_date.strip())
            else:
                print("Company code or registration date not found on the page.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            browser.close()  



