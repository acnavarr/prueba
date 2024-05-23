import os

import allure
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from lib.helpers.generalhelpers import object_value, get_config, compress_and_save_to_temp, add_attchmen, capture
from lib.pages.basepage import BasePage
from lib.pages.homepage import HomePage
from utils.qase_service import QaseService


def before_all(context):
    driver = set_selenium_driver(context)
    driver.set_page_load_timeout('30')
    driver.maximize_window()

    context.web_driver = driver
    context.browser = BasePage(context)
    context.home = HomePage(context)

    contexts = {
        'home': context.home,
    }

    context.all_contexts = contexts
    context.test_run_id = 2


def after_scenario(context, scenario):
    scenario.failed_steps = context.failed_steps
    context.status = object_value(str(scenario.status))
    if get_config("qase","TEST_PLAN_ID"):
        status= scenario.status.name
        if len(scenario.tags)>0:
            compress_file=compress_and_save_to_temp(f"screenshots/{context.scenario.name}", f"test_case_{scenario.name.replace(' ','_')}")
            hash=add_attchmen(compress_file)
            QaseService.create_result(int(scenario.tags[0]),status,context.test_run_id,int(scenario.duration),scenario.name,scenario,hash)
    if len(scenario.tags)>0:
        QaseService.check_test_case_is_automated(int(scenario.tags[0]))


def after_all(context):
    context.browser.quit()
    return print("===== That's all folks =====")


def after_step(context, step):
    if step.exception is not None:
        context.step_error = step.exception
        context.failed_step = step.name
    if step.status == 'failed':
        context.failed_step = step.name
    try:
        context.failed_steps = []
        if step.status == 'failed':
            context.failed_steps.append(step.name)
    except Exception as e:
        print("error:", e)

def validate_scenario(scenario, context, steps):
    if scenario.status.name == 'failed':
        return print('Failed Step: ' + context.failed_step + '\n' + str(context.step_error))


def set_selenium_driver(context):
    env = context.config.userdata["driver"]
    if env == 'aws':
        driver = set_docker_driver()
    else:
        driver = set_local_driver()
    return driver


def set_local_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2
    })
    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def set_docker_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.set_capability('--lang', 'en-GB')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return webdriver.Remote(
        command_executor='http://0.0.0.0:4444/wd/hub',
        desired_capabilities=chrome_options.to_capabilities()
    )

def test_rail_report(context):
    return context.config.userdata["testrail"]
