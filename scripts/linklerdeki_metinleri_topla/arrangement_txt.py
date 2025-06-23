import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Ortam değişkenlerini yükle
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Groq modeli tanımı
llm = ChatGroq(
    temperature=0.2,
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

def temizle_haber_metni(metin):
    prompt = (
        "Aşağıdaki metinde gereksiz kısımlar, reklamlar, yazar bilgileri ve başlıklar olabilir. "
        "Lütfen sadece haberin ana metnini sade bir şekilde döndür:\n\n"
        f"{metin}\n\nSadece haber metni:"
    )
    yanit = llm.invoke([HumanMessage(content=prompt)])
    return yanit.content.strip()

def klasordeki_dosyalari_temizle(kaynak_klasor, hedef_klasor):
    if not os.path.exists(hedef_klasor):
        os.makedirs(hedef_klasor)
        print(f"'{hedef_klasor}' klasörü oluşturuldu.")

    for i in range(63, 149):
        try:   
            dosya_adi = f"metin_{i}.txt"
            if dosya_adi.endswith(".txt"):
                kaynak_dosya_yolu = os.path.join(kaynak_klasor, dosya_adi)
                print(f"{dosya_adi} işleniyor...")

                with open(kaynak_dosya_yolu, "r", encoding="utf-8") as f:
                    metin = f.read()

                temiz_metin = temizle_haber_metni(metin)

                hedef_dosya_yolu = os.path.join(hedef_klasor, dosya_adi)
                with open(hedef_dosya_yolu, "w", encoding="utf-8") as f:
                    f.write(temiz_metin)

                print(f"Temizlenmiş dosya: {hedef_dosya_yolu}")
        except Exception as e:
            print(f"{dosya_adi} dosyası işlenirken hata oluştu: {e}")
            continue

if __name__ == "__main__":
    kaynak_klasor = "metinler"          # Orijinal metinlerin bulunduğu klasör
    hedef_klasor = "temiz_metinler"     # Temizlenmiş metinlerin kaydedileceği klasör
    klasordeki_dosyalari_temizle(kaynak_klasor, hedef_klasor)
