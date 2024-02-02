# Validator Nodes Status 
# Description
This project is designed to scrape the status of validator nodes from Neural Intenet website, compile the data into an Excel file, apply conditional formatting based on certain criteria, and then email the resulting file to a list of recipients. It utilizes Selenium for web scraping, pandas for data manipulation and styling, and smtplib for sending emails.

# Features
1. Scrapes validator node status data from a web page.
2. Compiles and formats data into an Excel file.
3. Applies conditional styling to data based on specific criteria.
4. Emails the Excel file to specified recipients.
   
# Prerequisites
Before you can run this script, you need to ensure you have the following installed:
1. Python 3.x
2. Pip (Python package installer)
   
# Installation
Clone this repository or download the source code.
Install the required Python packages by running the following command in your terminal or command prompt:

pip install -r requirements.txt
This will install the following packages:
pandas
selenium
openpyxl
python-dotenv (if you decide to use .env for environment variables)
Make sure you have a WebDriver installed (e.g., ChromeDriver for Google Chrome) and it's accessible from your PATH. This is required for Selenium to interact with web browsers.

# Configuration
Set up environment variables for your email credentials and other sensitive information. This can be done in several ways, depending on your operating system. For development purposes, you can also use a .env file and load it using the python-dotenv package.

email=<YOUR_EMAIL>
password=<YOUR_PASSWORD>
Modify the receiver_emails list in the script to include all intended recipients.

# Usage
To run the script, navigate to the directory containing the script in your terminal and execute:
python <script_name>.py
Replace <script_name> with the name of the script file.

# Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your enhancements.
