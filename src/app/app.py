"""
Streamlit arayüzünün giriş noktası: sayfa ayarı, dil seçici, sayfa gezinmesi ve alt not.

Çalıştırma (repo kökünden; .streamlit/config.toml kökte olduğu için orada çalıştırılmalı):
  venv\\Scripts\\python.exe -m streamlit run src/app/app.py

Çok sayfalı yapı (st.navigation): şimdilik yalnız Görüntü sayfası var (Adım 7a, vize).
7b'de Video, Adım 8'de Kamera sayfası `pages` listesine bir satır eklenerek bağlanır.
"""

import streamlit as st

from core.texts import DEFAULT_LANG, LANGS, t

# Sayfa ayarı her çalıştırmada ilk Streamlit komutu olmalı. "wide": iki görüntü yan yana sığsın diye geniş düzen.
st.set_page_config(page_title=t("page_title"), layout="wide")

# Dil seçici kenar çubuğunun en üstünde. key="lang" → seçim st.session_state["lang"]'e yazılır,
# texts.t() de oradan okur. required=True: seçim boş bırakılamaz.
st.sidebar.segmented_control(
    t("lang_label"),
    options=list(LANGS),
    format_func=LANGS.get,
    default=DEFAULT_LANG,
    required=True,
    key="lang",
)

# Sayfalar. Yeni sayfa eklemek için bu listeye st.Page(...) eklenir.
pages = [
    st.Page("pages/goruntu.py", title=t("nav_image"), url_path="goruntu", default=True),
]
# Tek sayfa varken menü gereksiz → gizli; 7b'de sayfa sayısı artınca otomatik görünür.
nav = st.navigation(pages, position="sidebar" if len(pages) > 1 else "hidden")
nav.run()  # seçili sayfanın kodunu çalıştırır

# Alt not: her sayfanın en altında, seçili dilde, iki satır:
# 1) sorumluluk notu (Legal bölümündeki "son karar insanda" ilkesi), 2) veri seti atfı (lisans atıf istiyor).
# "  \n": Markdown'da aynı paragraf içinde satır sonu (iki satır arasında boşluk açmaz).
st.space("medium")
st.caption(f'{t("footer")}  \n{t("footer_dataset")}')
