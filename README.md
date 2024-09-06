# Google Map Scraping

*“Larger the area longer it will take.”* - **Yoda**

## Introduction

This project provides a suite of Python scripts to scrape and extract information from Google Maps and Instagram based on a specified location and search term. It generates Excel files containing useful links and detailed information related to your search.

## Project Overview

- **`scrape_step_0_location.py`**: Geocodes the place to get its bounding box.
- **`scrape_step_1_links.py`**: Scrapes Google Maps links based on the search term and location.
- **`scrape_step_2_extract.py`**: Extracts detailed information from the Google Maps links.
- **`scrape_step_3_insta.py`**: Scrapes Instagram links related to the search term.
- **`scrape_step_4_check.py`**: Checks if the current location is within the specified "place name."
- **`scrape_step_5_compile.py`**: Orchestrates the execution of the above scripts and manages file creation.
- **`scrape_step_6_generate.py`**: Generates Excel files for storing the scraped data.
- **`scrape_step_7_user.py`**: User-configurable script to specify place and search term.

## Prerequisites

- **Python 3.7 or later** [Download](https://www.python.org/downloads/)
- **Visual Studio Code** or any other code editor, [VScode Download](https://code.visualstudio.com/download) 
- **Internet access** for scraping, [I wish I could give you free internet too...]()

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Vergil1000x/Google_Map_Scraper.git
   cd Google-Map-Scraper
   ```

2. **Install Dependencies**

   ```bash
   pip install geopy openpyxl selenium playwright beautifulsoup4 pandas
   playwright install
   ```

## Usage

1. **Configure `scrape_step_7_user.py`**

   Open `scrape_step_7_user.py` and set the `place_name` and `search_term` variables, on line 6 and line 7:

   ```python
   place_name = "Varanasi"
   search_term = "Aesthetic Clinic"
   ```

2. **Run the Script**

   Execute `scrape_step_7_user.py` to start the scraping process:

   ```bash
   python scrape_step_7_user.py
   ```

   This will generate three Excel files in your folder with the following format:

   - **`{place_name}_{search_term}_{timestamp}_input.xlsx`**: Contains Google Maps links.
   - **`{place_name}_{search_term}_{timestamp}_output.xlsx`**: Contains details of the search term in the given place.
   - **`{place_name}_{search_term}_{timestamp}_insta.xlsx`**: Contains Instagram links related to the search term.

## Examples

Example files generated might look like:

- `Varanasi_Aesthetic Clinic_2002-02-20_input.xlsx`
- `Varanasi_Aesthetic Clinic_2002-02-20_output.xlsx`
- `Varanasi_Aesthetic Clinic_2002-02-20_insta.xlsx`

## Tips

1. **Configure `scrape_step_2_extract.py`**

   In line 93, you can adjust the value `3` to any number to optimize performance based on your needs. For example:

   ```python
   semaphore = asyncio.Semaphore(3)
   ```

   Increasing the value allows more concurrent tasks, which might speed up scraping but could also increase resource usage.

2. **Configure `scrape_step_3_insta.py`**

   Similarly, in line 62, you can change the value `5` to better suit your performance requirements:

   ```python
   semaphore = asyncio.Semaphore(5)
   ```

   Adjusting this value can help balance between scraping speed and system load.

## Troubleshooting

- **Error: `Yada Yada Anything`**: Ask [ChatGPT](https://chatgpt.com/) or Ask [Google](https://www.google.com/) or Ask [Me](mailto:koushikmallick1000@gmail.com).

## Contributing

Contributions are welcome!
