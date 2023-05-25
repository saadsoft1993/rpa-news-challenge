class NewsLocators:

    search_button = '//button[contains(@class, "css-tkwi90")]'
    search_input = '//input[@data-testid="search-input"]'

    section_button = '//label[text()="Section"]'
    section_select = '//span[text()="{section}"]//..//input'

    sort_button = '//select[@data-testid="SearchForm-sortBy"]'
    
    total_result = '//p[@data-testid="SearchForm-status"]'
    
    date_button = '//button[@data-testid="search-date-dropdown-a"]'
    specific_date = '//button[@aria-label="Specific Dates"]'
    start_date = '//input[@data-testid="DateRange-startDate"]'
    end_date = '//input[@data-testid="DateRange-endDate"]'
    
    news_result = '//li[@data-testid="search-bodega-result"][{index}]'
    news_title = './/h4'
    news_date = './/span[@data-testid="todays-date"]'
    news_description = './/p[@class="css-16nhkrn"]'
    news_image = './/img'

    show_more = '//button[contains(text(),"Show More")]'

    pop_up_close_button = '//button[contains(text(),"Accept")]'
