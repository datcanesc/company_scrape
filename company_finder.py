from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import os
import yaml

config_path = "/app/config/config.yaml"
with open(config_path) as file:
    config = yaml.safe_load(file)

sel_config = config["seleniumgrid"]

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument("--headless")
driver = webdriver.Remote(
    command_executor=f"{sel_config['host']}:{sel_config['port']}", options=chromeOptions
)

country_codes  = [
    "afghanistan", "åland-islands", "albania", "algeria", "american-samoa", "andorra", "angola", "anguilla", "antarctica",
    "antigua-and-barbuda", "argentina", "armenia", "aruba", "australia", "austria", "azerbaijan", "bahamas", "bahrain",
    "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bermuda", "bhutan", "bolivia-plurinational-state-of",
    "bonaire-sint-eustatius-and-saba", "bosnia-and-herzegovina", "botswana", "brazil", "british-indian-ocean-territory", 
    "brunei-darussalam", "bulgaria", "burkina-faso", "burundi", "cambodia", "cameroon", "canada", "cape-verde", "cayman-islands", 
    "chad", "chile", "china", "christmas-island", "colombia", "congo", "congo-the-democratic-republic-of-the", "cook-islands",
    "costa-rica", "côte-d'ivoire", "croatia", "cuba", "curaçao", "cyprus", "czech-republic", "denmark", "djibouti", "dominica",
    "dominican-republic", "ecuador", "egypt", "el-salvador", "equatorial-guinea", "eritrea", "estonia", "ethiopia", "falkland-islands-(malvinas)",
    "faroe-islands", "fiji", "finland", "france", "french-guiana", "french-polynesia", "french-southern-territories", "gabon", "gambia",
    "georgia", "germany", "ghana", "gibraltar", "greece", "greenland", "grenada", "guadeloupe", "guam", "guatemala", "guernsey", "guinea",
    "guyana", "haiti", "honduras", "hong-kong", "hungary", "iceland", "india", "indonesia", "iran-islamic-republic-of", "iraq", "ireland",
    "isle-of-man", "israel", "italy", "jamaica", "japan", "jersey", "jordan", "kazakhstan", "kenya", "kiribati", "korea-republic-of",
    "kosovo", "kuwait", "kyrgyzstan", "lao-people's-democratic-republic", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein",
    "lithuania", "luxembourg", "macao", "macedonia-the-former-yugoslav-republic-of", "madagascar", "malawi", "malaysia", "maldives", "mali",
    "malta", "marshall-islands", "martinique", "mauritania", "mauritius", "mayotte", "mexico", "micronesia-federated-states-of",
    "moldova-republic-of", "monaco", "mongolia", "montenegro", "montserrat", "morocco", "mozambique", "myanmar", "namibia", "nepal",
    "netherlands", "new-caledonia", "new-zealand", "nicaragua", "niger", "nigeria", "northern-mariana-islands", "norway",
    "oman", "pakistan", "palau", "palestine-state-of", "panama", "papua-new-guinea", "paraguay", "peru", "philippines", "poland",
    "portugal", "puerto-rico", "qatar", "réunion", "romania", "russian-federation", "rwanda", "saint-kitts-and-nevis", "saint-lucia",
    "saint-vincent-and-the-grenadines", "samoa", "san-marino", "saudi-arabia", "senegal", "serbia", "seychelles", "sierra-leone", "singapore",
    "sint-maarten-(dutch-part)", "slovakia", "slovenia", "solomon-islands", "somalia", "south-africa", "south-sudan", "spain", "sri-lanka",
    "sudan", "suriname", "swaziland", "sweden", "switzerland", "syrian-arab-republic", "taiwan-province-of-china", "tajikistan",
    "tanzania-united-republic-of", "thailand", "timor-leste", "togo", "tonga", "trinidad-and-tobago", "tunisia", "turkey", "turkmenistan",
    "turks-and-caicos-islands", "uganda", "ukraine", "united-arab-emirates", "united-kingdom", "united-states", "uruguay", "uzbekistan",
    "vanuatu", "venezuela-bolivarian-republic-of", "viet-nam", "virgin-islands-british", "virgin-islands-us", "western-sahara",
    "yemen", "zambia", "zimbabwe"
]


base_url = "https://theorg.com/explore/countries/"
output_path = "/company_urls_data/company_urls.txt"
last_processed_file = "/company_urls_data/last_processed.txt"

# Eğer last_processed.txt dosyası yoksa oluştur
if not os.path.exists(last_processed_file):
    with open(last_processed_file, 'w') as f:
        f.write("")

# last_processed.txt dosyasından en son işlenen ülke kodunu oku
with open(last_processed_file, 'r') as f:
    last_processed_code = f.read().strip()

# Eğer en son işlenen ülke kodu varsa, bu kodun index'ini bul
start_index = 0
if last_processed_code:
    start_index = country_codes.index(last_processed_code) + 1

for code in country_codes[start_index:]:
    url = base_url + code
    driver.get(url)
    time.sleep(4)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    try:
        org_links = driver.find_elements(By.CSS_SELECTOR, 'a[class="sc-a7e97447-4 gUNvNW"]')
        if not org_links:
            print(f"Element bulunamadı: {code}")
            continue
    except NoSuchElementException:
        print(f"!!!!!!!!!! Element bulunamadı: {code}")
        continue

    url_list = [org_link.get_attribute("href") for org_link in org_links]

    with open(output_path, "a", encoding="utf-8") as file:
        for url in url_list:
            file.write(url + "\n")
    
    # İşlenen ülke kodunu last_processed.txt dosyasına yaz
    with open(last_processed_file, 'w') as f:
        f.write(code)

driver.quit()
