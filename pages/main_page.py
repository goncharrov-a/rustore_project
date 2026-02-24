from selene import be, browser, have, query


class MainPage:
    def open(self):
        browser.open("/")
        return self

    def should_have_correct_title(self):
        browser.should(have.title_containing("RuStore официальный магазин приложений для Android"))
        return self

    def should_have_clickable_logo(self):
        browser.element('[data-testid="header_logo"]').should(be.clickable)
        return self

    def click_logo(self):
        browser.element('[data-testid="header_logo"]').should(be.clickable).click()
        return self

    def should_have_download_button(self):
        browser.element('[data-testid="goToDownloadInstruction"]').should(be.visible)
        return self

    def go_to_instruction(self):
        browser.element('[data-testid="goToDownloadInstruction"]').should(be.clickable).click()
        return self

    def open_search(self):
        browser.element('[data-testid="header_search_button"]').should(be.clickable).click()
        return self

    def should_have_search_button(self):
        browser.element('[data-testid="header_search_button"]').should(be.visible)
        return self

    def should_have_clickable_header_link(self, link_text: str):
        browser.all('[data-testid="header_routeLink"]').by(have.exact_text(link_text)).first.should(
            be.clickable
        )
        return self

    def header_link_href(self, link_text: str) -> str:
        link = browser.all('[data-testid="header_routeLink"]').by(have.exact_text(link_text)).first
        return link.get(query.attribute("href"))

    def header_link_target(self, link_text: str) -> str:
        link = browser.all('[data-testid="header_routeLink"]').by(have.exact_text(link_text)).first
        return link.get(query.attribute("target"))
