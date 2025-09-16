from selenium.webdriver.common.by import By
import time

BASE_URL = "http://localhost:8080/index.html"


def test_transaction_creation_flow(driver):
    """
    Test transaction creation flow
    :param driver:
    :return:
    """
    driver.get(BASE_URL)

    # Use userId=1 from backend mock
    driver.find_element(By.ID, "txnUserId").send_keys("1")
    driver.find_element(By.ID, "amount").send_keys("200.50")
    driver.find_element(By.ID, "type").send_keys("transfer")
    driver.find_element(By.XPATH, "//button[text()='Create Transaction']").click()

    time.sleep(1)
    message = driver.find_element(By.ID, "txnMessage").text
    assert "Transaction created successfully!" in message