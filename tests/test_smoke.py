import os

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_android_smoke_add_product_to_cart():

    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "Android Emulator"

    options.app_package = "com.saucelabs.mydemoapp.android"
    options.app_activity = ".view.activities.SplashActivity"

    options.no_reset = True

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    wait = WebDriverWait(driver, 15)

    try:
        # =========================
        # Products page
        # =========================
        products = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "title"
                )
            )
        )

        assert products.text == "Products"

        # =========================
        # Select product
        # =========================
        product = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.XPATH,
                    "//android.widget.TextView[@text='Sauce Labs Backpack']"
                )
            )
        )

        product.click()

        # =========================
        # Product detail
        # =========================
        product_name = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.TextView[@text='Sauce Labs Backpack']"
                )
            )
        )

        assert product_name.text == "Sauce Labs Backpack"

        # =========================
        # Add product to cart
        # =========================
        add_cart = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "Tap to add product to cart"
                )
            )
        )

        add_cart.click()

        # =========================
        # Cart badge
        # Wait for actual state change
        # =========================
        cart_badge_locator = (
            AppiumBy.ID,
            "com.saucelabs.mydemoapp.android:id/cartTV"
        )

        wait.until(
            EC.text_to_be_present_in_element(
                cart_badge_locator,
                "1"
            )
        )

        cart_badge = driver.find_element(
            *cart_badge_locator
        )

        assert cart_badge.text == "1"

        # =========================
        # Open cart
        # =========================
        cart_button = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ACCESSIBILITY_ID,
                    "View cart"
                )
            )
        )

        cart_button.click()

        # =========================
        # Cart product
        # =========================
        cart_product = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    "//android.widget.TextView[@text='Sauce Labs Backpack']"
                )
            )
        )

        assert cart_product.text == "Sauce Labs Backpack"

        # =========================
        # Quantity
        # =========================
        quantity = wait.until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.ID,
                    "com.saucelabs.mydemoapp.android:id/noTV"
                )
            )
        )

        assert quantity.text == "1"

    except Exception:

        os.makedirs("screenshots", exist_ok=True)

        driver.save_screenshot(
            "screenshots/smoke_test_failure.png"
        )

        raise

    finally:

        driver.quit()