import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def priorartlink(contestlink,driver):   
    try:
        driver.get(contestlink)
        

        
        try:
            download_link_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'DOWNLOAD WINNING PRIOR ART HERE:')]/following-sibling::a"))
            )
            download_link = download_link_element.get_attribute("href")
            return download_link
        except:
            print("Tag can't be found :(")
            return None

    except Exception as e:
        
        return None
    finally:
        print("Done")

def prior_art(contestlink,driver):
    
    #use contest link to get the ID of the prior art
    #Here is an example of a link you would recieve as a function parameter: https://patroll.unifiedpatents.com/contests/mJ5QT4wkDCCjhy9xb
   
    artlink=priorartlink(contestlink,driver)
    if artlink:
        pass
    else:
        return None

    prior_art_list = []

    if True:
        driver.get(artlink)
        
        #waits until page loads dynamically
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')) 
        
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        p_tags = soup.find_all('p')

            

        for p_tag in p_tags:
                if "Winning Submissions:" in p_tag.text:
                    submissions_text = p_tag.text.split("Winning Submissions:")[1].strip()
                    #splits by semi colon to find list of prior art
                    references = [ref.strip() for ref in submissions_text.split(';')]
                    prior_art_list.extend(references)


    #this is another style of the page: https://www.unifiedpatents.com/insights/2025/3/31/3000-awarded-in-second-cloud-native-heroes-challenge-on-patroll
    if len(prior_art_list)==0:
        patent_links = soup.find('ul', {'data-rte-list': 'default'}).find_all('a')

        for link in patent_links:
            prior_art_list.append(link.text)

    print(prior_art_list)
    return '; '.join(prior_art_list)


    
prior_art("https://patroll.unifiedpatents.com/contests/d4wk2MggiYTwqh4Qq",webdriver)
