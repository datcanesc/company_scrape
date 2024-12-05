from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import os
import yaml
import traceback

config_path = "/app/config/config.yaml"
with open(config_path) as file:
    config = yaml.safe_load(file)

sel_config = config["seleniumgrid"]

# Chrome seçeneklerini ayarla
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--incognito")
chromeOptions.add_argument("--headless")
driver = webdriver.Remote(
    command_executor=f"{sel_config['host']}:{sel_config['port']}", options=chromeOptions
)

def get_social_media_links(driver, class_name, default=None):
    try:
        links_container = driver.find_element(By.CLASS_NAME, class_name)
        links = links_container.find_elements(By.TAG_NAME, "a")
        return [link.get_attribute("href") for link in links]
    except NoSuchElementException:
        return default if default is not None else []
    
def get_text_by_class_name(driver, class_name, default=None):
    try:
        return driver.find_element(By.CLASS_NAME, class_name).text
    except NoSuchElementException:
        return default
    
def get_text_by_class_names(driver, class_names, default=None):
    for class_name in class_names:
        try:
            return driver.find_element(By.CLASS_NAME, class_name).text
        except NoSuchElementException:
            continue
    return default

def get_attribute_by_class_name(driver, class_name, attribute, default=None):
    try:
        return driver.find_element(By.CLASS_NAME, class_name).get_attribute(attribute)
    except NoSuchElementException:
        return default

def click_element_by_class_name(driver, class_name):
    try:
        driver.find_element(By.CLASS_NAME, class_name).click()
    except NoSuchElementException:
        pass

def scrape_profile(driver, profil_url):
    driver.get(profil_url)
    time.sleep(1)

    profil_info = driver.find_element(By.CLASS_NAME, "sc-fd87ca3d-0.jHkhlk.sc-d0fe8922-2.kimjIO")

    name = get_text_by_class_name(driver, "sc-d3ca6972-0.sc-d0fe8922-3.irBBrW.guqA-Dx")
    photo_url = get_attribute_by_class_name(profil_info, "sc-dcc6af1e-1.hLdhge", "src")

    role = get_text_by_class_name(profil_info, "sc-d3ca6972-0.sc-d0fe8922-1.kEyLlR.lfvyQv")

    person_about = get_text_by_class_names(driver, [
    "sc-53c3541a-3.sc-f65cbdf0-0.etLiDz.jUBLat",
    "sc-2c46953c-3.sc-66ef78ef-0.hGqFjX.fQmJDM"
    ])
    
    person_links = get_attribute_by_class_name(driver,"sc-6de434d-3.fxxeMP","href")
    
    try:
        previous_links_container = driver.find_element(By.CLASS_NAME,"sc-ab61bac2-3.krtZoa")
        links = previous_links_container.find_elements(By.TAG_NAME, "a")
        previous_company_links = [link.get_attribute("href") for link in links]
    except NoSuchElementException:
        previous_company_links = []
    
    return {
        "name": name,
        "role": role,
        "profil_url": profil_url,
        "photo_url": photo_url,
        "person_links":person_links,
        "person_about": person_about,
        "prev_comp_link":previous_company_links
    }

def scrape_team(driver, team_url):
    driver.get(team_url)
    # team_name = get_text_by_class_name(driver, "sc-d3ca6972-0.sc-bb1bc1e8-3.foLzvG.jZYlhQ")
    team_name = get_text_by_class_name(driver, "sc-d3ca6972-0.sc-450f287c-3.foLzvG.jgpRZh")
    team_about = get_text_by_class_name(driver, "sc-d3ca6972-0.deGbJB")
    members = driver.find_elements(By.CLASS_NAME, "sc-23066df0-4.bGaxEm")
    member_profil_urls = [member.get_attribute("href") for member in members]
    
    team_members = [scrape_profile(driver, member_profil_url) for member_profil_url in member_profil_urls]
    
    return {
        "team_name": team_name,
        "team_about":team_about,
        "members": team_members
    }

def scrape_company(url):
    driver.get(url)
    time.sleep(4)

    # click_element_by_class_name(driver, "sc-80e062b3-2.fskZGw")
    click_element_by_class_name(driver, "sc-d92aa278-2 iyZABG")
    click_element_by_class_name(driver, "sc-c699a8bc-1.ighSQE.sc-ca8d01e2-0.iyvloi")

    company_name = get_text_by_class_name(driver, "sc-d3ca6972-0.WiNit")
    company_url = url
    # company_logo = get_attribute_by_class_name(driver, "sc-e588943-1.eYbRcR.sc-28945b3-1.eWOjsZ", "src")
    company_logo = get_attribute_by_class_name(driver, "sc-e588943-1.eYbRcR.sc-6b1cd0f2-1.dAepNY", "src")
    company_about = get_text_by_class_name(driver, "sc-d3ca6972-0.eGfdcf", "").replace("Read less", "").strip()
    industries = get_text_by_class_name(driver, "sc-d3ca6972-0.sc-edd8a6de-1.sc-edd8a6de-2.kEyLlR.gVbaMw.cvBscu")
    location = get_text_by_class_name(driver, "sc-d3ca6972-0.sc-edd8a6de-1.kEyLlR.eEvIUj")
    social_media_links = (
    get_social_media_links(driver, "sc-6de434d-0.mdjtR") +
    get_social_media_links(driver, "sc-6de434d-0.mdjtL") +
    get_social_media_links(driver, "sc-6de434d-0.mdjtK") +
    get_social_media_links(driver, "sc-6de434d-0.mdjtQ")
    )
    
    profil_elements = driver.find_elements(By.CLASS_NAME, "PositionCard_profileLink__HKaz_")
    profil_urls = [profil.get_attribute("href") for profil in profil_elements if profil.get_attribute("href")]
    
    team_links = driver.find_elements(By.CSS_SELECTOR, 'a.sc-85a5f16-0.cGLCDK')

    team_urls = [team_link.get_attribute("href") for team_link in team_links]
    
    
    persons = [scrape_profile(driver, profil_url) for profil_url in profil_urls]
    
    teams = [scrape_team(driver, team_url) for team_url in team_urls]
    
    return {
        "company_name": company_name,
        "company_url": company_url,
        "company_logo": company_logo,
        "company_about": company_about,
        "industries": industries,
        "location": location,
        "links": social_media_links,
        "persons": persons,
        "teams": teams
    }

company_output_path = "/company_data/company.json"
company_urls_path = "/company_urls_data/company_urls.txt"
scraped_urls_path = "/company_data/scraped_urls.txt"

def main():
    scraped_urls = set()
    
    if os.path.exists(scraped_urls_path):
        with open(scraped_urls_path, 'r') as f:
            scraped_urls = set(line.strip() for line in f.readlines())
    
    with open(company_urls_path, 'r') as file:
        urls = [url.strip() for url in file.readlines()]
    
    data_list = []
    
    for url in urls:            
        if url not in scraped_urls:
            try:
                data = scrape_company(url)
                data_list.append(data)
                
                with open(scraped_urls_path, 'a') as f:
                    f.write(url + '\n')
                
                with open(company_output_path, 'w', encoding='utf-8') as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=4)
                
                print(f"{url} scrape edildi ve kaydedildi.")
            except Exception as e:
                error_message = traceback.format_exc()  # Tüm hata geçmişini alır
                print(f"{url} scrape edilirken hata oluştu:\n{error_message}")  
        print("Tüm veriler JSON dosyasına yazıldı")
        
    driver.quit()

if __name__ == "__main__":
    main()
