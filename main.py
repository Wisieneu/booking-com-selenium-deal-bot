from booking.booking import Booking

import time
try:
  with Booking() as bot:
    bot.land_first_page()
    bot.input_travel_destination(input("Where would you like to go?\n"))
    bot.select_dates(check_in_date=input("What is the check in date? (Format YYYY-MM-DD)\n"), check_out_date=input("What is the check out date? (Format YYYY-MM-DD)\n"))
    bot.select_adults_count(int(input("Input the adult people count:\n")))
    bot.search_bookings()
    bot.apply_filters()
    bot.refresh()
    bot.report_results()

except Exception as e:
  if 'in PATH' in str(e):
    print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Chrome Webdrivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/to/your/folder/ \n'
        )
  else: 
    raise
  