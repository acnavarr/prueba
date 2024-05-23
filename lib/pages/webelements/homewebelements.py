from selenium.webdriver.common.by import By


class HomeWebElements:
    where_label = (By.CSS_SELECTOR, ".P4Ui-title.P4Ui-mod-theme-dark")
    signin_button = (By.XPATH, "//span[text()='Iniciar sesión']")
    search_button = (By.CSS_SELECTOR, '.pageContent .SearchPage__FrontDoor .HPw7-form-fields-and-submit .HPw7-submit button')

    submenu_label=(By.XPATH,"//div[@class='dJtn-menu-item-title' and text()='{}']//ancestor::li")
