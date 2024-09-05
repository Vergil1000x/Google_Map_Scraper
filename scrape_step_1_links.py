import time
import openpyxl
import urllib.parse
import scrape_step_0_location
import scrape_step_4_check
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def setup_webdriver(service_path):
    """Setup and return a configured WebDriver instance."""
    service = Service(service_path)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=options)


def scrape_links(driver, search_term, lat, lng, worksheet):
    """Scrape links for a given search term and location."""
    try:
        # Encode the search term and construct URL
        encoded_search_term = urllib.parse.quote_plus(search_term)
        url = f"https://www.google.com/maps/search/{encoded_search_term}/@{lat},{lng},14z/data=!4m2!2m1!6e1?entry=ttu"
        driver.get(url)
        print(f"Loading URL: {driver.current_url}")

        # Wait for the results container to be visible
        divx = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//div[@aria-label='Results for {search_term}']")
            )
        )

        # Scroll through results to load more data
        scroll_count = 0
        while scroll_count < 150:  # Adjust as needed
            driver.execute_script("arguments[0].scrollBy(0, 1000000);", divx)
            time.sleep(0.1)  # Allow data to load
            scroll_count += 1

        # Extract and save links
        links = driver.find_elements(By.XPATH, "//a[@href]")
        found_links = 0  # Counter for debugging purposes
        for link in links:
            href = link.get_attribute("href")
            if href and "maps" in href:
                worksheet.append([href])
                print(f"Found link: {href}")
                found_links += 1

        if found_links == 0:
            print(f"No valid links found for {search_term} at {lat}, {lng}")

    except TimeoutException:
        print(
            f"Timeout while loading or finding elements for {search_term} at {lat}, {lng}"
        )
        worksheet.append(["Timeout error"])
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        worksheet.append(["Element not found"])
    except Exception as e:
        print(f"Error: {e}")
        worksheet.append([f"Error: {e}"])


def main(
    input_file_path=r"fx.xlsx",
    search_term="Aesthetics Clinic",
    place_name="Varanasi",
):

    (min_latitude, max_latitude, min_longitude, max_longitude) = (
        scrape_step_0_location.main(place_name)
    )

    # Setup WebDriver
    driver = setup_webdriver(r"chromedriver.exe")

    # Load the Excel workbook and worksheet
    workbook = openpyxl.load_workbook(input_file_path)
    worksheet = workbook.active

    # Scrape links for the given latitude and longitude ranges
    lat = min_latitude
    while lat <= max_latitude:
        lng = min_longitude
        while lng <= max_longitude:
            time.sleep(1)
            if scrape_step_4_check.main(place_name, lat, lng):
                scrape_links(driver, search_term, lat, lng, worksheet)
            lng += 0.1  # Adjust longitude increment as needed
        lat += 0.1  # Adjust latitude increment as needed

    # Save the workbook and clean up
    try:
        workbook.save(input_file_path)
        print("Links saved successfully to Excel.")
    except Exception as e:
        print(f"Error saving workbook: {e}")

    workbook.close()
    driver.quit()


if __name__ == "__main__":
    main()
