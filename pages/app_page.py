from selene import be, browser, have


class AppPage:
    def open(self, path: str):
        browser.open(path)
        return self

    def should_be_loaded(self):
        browser.element('[data-testid="name"]').should(be.visible)
        browser.element('[data-testid="deepLinkButton"]').should(be.visible)
        return self

    def should_have_title(self, title_text: str):
        browser.should(have.title_containing("Госуслуги"))
        return self

    def should_have_name(self, app_name: str):
        browser.element('[data-testid="name"]').should(have.exact_text(app_name))
        return self

    def should_have_action_buttons(self):
        browser.element('[data-testid="deepLinkButton"]').should(be.visible)
        return self
