import pytest, yaml, pytest_html
from utils.api import APIClient
from selenium import webdriver
import os
from datetime import datetime
import base64

@pytest.fixture(scope="session")
def config():
    try:
        with open('config.yaml', 'r') as file:
            data = yaml.safe_load(file)["test_config"]
            return data
    except FileNotFoundError:
        print("Error: 'config.yaml' not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")


@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(config['base_url'], config['headers'])


@pytest.fixture
def driver(config):
    options = webdriver.ChromeOptions()
    if config["headless"]:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(config["timeout"])
    driver.set_window_size(1280, 800)
    yield driver
    driver.quit()


# ---------- Hook: add screenshots on failure ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Take screenshot if a UI test fails
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # take screenshot
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            filename = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)

            # also embed screenshot into HTML report
            extra = getattr(report, "extra", [])
            with open(filepath, "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode("utf-8")
            html = f'<div><img src="data:image/png;base64,{encoded_img}" ' \
                   f'style="width:600px;height:auto;" onclick="window.open(this.src)" /></div>'
            extra.append(pytest_html.extras.html(html))
            report.extra = extra