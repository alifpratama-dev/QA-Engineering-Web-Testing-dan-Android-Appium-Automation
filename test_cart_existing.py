import time
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


@pytest.fixture()
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = "com.saucelabs.mydemoapp.android"
    options.app_activity = ".view.activities.SplashActivity"
    session = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield session
    session.quit()


def test_add_backpack_to_cart(driver):
    driver.find_element(
        AppiumBy.XPATH,
        "//*[contains(@text, 'Sauce Labs Backpack')]",
    ).click()
    time.sleep(5)

    driver.find_element(
        AppiumBy.XPATH,
        "//*[@text='Add to cart']",
    ).click()
    time.sleep(2)

    driver.find_element(
        AppiumBy.XPATH,
        "//*[@content-desc='Cart']",
    ).click()

    assert "Backpack" in driver.page_source
