from selenium import webdriver
from selenium.common import (
    WebDriverException,
    TimeoutException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import random

from logs.logger import logger


URL_LOGIN = "https://quotes.toscrape.com/login"
URL_QUOTES = "https://quotes.toscrape.com/"


def scrape_quotes():
    """
    Uses Selenium to log in to quotes.toscrape.com, scrape quotes from
    the main page, and return 3 random quotes as a single formatted string.
    """
    logger.info("Starting Selenium driver")

    try:
        driver = webdriver.Chrome()
    except WebDriverException as e:
        logger.error(f"Failed to start Selenium WebDriver: {e}")
        return "Failed to start web driver."

    try:
        logger.info("Opening login page")
        driver.get(URL_LOGIN)

        logger.info("Filling username and password")
        # Find username and password fields by ID and fill them
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("admin")

        logger.info("Submitting login form")
        # Click the submit button using CSS selector for input[type='submit']
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        logger.info("Waiting for quotes page to load")
        try:
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, "quote"))
            )
        except TimeoutException:
            logger.error("Timeout waiting for quotes to load")
            return "Login failed or quotes did not load in time."

        logger.info("Navigating to quotes page")
        driver.get(URL_QUOTES)

        logger.info("Collecting quotes")
        # Find all quote elements by class name
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        texts = [q.text for q in quotes]

        if not texts:
            logger.warning("No quotes found on the page")
            return "No quotes found."

        # Select 3 random quotes (or less if fewer available)
        selected = random.sample(texts, min(3, len(texts)))
        logger.info(f"Selected {len(selected)} random quotes")

        return "\n\n".join(selected)
    except NoSuchElementException as e:
        logger.error(f"Element not found during scraping: {e}")
        return "Error during scraping: element not found."

    except Exception as e:
        logger.error(f"Unexpected error during scraping: {e}")
        return "Unexpected error occurred during scraping."

    finally:
        logger.info("Closing the browser")
        driver.quit()
