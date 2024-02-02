import logging
import pandas as pd
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os 

logging.basicConfig(level=logging.INFO)
email_user = os.environ.get('email')
email_password = os.environ.get('password')
smtp_server = 'smtp.gmail.com'
receiver_emails = [['itrat@neuralinternet.ai','ibtehajkhanoff@gmail.com','iamkulsoom6@gmail.com','asif@neuralinternet.ai','gunner@neuralinternet.ai','adrian@neuralinternet.ai','hansel@neuralinternet.ai','pankaj@neuralinternet.ai']]

def send_results_via_email(attachment_file):
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = "Validator_Nodes_Status"

    body = "Please find the Validators Node status."
    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(attachment_file)
    attachment = open(attachment_file, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)
    text = msg.as_string()

    try:
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, receiver_emails, text)
        server.quit()
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error in sending email: {e}")

def style_rows(row, total_rows, new_data_length):
    # Initialize default styles for each column in the row
    styles = [''] * len(row)

    # Apply bold style to the header row
    if row.name == 0:
        return ['font-weight: bold'] * len(row)

    if pd.isna(row['Subnet']) and pd.isna(row['UID']) and pd.isna(row['Updated']) and pd.isna(row['vTrust']):
        # Skip styling for empty rows
        return [''] * len(row)
    elif row.name == total_rows - new_data_length - 1:
        # Bold style for timestamp row, no background color
        return ['font-weight: bold'] * len(row)

 # Apply conditional styles for other rows
    try:
            updated = float(row['Updated'])
            vtrust = float(row['vTrust'])
    except (ValueError, TypeError):
        return [''] * len(row)  # Skip styling if values are not numeric

    if pd.notna(vtrust) and vtrust < 0.90:
            return ['background-color: red'] * len(row)
    elif pd.notna(updated) and updated > 500:
            return ['background-color: orange'] * len(row)
    elif pd.notna(vtrust) and vtrust >= 0.90 and pd.notna(updated) and updated <= 500:
        return ['background-color: green'] * len(row)


    return [''] * len(row)  # Default style for other cases


def apply_styling(data):
    return data.style.apply(style_rows, axis=1)

def is_valid_excel_file(file_path):
    try:
        pd.read_excel(file_path, engine='openpyxl')
        return True
    except Exception as e:
        logging.error(f"Invalid or corrupted Excel file: {e}")
        return False

def run_scraping():
    driver = webdriver.Chrome()
    driver.get('https://taostats.io/validators/neural-internet/')
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'staking_data_block')))
    except Exception as e:
        logging.error(f"Error waiting for elements: {e}")
        driver.quit()
        return None

    data_block = driver.find_elements(By.CLASS_NAME, 'staking_data_block')
    Subnet, UID, Updated, Vtrust = [], [], [], []

    for block in data_block:
        try:
            sn_text = block.find_element(By.XPATH, './/div[1]/div/small').text
            uid_text = block.find_element(By.XPATH, './/div[3]/div/small').text
            updated_text = block.find_element(By.XPATH, './/div[6]/div/small').text
            vtrust_text = float(block.find_element(By.XPATH, './/div[7]/div/small').text)
            
            Subnet.append(sn_text)
            UID.append(uid_text)
            Updated.append(updated_text)
            Vtrust.append(vtrust_text)
        except Exception as e:
            logging.error(f"Error extracting data: {e}")

    driver.quit()

    new_data = pd.DataFrame({'Subnet': Subnet, 'UID': UID, 'Updated': Updated, 'vTrust': Vtrust})
    excel_file_path = 'Validator_Node_Status.xlsx'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file exists and is valid
    if os.path.exists(excel_file_path) and is_valid_excel_file(excel_file_path):
        existing_data = pd.read_excel(excel_file_path, engine='openpyxl')
    else:
        # Create a DataFrame with a header row and two empty rows
        existing_data = pd.DataFrame(columns=['Subnet', 'UID', 'Updated', 'vTrust'])
        header_row = pd.DataFrame([['Subnet', 'UID', 'Updated', 'vTrust']], columns=['Subnet', 'UID', 'Updated', 'vTrust'])
        empty_rows = pd.DataFrame([["", "", "", ""]] *2, columns=['Subnet', 'UID', 'Updated', 'vTrust'])
        existing_data = pd.concat([empty_rows,header_row], ignore_index=True)

    # Concatenate with timestamp row and new data
    timestamp_row = pd.DataFrame([[current_time, "", "", ""]], columns=new_data.columns)
    new_data_with_timestamp = pd.concat([timestamp_row, new_data], ignore_index=True)

    combined_data = pd.concat([existing_data, new_data_with_timestamp], ignore_index=True)
    
   
        # Apply styling to the combined data
    styled_data = combined_data.iloc[1:].style.apply(lambda row: style_rows(row, len(combined_data), len(new_data)), axis=1)

     # Save the styled data to an Excel file
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        styled_data.to_excel(writer, index=False)
        # Set the title if creating a new file
        if not os.path.exists(excel_file_path):
            writer.book.title = "Neural Internet Validators Status"

    logging.info("Excel file updated with new styled data")

    return excel_file_path


def main():
    excel_file_path = run_scraping()
    if excel_file_path:
        send_results_via_email(excel_file_path)

if __name__ == "__main__":
    main()