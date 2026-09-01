# Android Appium Smoke Test

Automation test sederhana untuk aplikasi **Sauce Labs My Demo App Android** https://github.com/saucelabs/my-demo-app-android/releases menggunakan:

* Python
* Appium Server
* UiAutomator2
* Android Emulator Pixel 7

APK yang digunakan:

mda-2.2.0-25.apk

## Test Scenario

Launch application → Select product → Add to cart → Open cart → Assert cart state

## Environment

Device : Pixel 7 Emulator
Android Version : Android 15
Appium : 3.7.0
UiAutomator2 : 8.5.0
Python : 3.13.7
APK : mda-2.2.0-25.apk

## Project Setup

Masuk ke folder project:

cd /d D:\demo-appium

Buat virtual environment:

python -m venv .venv

Aktifkan virtual environment:

.venv\Scripts\activate.bat

Install library yang digunakan:

pip install Appium-Python-Client pytest

Install driver UiAutomator2:

appium.cmd driver install uiautomator2

## Android SDK

File Android SDK:

C:\Users\ASUS\AppData\Local\Android\Sdk

Jika environment variable belum tersedia, jalankan:

set ANDROID_HOME=C:\Users\ASUS\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\ASUS\AppData\Local\Android\Sdk

Cek emulator:

adb devices

Emulator terdeteksi:

emulator-5554    device

## Run Appium

Jalankan Appium Server:

appium.cmd

Appium berjalan pada:

http://127.0.0.1:4723

Terminal Appium dibiarkan tetap berjalan

## Run Test

Buka terminal kedua dan masuk ke project:

cd /d D:\demo-appium

Aktifkan virtual environment:

.venv\Scripts\activate.bat

Jalankan smoke test:

python -m pytest tests\test_smoke.py -v

## Test Result

Hasil eksekusi:

tests/test_smoke.py::test_android_smoke_add_product_to_cart PASSED 1 passed in 28.04s

Test berhasil menjalankan:

1. Membuka aplikasi
2. Memilih Sauce Labs Backpack
3. Menambahkan produk ke cart
4. Membuka cart
5. Memastikan produk terdapat di cart
6. Memastikan quantity produk 1

### Products page

Memastikan halaman Products tampil:

assert products.text == "Products"

### Product

Memastikan produk yang dipilih adalah Sauce Labs Backpack:

assert product.text == "Sauce Labs Backpack"

### Cart badge

Jumlah produk pada cart harus 1:

assert cart_badge.text == "1"

### Cart product

Setelah cart dibuka produk harus tetap Sauce Labs Backpack:

assert cart_product.text == "Sauce Labs Backpack"

### Quantity

Quantity produk di cart harus 1:

assert quantity.text == "1"

### Accessibility ID

Digunakan untuk elemen yang memiliki accessibility label yang tersedia pada aplikasi

Contoh:

(AppiumBy.ACCESSIBILITY_ID, "title")

dan:

(AppiumBy.ACCESSIBILITY_ID, "View cart")

### XPath

XPath digunakan untuk mencari produk berdasarkan text:

(AppiumBy.XPATH,
 "//android.widget.TextView[@text='Sauce Labs Backpack']")

### ID

ID digunakan untuk elemen yang memiliki resource ID dari aplikasi.

Contoh:

(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")

dan:

(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")

## Failure Evidence

Jika test gagal pada saat test function dijalankan screenshot akan disimpan ke folder:

screenshots/

Nama screenshot:

smoke_test_failure.png

Screenshot digunakan sebagai evidence jika mengalami failure

## Troubleshooting

Selama setup ditemukan beberapa masalah yaitu:

### 1. PowerShell Execution Policy

Command `appium` tidak dapat dijalankan karena PowerShell memblokir `appium.ps1`

Solusi yang digunakan:

appium.cmd

### 2. UiAutomator2 belum tersedia

Awalnya test menghasilkan error:

Could not find a driver for automationName 'UiAutomator2'

Solusi:

appium.cmd driver install uiautomator2

### 3. Android SDK belum terbaca

Test kemudian menghasilkan:

Neither ANDROID_HOME nor ANDROID_SDK_ROOT environment variable was exported

Solusi:

set ANDROID_HOME=C:\Users\ASUS\AppData\Local\Android\Sdk
set ANDROID_SDK_ROOT=C:\Users\ASUS\AppData\Local\Android\Sdk

Setelah konfigurasi Android SDK diperbaiki, Appium dapat membuat session Android.

### 4. UiAutomator2 socket hang up

Pada salah satu percobaan muncul:

socket hang up

Emulator kemudian direstart dan test dijalankan kembali dan berhasil

## Final Execution

Final execution:

1 passed in 28.04s

Status:

PASSED