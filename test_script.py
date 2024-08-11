import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture()
def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def click_element(driver, element):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()


def test_payment_process(setup):
    driver = setup

    driver.get("https://app-staging.qlub.cloud/qr/ae/dummy-checkout/89/_/_/e4b9eac596")

    pay_now_button = driver.find_element(By.XPATH, "//*[@data-qa-id='landing-pay-now']")
    click_element(driver, pay_now_button)

    split_bill_button = driver.find_element(By.XPATH, "//*[@data-qa-id='billing-split-bill']")
    click_element(driver, split_bill_button)

    select_custom_button = driver.find_element(By.XPATH, "//*[@id='select-custom']")
    click_element(driver, select_custom_button)

    custom_amount_input = driver.find_element(By.XPATH, "//*[@name='amount']")
    custom_amount_input.send_keys("50")

    confirm_split_bill_button = driver.find_element(By.XPATH, "//*[@id='split-bill']")
    click_element(driver, confirm_split_bill_button)

    time.sleep(2)
    tip_5_button = driver.find_element(By.XPATH, "//*[@id='tip_5']").find_element(By.TAG_NAME, "div")
    click_element(driver, tip_5_button)

    iframe = driver.find_element(By.XPATH, "//*[@title='Secure payment input frame']")
    driver.switch_to.frame(iframe)

    card_number_input = driver.find_element(By.XPATH, "//*[@id='Field-numberInput']")
    card_number_input.send_keys("4242 4242 4242 4242")

    card_date_input = driver.find_element(By.XPATH, "//*[@id='Field-expiryInput']")
    card_date_input.send_keys("0226")

    card_security_input = driver.find_element(By.XPATH, "//*[@id='Field-cvcInput']")
    card_security_input.send_keys("100")

    driver.switch_to.default_content()

    pay_button = driver.find_element(By.XPATH, "//button[.//span[text()='Pay Now']]")
    click_element(driver, pay_button)

    time.sleep(5)
    success_icon = driver.find_element(By.XPATH, "//*[@data-testid='CheckRoundedIcon']")
    assert success_icon.is_displayed()
