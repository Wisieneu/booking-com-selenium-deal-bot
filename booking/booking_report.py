# This file contains logic behind result reporting

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class BookingReport:
  def __init__(self, results) -> None:
    self.results = results
    
  def pull_deal_box_attributes(self):
    collection = []
    for deal_box in self.results:
      hotel_name = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
      hotel_price = deal_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').strip()
      score_index = str(deal_box.get_attribute('innerHTML')).find('Scored ') + 7
      hotel_score = f"{deal_box.get_attribute('innerHTML')[score_index: score_index+3]} / 10"

      collection.append([hotel_name, hotel_price, hotel_score]) 
    return collection