from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains


class BookingFiltration:
  def __init__(self, driver: WebDriver):
    self.driver = driver
    self.filter_bar = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="filters-sidebar"]')

  def apply_star_rating(self, *star_values): 
    star_filtration_box = self.filter_bar.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
    # Remove the cookie bar covering other DOM elements 
    self.driver.execute_script('document.getElementById("onetrust-banner-sdk").remove()')
    star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, 'div')
    for star_element in star_child_elements:
      for star_value in star_values:
        if star_element.get_attribute('innerHTML').strip() == f'{star_value} stars':
          ActionChains(self.driver).scroll_to_element(star_element).perform()
          star_element.click()
  
  def sort_by_price(self):
    element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
    element.click()
    dropdown_elements = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="sorters-dropdown"]').find_elements(By.CSS_SELECTOR, 'li')
    for el in dropdown_elements:
      if 'Price (lowest first)' in el.get_attribute('innerHTML'):
        el.click()
        break