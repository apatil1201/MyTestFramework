from selenium.webdriver.common.by import By
import time
from utils.data_generation import get_user
BASE_URL = "http://localhost:8080/index.html"


def test_user_creation_flow(driver):
    """
    Test user creation flow
    :param driver:
    :return:
    """
    driver.get(BASE_URL)
    user = get_user()
    driver.find_element(By.ID, "name").send_keys(user["name"])
    driver.find_element(By.ID, "email").send_keys(user["email"])
    driver.find_element(By.ID, "accountType").send_keys(user["accountType"])
    driver.find_element(By.XPATH, "//button[text()='Register']").click()

    time.sleep(1)  # wait for response
    message = driver.find_element(By.ID, "message").text
    assert "User registered successfully!" in message


def test_error_message_validation(driver):
    """
    Validate correct error message displayed when missing email id
    :param driver:
    :return:
    """
    driver.get(BASE_URL)

    # Try registering without email
    driver.find_element(By.ID, "name").send_keys("Bob Error")
    driver.find_element(By.ID, "accountType").send_keys("basic")
    driver.find_element(By.XPATH, "//button[text()='Register']").click()

    time.sleep(1)
    message = driver.find_element(By.ID, "message").text
    assert "invalid user data" in message.lower()