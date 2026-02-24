from selene import be, browser, command, have


class Footer:
    def scroll_to_footer(self):
        browser.element("footer").perform(command.js.scroll_into_view)
        return self

    def should_have_qr_code(self):
        browser.element('footer img[src*="qr"]').should(be.visible)
        return self

    def should_have_support_button(self):
        browser.all("footer a, footer button").by(have.text("Обратиться в поддержку")).first.should(
            be.visible
        )
        return self
