import streamlit as st
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from io import BytesIO

def search_internet_for_contact_info(keywords):
    search_url = "https://www.google.com/search?q={}"
    
    results = []
    for keyword in keywords:
        url = search_url.format(keyword)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.find_all("h3"):
            title = item.get_text()
            link = item.find_parent("a")["href"]
            
            # სცადეთ მიღებისას საკონტაქტო ინფორმაცია
            contact_info = []
            contact_page = requests.get(link)
            contact_page_soup = BeautifulSoup(contact_page.text, "html.parser")
            
            # ძიება საკონტაქტო ინფორმაციისთვის (მაგალითად, ელ. ფოსტა, ტელეფონი)
            email = contact_page_soup.find("a", href=lambda href: href and "mailto:" in href)
            phone = contact_page_soup.find("a", href=lambda href: href and "tel:" in href)
            social = contact_page_soup.find_all("a", href=lambda href: href and "facebook.com" in href) # ეს მარტო ფეისბუკისთვის
            name = contact_page_soup.find("h1") or contact_page_soup.find("h2") # პოსტის დასახელება

            if email:
                contact_info.append(f"Email: {email['href'][7:]}")
            if phone:
                contact_info.append(f"Phone: {phone['href'][4:]}")
            if social:
                contact_info.append(f"Social Links: {[a['href'] for a in social]}")

            results.append({"title": title, "link": link, "contact_info": contact_info, "name": name.text if name else "Unknown"})

    return results

def save_to_excel(results):
    wb = Workbook()
    ws = wb.active
    ws.append(["კომპანიის სახელი/ფიზიკური პირი", "საკონტაქტო ინფორმაცია", "ლინკი"])

    for result in results:
        contact_info = ", ".join(result["contact_info"]) if result["contact_info"] else "No contact info"
        ws.append([result["name"], contact_info, result["link"]])

    output = BytesIO()
    wb.save(output)
    return output.getvalue()

st.title("გლობალური ძიება ინტერნეტში")
keywords = [
    "ბეტონის სიმტკიცე", "შენობის ექსპერტიზა", "ნაგებობის ექსპერტიზა", 
    "ბეტონის გამოცდა", "საშენი მასალების სპეციალისტი", "სამშენებლო ლაბორატორია", 
    "ტექნიკური ექსპერტიზა", "ანკერების გამოცდა", "ხიმინჯების გამოცდა", 
    "ბეტონის გამოცდა", "დატკეპვნის კოეფიციენტი"
]

if st.button("ძიება"):
    results = search_internet_for_contact_info(keywords)
    excel_data = save_to_excel(results)
    st.success(f"{len(results)} შედეგი მოიძებნა!")
    st.download_button(
        label="გადმოწერე Excel ფაილი",
        data=excel_data,
        file_name="contact_info.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
