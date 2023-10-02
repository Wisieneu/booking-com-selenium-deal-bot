import os
import time
import types
import typing
from prettytable import PrettyTable

from selenium import webdriver
from selenium.webdriver.common.by import By

import booking.constants as const
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport

class Booking(webdriver.Chrome):
  def __init__(self, currency='USD', driver_path=r"C:\SeleniumDrivers") -> None:
    self.driver_path = driver_path
    os.environ['PATH'] += r";C:\SeleniumDrivers\chromedriver-win64"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    super(Booking, self).__init__(options=options)
    self.implicitly_wait(5)
    self.maximize_window()
    self.currency = currency
    
  def __exit__(self, exc_type, exc, traceback):
    self.quit()
  
  def land_first_page(self):
    self.get(f'{const.BASE_URL}/?selected_currency={self.currency}')
    
  def input_travel_destination(self, place):
    search_field = self.find_element(By.NAME, 'ss')
    search_field.clear()
    search_field.send_keys(place)
    time.sleep(1) # Autocompletion has to load with values replacing the suggested ones
    first_result = self.find_element(By.CSS_SELECTOR, 'div[tabindex="-1"]')
    first_result.click()
  
  def select_dates(self, check_in_date, check_out_date):
    check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in_date}"]')
    check_in_element.click()
    check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out_date}"]')
    check_out_element.click()
  
  def select_adults_count(self, count: int):
    self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]').click()
    self.find_element(By.CSS_SELECTOR, 'path[d="M20.25 12.75H3.75a.75.75 0 0 1 0-1.5h16.5a.75.75 0 0 1 0 1.5z"]').click()
    increase_adults_count_btn = self.find_element(By.CSS_SELECTOR, 'path[d="M20.25 11.25h-7.5v-7.5a.75.75 0 0 0-1.5 0v7.5h-7.5a.75.75 0 0 0 0 1.5h7.5v7.5a.75.75 0 0 0 1.5 0v-7.5h7.5a.75.75 0 0 0 0-1.5z"]')
    if count < 2: return
    for _ in range(1, count):
      increase_adults_count_btn.click()
      
  def search_bookings(self):
    self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    
  def apply_filters(self):
    filtration = BookingFiltration(driver=self)
    filtration.apply_star_rating(4, 5)
    filtration.sort_by_price()
  
  def report_results(self):
    results = self.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
    report = BookingReport(results)
    table = PrettyTable(field_names=["Hotel Name", "Hotel Price", "Hotel Score"])
    table.add_rows(report.pull_deal_box_attributes())
    print(table)