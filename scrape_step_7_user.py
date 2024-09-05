import asyncio
import scrape_step_5_compile
import scrape_step_6_generate

# Change values to what you need
place_name = "Varanasi"
search_term = "Aesthetics Clinic"


async def main():
    (input_file_path, output_file_path, insta_file_path) = scrape_step_6_generate.main(
        place_name, search_term
    )
    await scrape_step_5_compile.main(
        place_name, search_term, input_file_path, output_file_path, insta_file_path
    )


if __name__ == "__main__":
    asyncio.run(main())
