from selenium import webdriver
import time

chrome_driver_path = "/Users/user/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]

stop_time = time.time() + (60 * 5)
cookie = driver.find_element_by_id("cookie")
while True:
    timeout = time.time() + 5
    while True:
        cookie.click()
        if time.time() > timeout:
            all_prices = driver.find_elements_by_css_selector("#store b")
            item_prices = []
            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)
            cookie_upgrades = {}

            for n in range(len(item_prices)):
                cookie_upgrades[item_prices[n]] = item_ids[n]
            money_element = driver.find_element_by_id("money").text
            if "," in money_element:
                money_element = money_element.replace(",", "")
            num_cookies = int(money_element)

            afford_upgrades = {}
            for cost, id in cookie_upgrades.items():
                if num_cookies > cost:
                    afford_upgrades[cost] = id
            try:
                highest_price = max(afford_upgrades)
            except ValueError:
                pass
            else:
                purchase_id = afford_upgrades[highest_price]

                driver.find_element_by_id(purchase_id).click()

            timeout = time.time() + 5
        if time.time() > stop_time:
            break
    break
print(driver.find_element_by_id("cps").text)
