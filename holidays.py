import requests
from bs4 import BeautifulSoup
import dateparser
import datetime
URL = 'https://uclouvain.be/fr/etudier/calendrier-academique-0.html'

def get_holidays():
    try:
        holiday_page = requests.get(URL)
    except:
        return []
    
    parsed_page = BeautifulSoup(holiday_page.content, 'html.parser')
    all_holidays = []

    for year in reversed(parsed_page.find_all("h2")):
        holidays = []
        for day in year.find_all_next(name='li'):
            day = day.extract()
            holiday_list = [x.text for x in day.find_all('em')]
            if len(holiday_list)!=0:
                holidays.append("".join(holiday_list))
        
        for holiday in holidays:
            try:
                date = dateparser.parse(holiday.split(":")[0].split(None, 1)[1].strip() + " " + year.text.split("-")[0])
                if date.month < 9:
                    old_date = date
                    date = date.replace(year=date.year + 1)
            
                all_holidays.append(date.date())
            except:
                print("[WARNING] an error occured, but html is hard")
    
    return all_holidays

weekend = [5, 6]

def official_tgif(holidays):
    """
    with Carbonelle et al. 2018-2019, and Pairet et al. 2020
    """
    today = datetime.date.today()
    weekend_now = [(x-today.weekday()) for x in weekend]
    holidays_now = [(x-today).days for x in holidays]
    merged_holidays = sorted(holidays_now+weekend_now)
    merged_holidays = list(filter(lambda x: x >= 0, merged_holidays))

    count = max(0, merged_holidays[0]-1)
    exponent = 0
    for i, number in enumerate(merged_holidays):
        if i != number - merged_holidays[0]:
            break
        else:
            exponent += 1
    
    if merged_holidays[0] == 0:
        exponent -= 1
        count = "NO WORK"
    return count, exponent



if __name__ == "__main__":
    holidays = get_holidays()
    print(official_tgif(holidays))
