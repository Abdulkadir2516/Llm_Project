import requests
from bs4 import BeautifulSoup
import os

# Linklerin bulunduğu dosya yolu
links_file = "links.txt"
# Çıktıların kaydedileceği klasör
output_dir = "metinler"

os.makedirs(output_dir, exist_ok=True)

with open(links_file, "r", encoding="utf-8") as f:
    links = [line.strip() for line in f if line.strip()]

for idx, link in enumerate(links, 1):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Sayfadaki tüm metni al
        text = soup.get_text(separator="\n", strip=True)
        # Dosya adı oluştur
        output_path = os.path.join(output_dir, f"metin_{idx}.txt")
        with open(output_path, "w", encoding="utf-8") as out_f:
            out_f.write(text)
        print(f"{link} -> {output_path}")
    except Exception as e:
        print(f"Hata ({link}): {e}")