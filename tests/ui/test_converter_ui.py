import pytest
from playwright.sync_api import expect


@pytest.fixture(scope="module", autouse=True)
def ensure_browser_available(playwright):
    try:
        browser = playwright.chromium.launch()
        browser.close()
    except Exception as exc:
        pytest.skip(f"Playwright browser is unavailable in current environment: {exc}")


def test_converter_success(page, base_url):
    page.goto(base_url)
    page.locator("#from").select_option("USD")
    page.locator("#to").select_option("BYN")
    page.locator("#amount").fill("100")
    page.locator("#convert-btn").click()

    result = page.locator("#result")
    expect(result).to_contain_text("USD")
    expect(result).to_contain_text("BYN")


def test_converter_invalid_same_currency(page, base_url):
    page.goto(base_url)
    page.locator("#from").select_option("EUR")
    page.locator("#to").select_option("EUR")
    page.locator("#amount").fill("10")
    page.locator("#convert-btn").click()

    error = page.locator("#error")
    expect(error).to_contain_text("не должны совпадать")
