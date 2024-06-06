import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit.components.v1 as components
import os
import json

# Đọc thông tin đăng nhập từ biến môi trường
credentials_info = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
if credentials_info is None:
    st.error("GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable not set.")
    st.stop()

credentials_dict = json.loads(credentials_info)

# Thiết lập kết nối tới Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

try:
    # Mở Google Sheets và lấy dữ liệu
    sheet = client.open("Certificates").sheet1
    data = sheet.get_all_records()

    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(data)
    df.index += 1  # Đánh số thứ tự bắt đầu từ 1

    # Tạo cột chứa liên kết HTML
    df['Certificate Name'] = df.apply(lambda row: f'<a href="{row["Link"]}" target="_blank">{row["Certificate Name"]}</a>', axis=1)

    # Bỏ cột Link
    df = df.drop(columns=['Link'])

    # Tạo nội dung HTML với CSS để căn giữa và làm đẹp
    html_content = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        table {
            margin: 0 auto;
            border-collapse: collapse;
            width: 80%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
    <h1>My Certifications</h1>
    '''

    # Thêm bảng HTML
    html_content += df.to_html(escape=False, index=True, header=True)

    # Hiển thị nội dung HTML trên Streamlit
    components.html(html_content, height=600)
    
except gspread.SpreadsheetNotFound:
    st.error("The specified Google Sheet was not found. Please check the name and try again.")
except Exception as e:
    st.error(f"An error occurred: {e}")
