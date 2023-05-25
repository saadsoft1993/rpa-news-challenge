import datetime
import re
import time
import os
import shutil

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.Archive import Archive
from SeleniumLibrary.errors import ElementNotFound
from dateutil.relativedelta import relativedelta
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from news_locators import NewsLocators
from models import News
from config import OUTPUT


class FreshNews:
    """
    A class to scrape fresh news from a website.

    Args:
        search_phrase (str): The search phrase for news articles.
        sections (list): The list of sections to filter news articles.
        months (int): The number of months to retrieve news articles from.

    """

    def __init__(self, search_phrase, months, sections=None):
        self.browser = Selenium()
        self.base_url = 'https://www.nytimes.com/'
        self.locators = NewsLocators()
        self.news_list = []
        self.search_phrase = search_phrase
        self.sections = sections
        self.months = months
        self.files = Files()
        self.http = HTTP()
        self.lib = Archive()

    def setup(self):
        """
        Set up directories for storing output.

        """
        print('Setting up directories.')
        if not os.path.exists(OUTPUT):
            os.mkdir(OUTPUT)
        for filename in os.listdir(OUTPUT):
            file_path = os.path.join(OUTPUT, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        os.mkdir(f'{OUTPUT}/imgs')

    def open_site(self):
        """
        Open the news website.

        """
        print('Accessing the news website.')
        self.browser.open_headless_chrome_browser(self.base_url)

    def search_text(self):
        """
        Perform a search with the specified search phrase.

        """
        print(f'Searching with phrase: {self.search_phrase}')
        self.browser.click_element_if_visible(self.locators.search_button)
        self.browser.press_keys(self.locators.search_input, self.search_phrase)
        self.browser.press_keys(self.locators.search_input, 'RETURN')

    def select_section(self):
        """
        Select the specified sections to filter news articles.

        """
        if self.sections:
            print(f'Selecting sections: {", ".join(self.sections)}')
            self.browser.click_element_if_visible(self.locators.section_button)
            for section in self.sections:
                try:
                    self.browser.click_element_if_visible(self.locators.section_select.format(section=section))
                except Exception as e:
                    print(f'Failed to select section {section} with error: {str(e)}')
            self.browser.click_element_if_visible(self.locators.section_button)

    def select_newest(self):
        """
        Select the filter for newest news.

        """
        print('Selecting filter for newest news.')
        self.browser.wait_until_page_contains_element(self.locators.sort_button)
        self.browser.select_from_list_by_value(self.locators.sort_button, 'newest')

    def get_total_results_count(self):
        """
        Get the total number of results for the search.

        Returns:
            int: The total number of results.

        """
        raw_string = self.browser.find_element(self.locators.total_result).text
        try:
            total_value_string = re.search('of(.+?)results', raw_string).group(1)
        except AttributeError:
            total_value_string = '0'
        total_value_int = int(total_value_string.replace(' ', '').replace(',', ''))
        return total_value_int

    def get_date(self):
        """
        Get the date range for the search.

        Returns:
            tuple: The start and end dates in the format (to_date, from_date).

        """
        if self.months == 0:
            self.months = 1
        to_date = datetime.datetime.now()
        from_date = to_date - relativedelta(months=self.months)
        return to_date.strftime('%m/%d/%Y'), from_date.strftime('%m/%d/%Y')

    def set_date_range(self):
        """
        Set the date range for the search.

        """
        to_date, from_date = self.get_date()
        print(f'Setting date range from {from_date} to {to_date}.')
        self.browser.click_element_when_visible(self.locators.date_button)
        self.browser.click_element_when_visible(self.locators.specific_date)
        self.browser.input_text_when_element_is_visible(self.locators.start_date, from_date)
        self.browser.input_text_when_element_is_visible(self.locators.end_date, to_date)
        self.browser.press_keys(self.locators.end_date, 'RETURN')

    def read_news(self, news_index):
        """
        Read and store the details of a news article.

        Args:
            news_index (int): The index of the news article.

        """
        tries = 3
        while tries:
            try:
                search_result = self.browser.find_element(self.locators.news_result.format(index=news_index))
                break
            except ElementNotFound:
                tries -= 1
                time.sleep(2)
        else:
            print(f'Failed to read news at index {news_index}.')
            return None
        title = search_result.find_element(By.XPATH, self.locators.news_title).text
        print(f'Reading data for news with title: {title[:int(len(title)/2)]}....')
        date = search_result.find_element(By.XPATH, self.locators.news_date).text
        try:
            description = search_result.find_element(By.XPATH, self.locators.news_description).text
        except NoSuchElementException:
            description = ''
        try:
            image_url = search_result.find_element(By.XPATH, self.locators.news_image).get_attribute('src')
        except NoSuchElementException:
            image_url = ''
        if image_url:
            file_name = f'image{news_index}'
            file_path = f'{OUTPUT}/imgs/{file_name}'
            self.http.download(image_url, file_path)
        else:
            file_name = 'no image found'
        news_record = News(
            title=title,
            date=date,
            search_phrase=self.search_phrase,
            description=description,
            count=0,
            contains_amount=False,
            filename=file_name
        )
        self.news_list.append(news_record)

    def start(self):
        """
        Start the scraping process.

        """
        self.setup()
        self.open_site()
        self.search_text()
        self.set_date_range()
        self.select_newest()
        self.select_section()
        time.sleep(2)
        total_results = self.get_total_results_count()
        if not total_results:
            total_results = 0
        print(f'Total number of results found: {total_results}')
        for index in range(1, total_results + 1):
            if index % 10 == 0:
                try:
                    self.browser.click_element_when_visible(self.locators.pop_up_close_button)
                except AssertionError:
                    pass
                self.browser.scroll_element_into_view(self.locators.show_more)
                self.browser.click_element(self.locators.show_more)
            self.read_news(index)

    def end(self):
        """
        Finish the scraping process and store the collected data.

        """
        print('Creating Excel with collected news data.')
        self.files.create_workbook(f'{OUTPUT}/Latest News.xlsx', 'xlsx', f'News')
        for news in self.news_list:
            news_dict = news.dict()
            self.files.append_rows_to_worksheet(news_dict, header=True)
        self.files.save_workbook()
        self.files.close_workbook()
        self.lib.archive_folder_with_zip(f'{OUTPUT}/imgs', f'{OUTPUT}/images.zip', recursive=True)
        print('Collected data has been stored in output.')
