# Otodom Scraper 🏠🚀

Welcome to the **Otodom Scraper Project** — a smart tool that extracts real estate offers from [Otodom.pl](https://www.otodom.pl/) based on your custom search filters.

This is just the beginning: our goal is to build a complete application for property analysis, market insights, and predictive price estimation!

---

## 🚀 Project Vision

🔹 Allow users to easily select their search filters (city, price range, surface area, number of rooms, and more)  
🔹 Automatically scrape matching real estate listings  
🔹 Export all data neatly into Excel  
🔹 Build dynamic dashboards and quick market summaries  
🔹 Predict the market value of a property based on collected data using Machine Learning

All with a clean, user-friendly web application. Coming soon!

---

## 🛠️ Current Features (v0.01 Alpha)

- [x] Smart web scraping from Otodom based on a predefined filtered link
- [x] Export results to Excel (`excel_exports/`) with price, area, number of rooms, location, and direct listing URL
- [x] Handles multiple pages of offers automatically
- [x] Cookie consent popup handling
- [x] Basic error handling and stability improvements

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Selenium** (Web Scraping)
- **Pandas** (Data Processing)
- **OpenPyXL** (Excel export)
- (Coming soon) **Streamlit** (User GUI & dashboard visualization)
- (Coming soon) **Scikit-Learn** (Price prediction using ML)

## 🚀 How to Run

1. Clone the repository
2. Install dependencies (`pip install -r requirements.txt`)
3. Download matching ChromeDriver and place it in `chromedriver/`
4. Run:
   ```bash
   python src/otodom_scraper.py
5. Find your exported Excel file in excel_exports/
