from selene import be, browser, have


class SearchResultsPage:
    def should_be_opened(self):
        browser.element('[data-testid="search_screen_non_empty_result"]').should(be.visible)
        return self

    def should_have_results(self):
        browser.element('[data-testid="appslist"]').should(be.visible)
        browser.all('[data-testid="app-card"]').first.should(be.visible)
        return self

    def first_result_should_contain(self, text: str):
        browser.all('[data-testid="app-card"]').first.should(have.text(text))
        return self
