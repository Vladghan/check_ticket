import time

import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def plane(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    while True:
        options = Options()
        options.add_argument("--mute-audio")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options
        )

        driver.implicitly_wait(5)
        with driver:
            driver.get('https://www.izhavia.su/')
            roles = driver.find_elements_by_css_selector('input.Select-input')
            time.sleep(2)
            roles[0].send_keys('Пулково, Санкт-Петербург')
            time.sleep(1)
            driver.find_element_by_class_name('Select-menu-outer').click()
            time.sleep(1)
            roles[1].send_keys('Ижевск')
            time.sleep(1)
            driver.find_element_by_class_name('Select-menu-outer').click()
            time.sleep(1)
            data = driver.find_elements_by_css_selector('.widget-dates input.form-control')
            data[0].click()
            time.sleep(1)
            nex = driver.find_element_by_class_name('react-datepicker__navigation--next')
            nex.click()
            nex.click()
            day = driver.find_element_by_css_selector('[aria-label="day-28"]')
            day.click()
            driver.find_element_by_class_name('widget__startButton').click()
            try:
                WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    f'body > div.app-container > section > div.content.content-search-result > div > div > wrap > search-mono-brand-cartesian-variants > div > div > div.flightTableWrap.mobileHide > div.flightTable > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > info-box > span > span > span')))
            except TimeoutException:
                continue
            soup = BeautifulSoup(driver.page_source, 'lxml')
            rez_dirt = soup.select_one(
                'body > div.app-container > section > div.content.content-search-result > div > div > wrap > search-mono-brand-cartesian-variants > div > div > div.flightTableWrap.mobileHide > div.flightTable > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > info-box > span > span > span')
            context.bot.send_message(chat_id=chat_id, text=rez_dirt.string)
            time.sleep(1800)


def main():
    updater = Updater('1436004577:AAGilhFgyXQaL_6tz3SKeyP2Hb7E5IyAjxU')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(command='plane', callback=plane))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
