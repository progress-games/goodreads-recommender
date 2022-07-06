def init():
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    path = 'C:\Program Files (x86)\chromedriver.exe'

    driver = webdriver.Chrome(path)

    driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=39a05fa79cc07d548e50d6cf09db8e17')

    driver.find_element(By.NAME, 'email').send_keys('sca0023@elthamhs.vic.edu.au')
    driver.find_element(By.NAME, 'password').send_keys('123456')
    driver.find_element(By.ID, 'signInSubmit').click()

    return driver

def get_links(driver, page_no, ln):#, element_no):
    from selenium.webdriver.common.by import By

    driver.get(f"{ln}?page={page_no}")

        # Get element with tag name 'div'
    element = driver.find_elements(By.CLASS_NAME, 'bookTitle')

    links = [e.get_attribute('href') for e in element]
    
    shelf_links_raw = [link.replace('/show/', '/shelves/') for i, link in enumerate(links)]
    #shelf_links_raw = shelf_links_raw[element_no:len(shelf_links_raw)]

    shelf_links = []
    while len(shelf_links_raw) > 50:
        shelf_links_raw = shelf_links_raw[0:len(shelf_links_raw)-1]
    
    print(len(shelf_links_raw))
    for link in shelf_links_raw:
        driver.get(link)
        shelf_links.append(driver.current_url)
        print(shelf_links_raw.index(link))
    
    return shelf_links

if __name__ == '__main__':
    driver = init()
    print(get_links(driver, 1))