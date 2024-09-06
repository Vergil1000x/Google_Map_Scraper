import asyncio
import pandas as pd
import scrape_step_1_links
import scrape_step_2_extract
import scrape_step_3_insta
import scrape_step_4_check


async def main(
    place_name="Varanasi",
    search_term="Aesthetics Clinic",
    input_file_path=r"fx.xlsx",
    output_file_path=r"fxout.xlsx",
    insta_file_path=r"fxinsta.xlsx",
):
    # Step 1: Extract links
    await scrape_step_1_links.main(input_file_path, search_term, place_name)

    # Remove duplicates from the input file
    df = pd.read_excel(input_file_path)
    df_cleaned = df.drop_duplicates()
    df_cleaned.to_excel(input_file_path, index=False)

    # Step 2: Extract information
    await scrape_step_2_extract.main(input_file_path, output_file_path)

    # Step 3: Extract Instagram links
    await scrape_step_3_insta.main(output_file_path, insta_file_path)

    # Remove duplicates from the Instagram file
    df = pd.read_excel(insta_file_path)
    df_cleaned = df.drop_duplicates()
    df_cleaned.to_excel(insta_file_path, index=False)

    # Define a function to check if a URL is unwanted
    def is_unwanted_url(url):
        if pd.isna(url):  # Skip if URL is NaN
            return False
        url_str = str(url)
        return any(
            pattern in url_str
            for pattern in [
                "instagram.com/p/",
                "instagram.com/v/",
                "instagram.com/reel/",
                "instagram.com/reels/",
            ]
        )

    # Reload the file after cleanup
    df = pd.read_excel(insta_file_path)  # Reload the file after cleanup
    if df.shape[1] > 0:  # Ensure there is at least one column
        df_cleaned = df[~df.iloc[:, 0].apply(is_unwanted_url)]
        df_cleaned.to_excel(insta_file_path, index=False)
    else:
        print("DataFrame does not contain any columns.")


# Run the asynchronous functions
if __name__ == "__main__":
    asyncio.run(main())
