from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time


class Product:
    def __init__(self):
        #self.name = None
        self.price = None
        self.asin = None
        self.difference = None

    def __repr__(self):
        #return str(self.difference)
        return self.asin + ', ' + self.price
        #Testing
        #return self.name + ', ' + self.price
    
    def __eq__(self, other):
        return self.price == other.price

        
def collect_page_data(browser, list_products) -> list:
    ''' collects product name & price and returns list of Product objects
    Input: 
        browser (object), list_products (list)
    Returns:
        (list): updated list with product objects
    '''
    #get rid of sponsored items with contains.
    items = browser.find_elements(By.XPATH, "//div[contains(@class, 's-result-item s-asin')]")
    items = WebDriverWait(browser,5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-result-item s-asin')]")))
    for i in items:

        #find name

        #try:
            #names = i.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
        #except:
            #names = i.find_element(By.XPATH, ".//span[@class='a-size-base-plus a-color-base a-text-normal']")

        new_product = Product()
        #new_product.name = names.text

        #find prices
        prices = i.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
        cents = i.find_elements(By.XPATH, ".//span[@class='a-price-fraction']")
        #combine dollar and cents
        if prices != [] and cents != []:
            total = prices[0].text + '.' + cents[0].text
        else:
            #price = 0 means that there were no price attached to this product.
            total = "0"
        new_product.price = total

        #getting asin number
        s = i.get_attribute("data-asin")
        new_product.asin = s
        list_products.append(new_product)

    return list_products



def main():
    '''Main
    '''

    #Asking the user for the product they want and the minimum star rating of the specified prodcut
    user_product = input("What product are you searching for, please be specific?: ")
    user_star_minimum = input("What minimum star rating are you looking for (ex: 4, 3, 2, 1), just enter the number?: ")
    user_max_price = float(input("What is your maximum budget for this item?: "))


    #This code opens the "amazon.com" site, which is the site where the whole star rating/price comparison will take place
    mods = webdriver.ChromeOptions()
    #to make web driver to run in the background instead of pop up. Uncomment below code.
    #mods.add_argument('--headless')
    browser = webdriver.Chrome(options = mods, service = Service(ChromeDriverManager().install()))
    browser.maximize_window()
    browser.get("https://www.amazon.com/")
    browser.implicitly_wait(5)

    
    #This code sends the specified product name to the search bar
    browser_product_search = browser.find_element(By.XPATH, "//*[@id='twotabsearchtextbox']")
    browser_product_search.send_keys(user_product)
    time.sleep(1)

    #This code clicks on the search button after the specified product name is entered
    browser_product_click = browser.find_element(By.XPATH, "//*[@id='nav-search-submit-button']")
    browser_product_click.click()
    time.sleep(1)
    
    #finds and clicks ratings as given
    path = "//i[@class='a-icon a-icon-star-medium a-star-medium-%s']" % user_star_minimum
    browser_star_click = browser.find_element(By.XPATH, path)
    browser_star_click.click()
    time.sleep(1)

    #Intializing to store Product objects
    list_products = []

    for page in range(3):
        collect_page_data(browser, list_products)
        browser_next_click = browser.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        browser_next_click.click()
        time.sleep(3)

    #Testing 
        #Uncomment below codes to see it work
    #for i in list_products:
        #print(i)
    
    mean = 0
    counter = 0
    for i in list_products:
        if i.price != '0'and float(i.price.replace(',','')) <= user_max_price:
            #i.price = float(i.price.replace(',',''))
            mean = mean + float(i.price.replace(',',''))
            counter += 1
    mean = mean / counter

   
    for i in list_products:
        if i.price != '0' and float(i.price.replace(',','')) <= user_max_price:
            i.difference = (mean - float(i.price.replace(',','')))**2
    
    
    for i in range(len(list_products)):
        if list_products[i].difference != None:
            for j in range(len(list_products)):
                if list_products[j].difference != None and list_products[j].difference >= list_products[i].difference:
                    list_products[j], list_products[i] = list_products[i], list_products[j]

    print("Your products are: (copy and past ASIN num on google/amazon):\n")
    for i in range(5):
        if list_products[i].difference != None:
            print(list_products[i])


    #Lastly, research and figure out a way to make this into an executable.
        #So we can share and use potentially. 
    

    #Ends webdriver...end
    browser.quit()


if '__main__':
    main()
