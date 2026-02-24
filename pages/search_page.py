from selene import be, browser, have


class SearchPage:
    def should_be_opened(self):
        browser.element('[data-testid="search_input"]').should(be.visible)
        return self

    def should_have_empty_input_and_placeholder(self):
        search_input = browser.element('[data-testid="search_input"]').should(be.visible)
        search_input.should(have.attribute("placeholder").value("Поиск приложений и игр"))
        return self

    def should_have_non_empty_trends(self):
        browser.element('[data-testid="apps_list"]').should(be.visible)
        browser.all('[data-testid="search_trend"]').first.should(be.visible)
        return self

    def type_query(self, text: str):
        browser.element('[data-testid="search_input"]').type(text)
        return self

    def submit(self):
        browser.element('[data-testid="search_input"]').press_enter()
        return self
