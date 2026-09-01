# Automation Artifact Review
1. Review Findings

Fixed sleep

Source menggunakan time.sleep(5) setelah memilih produk dan time.sleep(2) setelah add to cart

Masalahnya waktu tunggunya statis. Kalau CI lagi lemot test bisa duluan mencari element sebelum UI nya siap

2. Cart locator tidak sesuai dengan recorded step

(AppiumBy.XPATH, "//*[@content-desc='Cart']")

Tetapi recorded step memberikan:

content-desc: tap_to_view_cart

Ini merupakan masalah locator yang cukup kuat karena failure terjadi ketika test mencari cart navigation

Log menunjukkan:

step 3: locating cart navigation using content-desc=Cart
timeout: cart navigation was not located within 10 seconds

3. Tidak ada explicit wait

Pada CI timing aplikasi dapat berbeda dengan local environment. Explicit wait lebih sesuai karena test menunggu kondisi element yang sebenarnya

## Corrected Source

``` python
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WAIT_SECONDS = 15


@pytest.fixture()
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = "com.saucelabs.mydemoapp.android"
    options.app_activity = ".view.activities.SplashActivity"

    session = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options,
    )

    yield session
    session.quit()


def test_add_backpack_to_cart(driver):
    wait = WebDriverWait(driver, WAIT_SECONDS)

    product = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Sauce Labs Backpack")',
            )
        )
    )
    product.click()

    add_to_cart = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ACCESSIBILITY_ID,
                "tap_to_add_product_to_cart",
            )
        )
    )
    add_to_cart.click()

    cart = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ACCESSIBILITY_ID,
                "tap_to_view_cart",
            )
        )
    )
    cart.click()

    cart_product = wait.until(
        EC.presence_of_element_located(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Sauce Labs Backpack")',
            )
        )
    )

    assert cart_product.is_displayed()
```

1. Fixed sleep dihapus, jadi

WebDriverWait(driver, WAIT_SECONDS)

2. Locator cart diperbaiki, jadi

AppiumBy.ACCESSIBILITY_ID,
"tap_to_view_cart"

3. Add cart locator diperbaiki, jadi

AppiumBy.ACCESSIBILITY_ID,
"tap_to_add_product_to_cart"

## Kesimpulan

Test awal gagal 2 dari 10 kali di CI kemungkinan karna locator cart tidak sesuai dengan recorded step dan test masih menggunakan fixed sleep(). Source mencari content-desc='Cart' sedangkan locator yang direkam adalah tap_to_view_cart ini mmebuat cart kadang tidak ditemukan. Fixed sleep juga membuat test sensitif terhadap perbedaan timing antara local dan CI. Perbaikannya adalah menggunakan locator yang sesuai dan mengganti sleep() dengan explicit wait (WebDriverWait).
