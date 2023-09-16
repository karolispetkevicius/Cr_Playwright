from playwright.sync_api import sync_playwright
import json
from playwright_stealth import stealth_sync
import time
import random
import pandas as pd




proxies = [{'http://qflaraby:opz4w46ujvjw@185.199.228.220:7300'},
    'http://qflaraby:opz4w46ujvjw@185.185.199.231.45:8382',
    'http://qflaraby:opz4w46ujvjw@188.74.210.207:6286',
    'http://qflaraby:opz4w46ujvjw@185.188.74.183.10:8279',
    'http://qflaraby:opz4w46ujvjw@185.188.74.210.21:6100',
    'http://qflaraby:opz4w46ujvjw@45.155.68.129:8133',
    'http://qflaraby:opz4w46ujvjw@154.95.36.199:6893',
    'http://qflaraby:opz4w46ujvjw@45.94.47.66:8110',
]


search_input_top90 = ['305887609', '306349759', '306371816', '306373062', '304780650', '306351646', '305991038', '305901884', '304981393', '305990413', '304974203', '306350754', '304970386', '304966758', '304968022', '305485432', '304923130', '305368468', '305097636', '305097561', '304971513', '304869729', '304960417', '304910421', '304972729', '305038602', '305039113', '305907773', '305500489', '305903892', '305992211', '305426430', '303250236', '304289683', '304715695', '304779114', '305907307', '305396916', '305390692', '305911241', '304779872', '305907499', '305190250', '305173386', '305791660', '305534071', '305534089', '305537053', '305544507', '305718872', '305928881', '305178472', '305561638', 
'305562163', '305291406', '305188922', '305874184', '305886717', '305853603', '305901585', '305809083', '305734848', '305219093', '305891949', '305892556', '305894443', '305901083', '305862239', '305726260', '305739172', '305730102', '305900273', '305863138', '305291395', '305791678', '305278782', '305216581', '305289526', '305500724', '305520157', '305565946', '305568038', '305587501', '305603051', '305609428', '305243315', '305343917', '305475025', '305317299', '305645050']
search_input_rest = ['305227663', '304985993', '305016260', '306324453', '304994451', '305026856', '306000608', '306348721', '306281137', '305016958', '305028394', '306339291', '306328665', '305017202', '305030388', '306089667', '306041131', '306079744', '306026161', '306078795', '306174690', '306268766', '306032591', '306028760', '306087278', '306008576', '306064710', '306277847', '306199754', '306273172', '306013192', '306062684', '305133609', '306005726', '305038399', '304045704', '304962585', '305163666', '305135542', '306161390', '306320782', '306319762', '306311178', '306297903', '306143360', '303055058', '306162396', '305154350', '306297885', '306160872', '306149395', '306134913', '306148279', 
'306021634', '306116146', '306139198', '306098399', '306157189', '306011145', '306108651', '306023973', '306108110', '306106248', '306118827', '306127541', '306119815', '306133359', '306016181', '305166922', '306025636', '306062677', '306095339', '305911871', '305489904', '305919327', '305393724', '305407914', '305490365', '305937371', '305932417', '305947419', '305911750', '305937599', '305958629', '305428538', '305938808', '305938402', '305944184', '305945496', '305450449', '305929595', '305936230', '305917504', '305929588', '305426341', '305951588', '305911825']
login_url = "https://www.cr.lt/"
search_url = "https://www.cr.lt/imones/n/noriu/search/"


account_pool = [
    {"username": "aoo0009", "password": "25SYqpH"}
]

#def rotate_proxy():
 #   return random.choice(proxies)

scraped_data = []


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
        
        #selected_proxy = rotate_proxy()
        browser = p.chromium.launch(headless=False, slow_mo=50)
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

        '''
        if page.url != login_url:
            print(f"Login successful for account: {account['username']}!")
            break
        else:
            print(f'Login in not successful for account: {account["username"]}.')
            browser.close()  

            time.sleep(3)  

            continue  
            '''
   
        # Capture cookies and store as a JSON file
        captured_cookies = page.context.cookies()

        with open('captured_cookies.json', 'w') as cookie_file:
            json.dump(captured_cookies, cookie_file)

        # Add the loaded cookies to the context
        with open('captured_cookies.json', 'r') as cookie_file:
            loaded_cookies = json.load(cookie_file)

        page.context.add_cookies(loaded_cookies)




        for search in search_input_rest:


        # Navigate to the search URL
            page.goto(search_url)

            # Detect if a captcha is present, if it is, solve it manually
            captcha_present = detect_captcha(page)

            if captcha_present:
                print("Captcha detected.")
                captcha_solution = input("Captcha solution:")
                page.fill('input[name="private_key"]', captcha_solution)

            # Enter data in the search bar
            page.fill('input[name="Company"]', search)

            # Click the search button
            page.evaluate('''() => {
                const button = document.querySelector('input[value="Ieškoti"]');
                if (button) {
                button.click();
                }
            }''')

                # Wait for the handler to navigate to the redirected URL
            page.wait_for_selector('td:has-text("Įmonės kodas:")', timeout=100000)

            company_name_h2 = page.query_selector('td.darkblue > h2')
            company_name = company_name_h2.inner_text() if company_name_h2 else None

                # Locate the <td> element containing the company code
            company_code_td = page.query_selector('td.bold:has-text("Įmonės kodas:") + td')
            company_code = company_code_td.inner_text() if company_code_td else None

            adress_td = page.query_selector('td.bold:has-text("Registracinis adresas:") + td')
            address = adress_td.inner_text() if adress_td else None

                # Locate the <td> element containing the registration date
            registration_date_td = page.query_selector('td.bold:has-text("Registravimo data:") + td')
            registration_date = registration_date_td.inner_text() if registration_date_td else None

            data = {
                    "Pavadinimas": company_name.strip(),
                    "Kodas": company_code.strip(),
                    "Adresas": address.strip(),
                    "Įregistravimo data": registration_date.strip()
                }
            
            scraped_data.append(data)



        time.sleep(3)
        browser.close()  

df = pd.DataFrame(scraped_data)

df.to_excel('Rest.xlsx', index = True, startrow=1)