import asyncio
import openpyxl
import urllib.parse
import scrape_step_0_location
import scrape_step_4_check
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def setup_browser():
    """Setup and return a configured Playwright browser instance."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)  # Set to True for headless mode
    context = await browser.new_context()
    return playwright, browser, context

async def scroll_within_div(page, search_term):
    """Scroll within the specific div to load more results."""
    div_selector = f"div[aria-label='Results for {search_term} near me']"

    try:
        await page.wait_for_selector(div_selector, timeout=20000)
        scroll_amount = 10000  # Number of pixels to scroll each time
        for _ in range(50):  # Adjust the number of scroll actions
            await page.evaluate(
                f"""
                var element = document.querySelector("{div_selector}");
                if (element) {{
                    element.scrollTop += {scroll_amount};
                }}
                """
            )
            await asyncio.sleep(0.1)  # Allow data to load
    except PlaywrightTimeoutError:
        print(f"Timeout while loading or finding the results for {search_term}.")

async def scrape_links(page, search_term, lat, lng, worksheet):
    """Scrape links for a given search term and location using Playwright."""
    try:
        # Encode the search term and construct URL
        encoded_search_term = urllib.parse.quote_plus(search_term + " near me")
        url = f"https://www.google.com/maps/search/{encoded_search_term}/@{lat},{lng},14z/data=!4m2!2m1!6e1?entry=ttu"
        await page.goto(url)
        print(f"Loading URL: {page.url}")

        # Scroll through results to load more data
        await scroll_within_div(page, search_term)

        # Extract and save links
        links = await page.query_selector_all("a[href]")
        found_links = 0
        for link in links:
            href = await link.get_attribute("href")
            if href and "maps" in href:
                worksheet.append([href])
                print(f"Found link: {href}")
                found_links += 1

        if found_links == 0:
            print(f"No valid links found for {search_term} at {lat}, {lng}")

    except Exception as e:
        print(f"Error: {e}")
        worksheet.append([f"Error: {e}"])

async def main(input_file_path=r"fx.xlsx", search_term="Aesthetics Clinic", place_name="Varanasi"):
    min_latitude, max_latitude, min_longitude, max_longitude = scrape_step_0_location.main(place_name)

    # Setup Playwright
    playwright, browser, context = await setup_browser()
    page = await context.new_page()

    workbook = None
    try:
        # Load the Excel workbook and worksheet
        workbook = openpyxl.load_workbook(input_file_path)
        worksheet = workbook.active

        # Scrape links for the given latitude and longitude ranges
        lat = min_latitude
        while lat <= max_latitude:
            lng = min_longitude
            while lng <= max_longitude:
                await asyncio.sleep(1)
                if scrape_step_4_check.main(place_name, lat, lng):
                    await scrape_links(page, search_term, lat, lng, worksheet)
                lng = round(lng + 0.1, 2)  # Adjust longitude increment as needed
            lat = round(lat + 0.1, 2)  # Adjust latitude increment as needed

        # Save the workbook
        workbook.save(input_file_path)
        print("Links saved successfully to Excel.")

    except Exception as e:
        print(f"Error saving workbook: {e}")

    finally:
        # Ensure all resources are properly closed
        if workbook:
            workbook.close()
        await context.close()
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Script interrupted by user.")
    except Exception as e:
        print(f"Error occurred: {e}")
