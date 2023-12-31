import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

price_dict = {}
#seller_dict = {}
#price_list = []

class TestAkakce(unittest.TestCase):

    def setUp(self) -> None:
        self.driver = webdriver.Chrome()

    def test_akakce_website(self):
        driver = self.driver
        driver.get("https://www.akakce.com/cep-telefonu.html")
        driver.maximize_window()
        self.assertIn("Cep Telefonu", driver.title)

        #toplam sayfa sayısını bulur
        WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
            (By.XPATH,"/ html / body / div[3] / p")))
        page_count = driver.find_element(By.XPATH,"/ html / body / div[3] / p").text
        page_count = int(page_count.split()[4])

        page = 0

        # sonraki sayfaya tıklanması için döngü.
        for page in range(page_count):
            
            # ilgili XPATH teki "li" taglarinin sayısını bulur.(ürün satırlarını)
            li_elements_main = driver.find_elements(By.XPATH, "/html/body/div[3]/ul/li")
            li_elements_main_count = len(li_elements_main)
            print(li_elements_main_count)

            scroll_down = driver.find_element(By.XPATH, f"/html/body/div[3]/ul")
            driver.execute_script("arguments[0].scrollIntoView();", scroll_down)

            i = 0

            # üstte bulunan "li" taglerinin içinde döngü oluşturup, her "li" taginin içindeki "li" taglerinde dolaşır(fiyatlarda)
            for i in range(li_elements_main_count):
                # sayfayı aşağı kaydırır.
                WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(
                    (By.XPATH, f"/html/body/div[3]/ul/li[{i + 1}]")))
                scroll_down = driver.find_element(By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]")
                driver.execute_script("arguments[0].scrollIntoView();", scroll_down)

                # ana "li" taginin içindeki li sayısını (fiyat sayısını) bulur
                WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
                    (By.XPATH, f"/html/body/div[3]/ul/li[{i + 1}]")))
                li_elements_child = (driver.find_element(By.XPATH, f"/html/body/div[3]/ul/li[{i + 1}]/div")
                                     .find_elements(By.TAG_NAME, "li"))
                li_elements_child_count = len(li_elements_child)

                # ürün adını alır
                item_name = driver.find_element(By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]/a/span/h3").text
                #print(item_name)
                #price_list.clear()

                #price_list = []
                seller_dict = {}

                j = 0

                # fiyat taglerinde döngü yapar.
                for j in range(li_elements_child_count):

                    # satıcı isimlerini alır.
                    try:
                        try:
                            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
                                (By.XPATH, f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[2]/i")))
                            item_seller = (driver.find_element(
                                By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[2]/i/img")
                                           .get_attribute("alt"))
                            #print(item_seller)
                        except:
                            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
                                (By.XPATH, f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[2]/i")))
                            item_seller = driver.find_element(
                                By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[2]/i").text
                            #print(item_seller)
                    except:
                        item_seller = "Not Found"

                    # fiyatları tek tek alır.
                    try:
                        WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
                            (By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[1]/span")))
                        item_price = driver.find_element(
                            By.XPATH,f"/html/body/div[3]/ul/li[{i + 1}]/div/ul/li[{j + 1}]/a/span[1]/span").text
                        #print(item_price)
                    except:
                        item_price = "Not found"

                    #price_list.append(item_price)
                    seller_dict[item_seller] = item_price

                price_dict[item_name] = seller_dict

            next_button = driver.find_element(By.XPATH, "/html/body/div[3]/p/a[2]")
            next_button.click()
            
        seller_dict.clear()
        #price_list.clear()

        for item, prices in price_dict.items():
            print(item, prices)


    def tearDown(self) -> None:
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
