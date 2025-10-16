import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# --- Konfigurasi utama ---
BLOG_FEED = "https://widodokapuk.blogspot.com/feeds/posts/default?alt=json"
OUTPUT = "mastersitemap.xml"

# --- Sitemap tambahan ---
EXTRA_SITEMAPS = [
    "https://sites.google.com/view/infokunews/sitemap.xml",
    "https://zonainfotips.github.io/blogsitemap/sitemap.xml"
]

print("🔄 Mengambil data feed dari Blogger...")
response = requests.get(BLOG_FEED)
feed = response.json()

urls = []
if "entry" in feed["feed"]:
    for entry in feed["feed"]["entry"]:
        link = next(l["href"] for l in entry["link"] if l["rel"] == "alternate")
        urls.append(link)

print(f"✅ Ditemukan {len(urls)} artikel dari Blogger")

# --- Buat struktur XML utama ---
root = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

# Tambahkan sitemap eksternal
for loc in EXTRA_SITEMAPS:
    sitemap = ET.SubElement(root, "sitemap")
    ET.SubElement(sitemap, "loc").text = loc
    ET.SubElement(sitemap, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Tambahkan sitemap Blogger
sitemap_blog = ET.SubElement(root, "sitemap")
ET.SubElement(sitemap_blog, "loc").text = "https://widodokapuk.blogspot.com/sitemap.xml"
ET.SubElement(sitemap_blog, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Tambahkan feed Blogger
sitemap_feed = ET.SubElement(root, "sitemap")
ET.SubElement(sitemap_feed, "loc").text = "https://widodokapuk.blogspot.com/feeds/posts/default?orderby=UPDATED"
ET.SubElement(sitemap_feed, "lastmod").text = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Simpan hasil XML
tree = ET.ElementTree(root)
tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)

print("🎉 Sitemap gabungan berhasil diperbarui:", OUTPUT)
