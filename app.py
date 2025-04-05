# davamate app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from io import BytesIO

def search_jobs_to_excel(keyword="რკინაბეტონი"):
    url = "https://www.jobs.ge"
    search_url = f"{url}/?q={keyword}"
    response = requests.get(search_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="list-group-item")

    wb = Workbook()
    ws = wb.active
    ws.append(["ვაკანსია", "კომპანია", "ლინკი"])

    for job in jobs:
        title_tag = job.find("a", class_="job-title")
        company_tag = job.find("div", class_="company-name")
        if title_tag and company_tag:
            title = title_tag.text.strip()
            company = company_tag.text.strip()
            link = url + title_tag['href']
            ws.append([title, company, link])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()

st.title("ვაკანსიების ძიება")
keyword = st.text_input("ძებნის სიტყვა", "რკინაბეტონი")

if st.button("ძიება"):
    excel_data = search_jobs_to_excel(keyword)
    st.success("ვაკანსიები მოიძებნა!")
    st.download_button(
        label="გადმოწერე Excel ფაილი",
        data=excel_data,
        file_name="jobs.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
