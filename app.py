import streamlit as st
from serpapi import GoogleSearch
from openpyxl import Workbook
from io import BytesIO

def search_internet_for_contact_info(keywords, api_key):
    search_results = []
    
    for keyword in keywords:
        params = {
            "q": keyword,
            "api_key": api_key
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # თუ ვაგროვებთ შედეგებს, რომლებიც არ იქნებიან ბლოკირებული.
        if 'organic_results' in results:
            for result in results['organic_results']:
                title = result.get('title')
                link = result.get('link')
                
                # საკონტაქტო ინფორმაციის გატანა
                contact_info = []
                contact_page = requests.get(link)
                contact_page_soup = BeautifulSoup(contact_page.text, "html.parser")
                
                email = contact_page_soup.find("a", href=lambda href: href and "mailto:" in href)
                phone = contact_page_soup.find("a", href=lambda href: href and "tel:" in href)
                social = contact_page_soup.find_all("a", href=lambda href: href and "facebook.com" in href)
                name = contact_page_soup.find("h1") or contact_page_soup.find("h2")
                
                if email:
                    contact_info.append(f"Email: {email['href'][7:]}")
                if phone:
                    contact_info.append(f"Phone: {phone['href'][4:]}")
                if social:
                    contact_info.append(f"Social Links: {[a['href'] for a in social]}")

                search_results.append({"title": title, "link": link, "contact_info": contact_info, "name": name.text if name else "Unknown"})

    return search_results

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
api_key = "a42f5c23c7135b385e09db757e6b4a915cfe034ba963702a4478cf8d76b864aa"  # SerpAPI key

if st.button("ძიება"):
    results = search_internet_for_contact_info(keywords, api_key)
    excel_data = save_to_excel(results)
    st.success(f"{len(results)} შედეგი მოიძებნა!")
    st.download_button(
        label="გადმოწერე Excel ფაილი",
        data=excel_data,
        file_name="contact_info.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
