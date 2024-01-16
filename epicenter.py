import folium
import base64
import uuid
from folium.features import CustomIcon
import os
from playwright.sync_api import sync_playwright
import time

def genmap(latitude, longitude, name):
    file_name = uuid.uuid4()
    m = folium.Map(
        location=[37.4, 137.3],
        tiles="cartodbdark_matter",
        attr="地震速報君",
        zoom_start=9
    )
    #icon = CustomIcon(
    #    icon_image='274c.png',
    #    icon_size=(25, 25),
    #    icon_anchor=(30, 30),
    #    popup_anchor=(3, 3)
    #)
    #folium.Marker(
    #    location=[latitude, longitude],
    #    icon=icon,
    #).add_to(m)

    m.save(f'temp/{file_name}.html')


    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath('.')}/temp/{file_name}.html")
        time.sleep(1)
        page.screenshot(path=f"{name}.png",full_page=True)
        browser.close()
    os.remove(f"temp/{file_name}.html")

genmap(0,0,'zen')