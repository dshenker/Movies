mfrom __future__ import division
from selenium.webdriver import Chrome
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
import re
from datetime import date, datetime
#import schedule
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import pytz
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
#import os
#import glob
today = date.today()
#dateToday = datetime.datetime.now(tz)
earnings = []
peopleInolved=[]
ratings = []
Productions = []
releaseDates  = []
percentsfull = []
popularities = []
metascores = []
starpowers= [] 
datesTaken = []
moneyMissed = []
opens = []
closes = []
def imdbScrape(movie, showtimes):
    webdriver = "/Users/dshenker/Desktop/chromedriver"
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox) # linux only
    chrome_options.add_argument("--headless")
    driver2 = Chrome(webdriver, options=chrome_options)
    movie = movie.replace("(2019)", " " )
    movie = movie.replace("(2020)", " " )
    movie = movie.replace(" ", '+')
    movie = movie.replace("&","and" )
    if(movie == 'BIRDS+OF+PREY+(AND+THE+FANTABULOUS+EMANCIPATION+OF+ONE+HARLEY+QUINN)'):
        movie = 'BIRDS+OF+PREY'
    print(movie)
    url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(movie)
    driver2.get(url)
    time.sleep(10)
    #wait = WebDriverWait(driver2, 10)
    #element = wait.until(EC.visibility_of_eleme
    # nt_located((By.CLASS_NAME, 'result_text')))
    try:
        a = driver2.find_element_by_class_name('result_text')
        link = a.find_element_by_tag_name('a')
        main_window = driver2.current_window_handle
        ActionChains(driver2) \
        .key_down(Keys.COMMAND) \
        .click(link) \
        .key_up(Keys.COMMAND) \
        .perform()
        driver2.switch_to.window(driver2.window_handles[1])
        time.sleep(10)
        rating = driver2.find_element_by_class_name('ratingValue')
        imdbRating = rating.find_element_by_tag_name('span')
        for s in showtimes:
            ratings.append(imdbRating.text)
        print('Rating: ' + imdbRating.text)
        summary = driver2.find_elements_by_class_name('credit_summary_item')
        peopleInolve = " "
        for s in summary:
            category = s.find_element_by_tag_name('h4')
            peopleInolve += category.text + ": " 
            print(category.text)
            items = s.find_elements_by_tag_name('a')
            for i in items: 
                peopleInolve += i.text + ", "
                print(i.text)
        for s in showtimes:
            peopleInolved.append(peopleInolve)
        bigDets = driver2.find_element_by_id('titleDetails')
        details = bigDets.find_elements_by_class_name('txt-block')
        prodsBig = " "
        for d in details:
            try:
                budgetcount = 0
                h4 = d.find_element_by_tag_name('h4')
                if(h4.text == 'Gross USA:'):
                    budget = d.text
                    for s in showtimes:
                        earnings.append(budget)
                    print( 'budget: ' + budget)
                elif(h4.text == 'Release Date:'):
                    release = d.text
                    for s in showtimes:
                        releaseDates.append(release)
                    print('release: ' + release)
                elif(h4.text == 'Production Co:'):
                    prods = d.find_elements_by_tag_name('a')
                    for p in prods:
                        prodsBig = ProdsBig + p.text + ", "
                        print('Prod: ' + p.text)
                    for s in showtimes:

                        Productions.append(prodsBig)
            
            except:
                pass
        if( len(earnings) < len(releaseDates)):
            for s in showtimes:
                earnings.append(0)
        barItems = driver2.find_elements_by_class_name('titleReviewBarItem')
        for b in barItems: 
            
            bsmall = b.text
            if(len(re.findall('Metascore', bsmall)) > 0):
                metascore = re.sub('[^0-9]','', bsmall)
                print('meta ' + metascore)
                for s in showtimes: 
                    metascores.append(metascore)
            elif(len(re.findall('Popularity', bsmall)) > 0):
                if ('(') in bsmall:
                    Result = bsmall[:bsmall.find('(') + 1]
                    popRating = re.sub('[^0-9]','', Result)
                else:
                    popRating = re.sub('[^0-9]','', bsmall)
                print('pop:' + popRating)
                for s in showtimes: 
                    popularities.append(popRating)
        CastList = driver2.find_element_by_class_name('cast_list')
        people = CastList.find_elements_by_class_name('primary_photo')
        StarPower = 0
        for i in range(9):
            link = people[i]
            link1 = link.find_element_by_tag_name('a').get_attribute('href')
            webdriver = "/Users/dshenker/Desktop/chromedriver"
            driver5 = Chrome(webdriver,options=chrome_options)
            driver5.get(link1)
            try:
                meter = driver5.find_element_by_id('meterHeaderBox')
                rating = meter.find_element_by_tag_name('a').text
            
                if(rating == 'SEE RANK'):
                    rating = 10000
                elif(rating == 'Top 5000'):
                    rating = 5000
                elif(rating == 'Top 500'):
                    rating = 500
                print(rating)
                StarPower+= (int)(rating)
            except:
                StarPower += 20000
            driver5.close()
            #driver2.close()
        for s in showtimes:
            starpowers.append(StarPower)
        driver2.switch_to_window(main_window)
    except:
        for s in showtimes: 
            starpowers.append(None)
            popularities.append(None)
            earnings.append(None)
            releaseDates.append(None)
            metascores.append(None)
            ratings.append(None)
            peopleInolved.append(None)
            print("No IMDB DATA FOUND")
    driver2.quit()

    
url1 = "https://www.fandango.com/amc-sunset-5-aacoz/theater-page"
url2 = "https://www.fandango.com/amc-lincoln-square-13-aabqi/theater-page"
#add path for local machine
def scraper(url, city):
    if(city == "LA"):
        tz = pytz.timezone('US/Pacific')
    else:
        tz = pytz.timezone('US/Eastern')
    dateToday = datetime.now(tz).date()
    dateToday = dateToday.strftime("%B %d, %Y")
    #dateToday = dateToday.replace(tzinfo = tz)
    #dateToday = dateToday.astimezone(tz)
    print(dateToday)
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox) # linux only
    chrome_options.add_argument("--headless")
   # driver = webdriver.Chrome(options=chrome_options)
    #webdriver = "/Users/andydazzo/Desktop/chromedriver"
    driver = Chrome(options=chrome_options)
   
    #NYCurl = "https://www.fandango.com/amc-lincoln-square-13-aabqi/theater-page"
    driver.get(url)
    wait = WebDriverWait(driver, 15)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'fd-movie')))
    movies = driver.find_elements_by_class_name('fd-movie')
    times = []
    titles = []
    prices = []
    RRGs= []
    amenitiesBig = []
    timesTaken = []
    # range 5 for sunset AMC, range 12 for nYC AMC
    for i in range(5):
        title = movies[i].find_element_by_tag_name("h3")
        print(title.text)
        RatingRuntimeGenre = movies[i].find_element_by_class_name("fd-movie__rating-runtime")
        print(RatingRuntimeGenre.text)
        showtimes = movies[i].find_elements_by_class_name("fd-movie__btn-list-item")
        imdbScrape(title.text, showtimes)
        count = 0
        if(city == "LA"):
            tz = pytz.timezone('US/Pacific')
        else:
            tz = pytz.timezone('US/Eastern')
        t = datetime.now(tz).time()
        print(t)
        for s in showtimes:
            count = count + 1
            try:
               # t = time.localtime()
               # current_time = time.strftime("%H:%M:%S", t)
               # tz = pytz.timezone('US/Eastern')
                current_time = datetime.now(tz).time()
                #d = datetime.datetime.now(pytz.timezone(tz))
                #datesTaken.append(d)
                print(current_time)
                timesTaken.append(current_time)
                titles.append(title.text + str(count))
                RRGs.append(RatingRuntimeGenre.text)
                showtime = s.find_element_by_tag_name('a')
                print(showtime.text)
                times.append(showtime.text)
                url = showtime.get_attribute('href')
                driver3 = Chrome(options=chrome_options)
                driver3.get(url)
                amenities = driver3.find_elements_by_class_name('amenityPopup')
                amenities1 = " "
                for a in amenities:
                    amenities1 += a.text + ", "
                    print(a.text)
                amenitiesBig.append(amenities1)
                price = driver3.find_element_by_class_name('pricePerTicket')
                print(price.text)
                prices.append(price.text)
                select = Select(driver3.find_element_by_class_name('qtyDropDown'))
                select.select_by_visible_text('1')
                button = driver3.find_element_by_id('NewCustomerCheckoutButton')
                button.click()
                try:
                    seats = driver3.find_element_by_id('frmSeatPicker')
                    #print(seats.get_attribute('innerHTML'))
                    x = seats.find_element_by_id('svg-Layer_1')
                    #driver.execute_script('arguments[0].click();', x)
                    y = x.get_attribute('innerHTML')
                    openSeats= []
                    openSeats = re.findall('availableSeat', y)
                    opens.append(len(openSeats))
                    closedSeats = re.findall('reservedSeat' , y)
                    closes.append(len(closedSeats))
                    totalSeats = len(openSeats) + len(closedSeats)
                    if(totalSeats == 0):
                        percentsfull.append(0.0)
                        moneyMissed.append(0.0)
                    else:
                        percentsfull.append(len(closedSeats) / totalSeats)
                        price = prices[len(prices) -1]
                        s = price.replace('$', '')
                        s1 = float(s)
                        moneyMissed.append(s1 * len(openSeats))
                        print('money missed ' + str((s1 * len(openSeats))))
                except:
                    percentsfull.append(0.0)
                    opens.append(0.0)
                    closes.append(0.0)
                    moneyMissed.append(0.0)
                #print(len(closedSeats) / totalSeats)


                driver3.close()
            
                
                
            except:
            # driver3.close()
                times.append(None)
                amenitiesBig.append(None)
                prices.append(None)
                percentsfull.append(None)
                moneyMissed.append(None)
                opens.append(None)
                closes.append(None)
                pass
            #driver.back()
    data = {
        'title' : titles,
        'Rating Runtime Genre': RRGs,
        'time': times,
        #'amenities' : amenitiesBig,
        'price' :prices,
        #'peopleInolved':  peopleInolved,
        #'IMDB rating': ratings,
        #'Earnings': earnings,
        #'Release Date': releaseDates,
        'percent full': percentsfull,
        #'Star Power' : starpowers,
        #'Popularity': popularities,
        #'MetaCritic Score': metascores,
        'Time Taken': timesTaken,
        'Money Missed' : moneyMissed,
        'Open Seats' : opens,
        'Taken Seats' : closes
    }
    try:
        df = pd.DataFrame(data)
        
        filename = "ProjectAutomationTest{}_{}_{}.csv".format(dateToday, current_time,city)
        df.to_csv(filename, encoding = 'utf-8')
       
        #automatically upload to google drive
   


    except:
        print("csv failed")
if __name__ == "__main__":
    print("started")
    scraper(url2,'NYC')
    count1 = 0 
    #schedule.every(45).minutes.do(scraper, url2,'NYC')
    #schedule.every(55).minutes.do(scraper, url1,'LA')
    while True:
        schedule.run_pending()
        earnings[:] = []
        peopleInolved[:] =[]
        ratings[:] = []
        Productions[:] = []
        releaseDates[:]  = []
        percentsfull[:] = []
        popularities[:] = []
        metascores[:] = []
        starpowers[:] = [] 
        datesTaken[:] = []
        moneyMissed[:] = []
        opens[:] = []
        closes[:] = []
        
       

    
        
   
   

