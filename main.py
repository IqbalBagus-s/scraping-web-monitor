from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/123.0.0.0 Safari/537.36'
opsi.add_argument(f'user-agent={user_agent}')

# Inisialisasi list untuk menyimpan driver, link, dan content
drivers = []
links = []
contents = []

# Jumlah halaman yang ingin di-scrape
jumlah_halaman = 10

# Membuat driver, mengambil screenshot, dan scraping
for i in range(1, jumlah_halaman+1):
    # Membuat driver
    driver = webdriver.Chrome(service=servis, options=opsi)
    driver.set_window_size(1300, 800)
    drivers.append(driver)

    # Mengambil link
    link = f"https://iprice.co.id/komputer/aksesoris/monitor/?page={i}&so=1"
    links.append(link)

    # Mengambil screenshot
    driver.get(link)
    time.sleep(5)  # Menunggu sebentar agar halaman selesai dimuat
    driver.save_screenshot(f"home{i}.png")

    # Mengambil content
    content = driver.page_source
    contents.append(content)

    # Menutup driver
    driver.quit()

# Melakukan scraping pada content
datas = [BeautifulSoup(content, "html.parser") for content in contents]
i = 1
list_nama,list_gambar,list_harga,list_ukuran_layar,list_resolusi_layar = [],[],[],[],[]
# Mengambil informasi produk dari setiap halaman
for data in datas:
    for area in data.find_all("a", class_=lambda x: x and x.startswith("zA")):
        print(f'monitor ke-{i}')
        nama = area.find('h3', class_="zE hd").text
        gambar = area.find('img')['src']
        harga = area.find('div', class_="z2").text
        ukuran_layar = area.find('div', class_="zH").text
        resolusi_layar = area.find('div', class_="zH zI").text

        list_nama.append(nama)
        list_gambar.append(gambar)
        list_harga.append(harga)
        list_ukuran_layar.append('')
        list_resolusi_layar.append('')
        i += 1
        print('-----------')
    for area in data.find_all("div", class_=lambda x: x and x.startswith("zA")):
        try:
            nama = area.find('h3', class_="zE zF qB").text
            gambar = area.find('img')['src']
            harga = area.find('div', class_="z3 wY hc h-").text

            print(f'monitor ke-{i}')
            list_nama.append(nama)
            list_gambar.append(gambar)
            list_harga.append(harga)
            list_ukuran_layar.append('')
            list_resolusi_layar.append('')
            i += 1
            print('-----------')
        except AttributeError:
            pass
# convert menjadi excel menggunakan pandas
df = pd.DataFrame({'Nama':list_nama,
                   'gambar':list_gambar,
                   'harga':list_harga,
                   'ukuran_layar':list_ukuran_layar,
                   'resolusi_layar':list_resolusi_layar
                   })
writer = pd.ExcelWriter('raw_data_monitor.xlsx')
df.to_excel(writer, sheet_name='sheet1', index=False)
writer._save()
