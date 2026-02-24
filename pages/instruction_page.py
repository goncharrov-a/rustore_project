from selene import be, browser, have, query


class InstructionPage:
    def should_be_opened(self):
        browser.should(have.url_containing("/instruction"))
        return self

    def should_have_correct_title(self):
        browser.should(have.title_containing("Скачать RuStore"))
        return self

    def should_have_download_button(self):
        browser.element('[data-testid="download_link"]').should(be.visible)
        return self

    def should_have_download_link_attrs(self):
        link = browser.element('[data-testid="download_link"]')
        href = link.get(query.attribute("href"))
        assert href is not None and href.endswith("/download")
        assert link.get(query.attribute("target")) == "_blank"
        return self
