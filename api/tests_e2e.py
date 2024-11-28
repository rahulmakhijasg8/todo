from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
import time


class AdminPanelAddTaskTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.admin_username = "admin"
        self.admin_password = "12345"
        self.live_server_url = "http://localhost:8000"

    def test_admin_login_and_create_task(self):
        self.driver.get(self.live_server_url + "/admin/")
        time.sleep(5)

        self.driver.find_element(By.ID, "id_username").send_keys(
            self.admin_username
        )
        self.driver.find_element(By.ID, "id_password").send_keys(
            self.admin_password
        )

        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()
        time.sleep(2)
        self.assertIn("Site administration", self.driver.page_source)
        self.driver.find_element(By.LINK_TEXT, "Tasks").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "ADD TASK").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "id_title").send_keys(
            "Test Task from Selenium"
        )
        self.driver.find_element(By.ID, "id_description").send_keys(
            "This is a description of the test task created by Selenium."
        )

        self.driver.find_element(By.ID, "id_due_date_0").send_keys(
            "2024-11-30"
        )
        self.driver.find_element(By.ID, "id_due_date_1").send_keys("23:59:59")

        tags_filter_options = self.driver.find_element(By.ID, "id_tags_from")
        tags_filter_options.find_element(
            By.XPATH, "//option[text()='Urgent']"
        ).click()
        self.driver.find_element(By.CLASS_NAME, "selector-add").click()
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        time.sleep(2)

        task_title = self.driver.find_element(
            By.XPATH, "//a[text()='Test Task from Selenium']"
        )
        time.sleep(2)
        self.assertTrue(task_title.is_displayed())
        self.driver.find_element(
            By.LINK_TEXT, "Test Task from Selenium"
        ).click()

        time.sleep(2)

        title_input = self.driver.find_element(By.ID, "id_title")
        title_input.clear()
        title_input.send_keys("Updated Test Task from Selenium")

        description_input = self.driver.find_element(By.ID, "id_description")
        description_input.clear()
        description_input.send_keys("Updated task for recording video.")

        self.driver.find_element(By.ID, "id_due_date_0").clear()
        self.driver.find_element(By.ID, "id_due_date_0").send_keys(
            "2024-12-01"
        )
        self.driver.find_element(By.ID, "id_due_date_1").clear()
        self.driver.find_element(By.ID, "id_due_date_1").send_keys("23:59:59")

        time.sleep(2)

        tags_filter_options = self.driver.find_element(By.ID, "id_tags_to")
        tags_filter_options.find_element(
            By.XPATH, "//option[text()='Urgent']"
        ).click()
        self.driver.find_element(By.CLASS_NAME, "selector-remove").click()

        time.sleep(2)

        tags_filter_options = self.driver.find_element(By.ID, "id_tags_from")
        tags_filter_options.find_element(
            By.XPATH, "//option[text()='High Priority']"
        ).click()
        self.driver.find_element(By.CLASS_NAME, "selector-add").click()

        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 1000);")
        self.driver.find_element(By.ID, "id_status").click()
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, "//option[text()='Working']"
        ).click()
        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/main/div/div/"
            "form/div/fieldset/div[5]/div/div",
        ).click()

        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        time.sleep(2)

        updated_task_title = self.driver.find_element(
            By.XPATH, "//a[text()='Updated Test Task from Selenium']"
        )
        self.assertTrue(updated_task_title.is_displayed())
        time.sleep(2)

        self.driver.find_element(
            By.LINK_TEXT, "Updated Test Task from Selenium"
        ).click()

        time.sleep(2)

        self.driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

        self.driver.find_element(By.CLASS_NAME, "deletelink").click()

        time.sleep(2)

        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='submit']"
        ).click()

        time.sleep(2)
        self.assertEqual(
            self.driver.find_element(By.CLASS_NAME, "success").text,
            "The task “Updated Test Task from Selenium” "
            "was deleted successfully.",
        )

        self.driver.close()
