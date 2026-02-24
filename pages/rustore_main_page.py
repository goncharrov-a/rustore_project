from selene import be, browser, have, query


class RuStoreMainPage:
    def open(self):
        browser.open("/")
        return self

    def open_catalog(self):
        browser.open("/catalog")
        return self

    def should_have_main_title(self):
        browser.should(have.title_containing("RuStore официальный магазин приложений для Android"))
        return self

    def should_be_on_main_page(self):
        browser.should(have.url_containing("rustore.ru/"))
        browser.element('[data-testid="header_logo"]').should(be.visible)
        return self

    def click_logo(self):
        browser.element('[data-testid="header_logo"]').should(be.clickable).click()
        return self

    def header_link(self, title: str):
        return browser.all('[data-testid="header_routeLink"]').by(have.exact_text(title)).first

    def header_link_href(self, title: str) -> str:
        return self.header_link(title).get(query.attribute("href"))

    def header_link_target(self, title: str) -> str:
        return self.header_link(title).get(query.attribute("target"))

    def should_have_download_button(self):
        browser.element('[data-testid="goToDownloadInstruction"]').should(be.visible)
        return self

    def should_have_search_button(self):
        browser.element('[data-testid="header_search_button"]').should(be.visible)
        return self

    def open_search(self):
        browser.element('[data-testid="header_search_button"]').should(be.clickable).click()
        return self

    def type_search_query(self, text: str):
        browser.element('[data-testid="search_input"]').should(be.visible).type(text)
        return self

    def submit_search(self):
        browser.element('[data-testid="search_input"]').press_enter()
        return self

    def should_show_search_suggestions(self):
        browser.element('[data-testid="apps_list"]').should(be.visible)
        return self

    def should_have_search_suggestion(self, text: str):
        browser.element('[data-testid="apps_list"]').should(have.text(text))
        return self

    def should_show_search_results_screen(self):
        browser.element('[data-testid="search_screen_non_empty_result"]').should(be.visible)
        browser.element("h1").should(have.text("По запросу «госуслуги» найдено"))
        return self

    def should_have_results_list(self):
        browser.element('[data-testid="appslist"]').should(be.visible)
        browser.all('[data-testid="app-card"]').first.should(be.visible)
        return self

    def first_result_card(self):
        return browser.all('[data-testid="app-card"]').first

    def should_have_first_result_named(self, text: str):
        self.first_result_card().should(have.text(text))
        return self

    def open_first_result(self):
        self.first_result_card().click()
        return self

    def should_show_app_card(self, app_name: str):
        browser.element('[data-testid="name"]').should(have.exact_text(app_name))
        browser.element('[data-testid="deepLinkButton"]').should(be.visible)
        browser.element('[data-testid="chips"]').should(be.visible)
        browser.element('[data-testid="developerInfo"]').should(be.visible)
        browser.all('[data-testid="permission"]').first.should(be.visible)
        return self

    def open_developer_page_from_card(self):
        browser.element('[data-testid="developerInfo"] [data-testid="link"]').click()
        return self

    def should_be_on_developer_page(self):
        browser.should(have.url_containing("/catalog/developer/"))
        browser.should(have.title_containing("приложений от Министерство цифрового развития"))
        return self
