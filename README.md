# Web Scraping Project

## Overview

This project is a web scraper designed to extract and process data from websites using Selenium, BeautifulSoup, and Tor's SOCKS5 proxy. It handles various tasks including captcha detection, human-like interactions, and page content extraction.

## Features

- **Captcha Detection**: Identifies and handles captchas by prompting for manual resolution if detected.
- **Human-like Interactions**: Simulates human behavior with scrolling, hovering, drag-and-drop, and right-click actions.
- **Headless and Non-Headless Modes**: Supports running in both headless and non-headless modes.
- **Cookie Management**: Saves and reuses cookies for persistent sessions.
- **Content Extraction**: Extracts and cleans HTML content, then splits it into manageable chunks.

## Installation

### Prerequisites

- **Python 3.6+**
- **Geckodriver**: Firefox WebDriver for Selenium. Download from [here](https://github.com/mozilla/geckodriver/releases).

### Set Up Virtual Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

Create a `requirements.txt` file with the following content:

```
selenium
beautifulsoup4
fake-useragent
```

## Usage

1. **Update `firefox_driver_path`** in the `scrape_website` function to point to your `geckodriver` executable.

2. **Run the script**:
   ```bash
   python your_script_name.py
   ```

   Replace `your_script_name.py` with the name of your Python script file.

3. **Handle Captchas**: If a captcha is detected, the script will prompt you to solve it manually.

## Code Overview

- **`check_stupid_captcha(driver)`**: Checks for captchas on the page.
- **`solve_captcha_manually(driver)`**: Prompts user to solve captcha.
- **`wait_for_element_to_appear(driver, element_selector)`**: Waits for an element to appear.
- **`scroll_to_element(driver, element)`**: Scrolls to a specified element.
- **`hover_over_element(driver, element_selector)`**: Simulates hovering over an element.
- **`drag_and_drop(driver, source_selector, target_selector)`**: Performs drag-and-drop action.
- **`right_click_element(driver, element_selector)`**: Simulates right-click on an element.
- **`mimic_human(driver)`**: Simulates human-like scrolling behavior.
- **`get_page_info(driver)`**: Prints page title, URL, and element information.
- **`scrape_website(url)`**: Main function to scrape the website.
- **`extract_body_content(html_content)`**: Extracts body content from HTML.
- **`clean_body_content(body_content)`**: Cleans the extracted content.
- **`split_dom_content(dom_content, max_length=6000)`**: Splits content into manageable chunks.

## Troubleshooting

- **Captcha Handling**: Ensure that the browser window is visible if running in non-headless mode to solve captchas manually.
- **Proxy Issues**: Verify Tor is running and configured correctly for SOCKS5 proxy.

## Contributing

Feel free to submit issues or pull requests. For larger changes, please discuss with the maintainers first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust or expand the `README.md` as needed based on additional features or details specific to your project!
