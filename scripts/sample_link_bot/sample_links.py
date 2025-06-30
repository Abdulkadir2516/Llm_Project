import requests
import time

API_KEY = "736007b41af56f73b2bef5274c4ae928146fa24ccbf0198bac1b4fcda2f8a014"

keywords = [
    "Sexual Harassment", "Doxing", "Cyberbullying", "Online Harassment",
    "Hate Speech", "Trolling", "Flaming", "Swatting",]

def google_search_links(query, api_key, total_results=30, results_per_page=10):
    links = []
    
    for start in range(0, total_results, results_per_page):
        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "start": start,
            "num": results_per_page
        }

        print(f"🔎 '{query}' - {start+1}. sonuçtan itibaren alınıyor...")
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            print(f"❌ Hata: {response.status_code} - {response.text}")
            break

        data = response.json()
        page_links = [r.get("link") for r in data.get("organic_results", []) if r.get("link")]
        links.extend(page_links)

        if not page_links:
            print("⚠️ Daha fazla sonuç bulunamadı.")
            break

        time.sleep(2)  # SerpAPI'nin rate limitine takılmamak için

    return links

if __name__ == "__main__":
    all_links = []

    for keyword in keywords:
        print(f"\n====================\n🔍 Kelime: {keyword}")
        keyword_links = google_search_links(keyword, API_KEY, total_results=30)
        all_links.extend(keyword_links)

        for link in keyword_links:
            print(link)

    with open("bulunan_linkler.txt", "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(link + "\n")

    print(f"\n✅ Toplam {len(all_links)} link 'bulunan_linkler.txt' dosyasına kaydedildi.")
