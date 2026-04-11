"""
FB Ad Template Generator — Streamlit web version
"""

import streamlit as st
import openpyxl
import os
import io
import zipfile
import json
import random
from datetime import datetime, timedelta

# ─── Константы ───────────────────────────────────────────────────────────────

HEADERS = [
    'Campaign ID', 'Creation Package Config ID', 'Campaign Name', 'Special Ad Categories',
    'Special Ad Category Country', 'Campaign Status', 'Campaign Objective', 'Buying Type',
    'Campaign Spend Limit', 'Campaign Daily Budget', 'Campaign Lifetime Budget',
    'Campaign Bid Strategy', 'Tags', 'Campaign Is Using L3 Schedule', 'Campaign Start Time',
    'Campaign Stop Time', 'Product Catalog ID', 'Campaign Page ID', 'New Objective',
    'Buy With Prime Type', 'Is Budget Scheduling Enabled For Campaign',
    'Campaign High Demand Periods', 'Buy With Integration Partner', 'Ad Set ID',
    'Ad Set Run Status', 'Ad Set Lifetime Impressions', 'Ad Set Name', 'Ad Set Time Start',
    'Ad Set Time Stop', 'Ad Set Daily Budget', 'Destination Type', 'Ad Set Lifetime Budget',
    'Rate Card', 'Ad Set Schedule', 'Use Accelerated Delivery', 'Frequency Control',
    'Ad Set Minimum Spend Limit', 'Ad Set Maximum Spend Limit',
    'Is Budget Scheduling Enabled For Ad Set', 'Ad Set High Demand Periods', 'Link Object ID',
    'Optimized Conversion Tracking Pixels', 'Optimized Custom Conversion ID',
    'Optimized Pixel Rule', 'Optimized Event', 'Custom Event Name', 'Link', 'Application ID',
    'Product Set ID', 'Place Page Set ID', 'Object Store URL', 'Offer ID',
    'Offline Event Data Set ID', 'Countries', 'Cities', 'Regions', 'Electoral Districts',
    'Zip', 'Addresses', 'Geo Markets (DMA)', 'Global Regions', 'Large Geo Areas',
    'Medium Geo Areas', 'Small Geo Areas', 'Metro Areas', 'Neighborhoods', 'Subneighborhoods',
    'Subcities', 'Location Types', 'Location Cluster IDs', 'Location Set IDs',
    'Excluded Countries', 'Excluded Cities', 'Excluded Large Geo Areas',
    'Excluded Medium Geo Areas', 'Excluded Metro Areas', 'Excluded Small Geo Areas',
    'Excluded Subcities', 'Excluded Neighborhoods', 'Excluded Subneighborhoods',
    'Excluded Regions', 'Excluded Electoral Districts', 'Excluded Zip', 'Excluded Addresses',
    'Excluded Geo Markets (DMA)', 'Excluded Global Regions', 'Excluded Location Cluster IDs',
    'Gender', 'Age Min', 'Age Max', 'Education Status', 'Fields of Study',
    'Education Schools', 'Work Job Titles', 'Work Employers', 'College Start Year',
    'College End Year', 'Interested In', 'Relationship', 'Family Statuses', 'Industries',
    'Life Events', 'Income', 'Multicultural Affinity', 'Household Composition', 'Behaviors',
    'Connections', 'Excluded Connections', 'Friends of Connections', 'Locales',
    'Site Category', 'Unified Interests', 'Excluded User AdClusters',
    'Broad Category Clusters', 'Targeting Categories - ALL OF', 'Custom Audiences',
    'Excluded Custom Audiences', 'Flexible Inclusions', 'Flexible Exclusions',
    'Advantage Audience', 'Individual Setting', 'Age Range', 'Targeting Optimization',
    'Targeting Relaxation', 'Product Audience Specs', 'Excluded Product Audience Specs',
    'Targeted Business Locations', 'Dynamic Audiences', 'Excluded Dynamic Audiences',
    'Beneficiary', 'Payer', 'Publisher Platforms', 'Facebook Positions',
    'Instagram Positions', 'Audience Network Positions', 'Messenger Positions',
    'WhatsApp Positions', 'Oculus Positions', 'Device Platforms', 'User Device',
    'Excluded User Device', 'User Operating System', 'User OS Version', 'Wireless Carrier',
    'Excluded Publisher Categories', 'Brand Safety Inventory Filtering Levels',
    'Optimization Goal', 'Attribution Spec', 'Billing Event', 'Bid Amount',
    'Ad Set Bid Strategy', 'Regional Regulated Categories',
    'Beneficiary (financial ads in Australia)', 'Payer (financial ads in Australia)',
    'Beneficiary (financial ads in Taiwan)', 'Payer (financial ads in Taiwan)',
    'Beneficiary (Taiwan)', 'Payer (Taiwan)', 'Beneficiary (Singapore)', 'Payer (Singapore)',
    'Beneficiary (securities ads in India)', 'Payer (securities ads in India)',
    'Beneficiary (selected locations)', 'Payer (selected locations)', 'Story ID', 'Ad ID',
    'Ad Status', 'Preview Link', 'Instagram Preview Link', 'Ad Name',
    'Dynamic Creative Ad Format', 'Default Language',
    'Additional Language 1', 'Additional Language 2', 'Additional Language 3',
    'Additional Language 4', 'Additional Language 5', 'Additional Language 6',
    'Additional Language 7', 'Additional Language 8', 'Additional Language 9',
    'Autotranslated Languages', 'Title',
    'Additional Title 1', 'Additional Title 2', 'Additional Title 3', 'Additional Title 4',
    'Additional Title 5', 'Additional Title 6', 'Additional Title 7', 'Additional Title 8',
    'Additional Title 9', 'Body',
    'Additional Body 1', 'Additional Body 2', 'Additional Body 3', 'Additional Body 4',
    'Additional Body 5', 'Additional Body 6', 'Additional Body 7', 'Additional Body 8',
    'Additional Body 9', 'Display Link',
    'Additional Link 1', 'Additional Display Link 1',
    'Additional Link 2', 'Additional Display Link 2',
    'Additional Link 3', 'Additional Display Link 3',
    'Additional Link 4', 'Additional Display Link 4',
    'Additional Link 5', 'Additional Display Link 5',
    'Additional Link 6', 'Additional Display Link 6',
    'Additional Link 7', 'Additional Display Link 7',
    'Additional Link 8', 'Additional Display Link 8',
    'Additional Link 9', 'Additional Display Link 9',
    'Link Description',
    'Additional Link Description 1', 'Additional Link Description 2',
    'Additional Link Description 3', 'Additional Link Description 4',
    'Additional Link Description 5', 'Additional Link Description 6',
    'Additional Link Description 7', 'Additional Link Description 8',
    'Additional Link Description 9',
    'Optimize text per person', 'Retailer IDs', 'Post Click Item Headline',
    'Post Click Item Description', 'Conversion Tracking Pixels', 'Image Hash',
    'Image File Name', 'Image Crops', 'Video Thumbnail URL',
    'Additional Image 1 Hash', 'Additional Image 1 Crops',
    'Additional Image 2 Hash', 'Additional Image 2 Crops',
    'Additional Image 3 Hash', 'Additional Image 3 Crops',
    'Additional Image 4 Hash', 'Additional Image 4 Crops',
    'Additional Image 5 Hash', 'Additional Image 5 Crops',
    'Additional Image 6 Hash', 'Additional Image 6 Crops',
    'Additional Image 7 Hash', 'Additional Image 7 Crops',
    'Additional Image 8 Hash', 'Additional Image 8 Crops',
    'Additional Image 9 Hash', 'Additional Image 9 Crops',
    'Instagram Platform Image Hash', 'Instagram Platform Image Crops',
    'Instagram Platform Image URL', 'Carousel Delivery Mode', 'Creative Type', 'URL Tags',
    'Event ID', 'Video ID', 'Video File Name',
    'Additional Video 1 ID', 'Additional Video 1 Thumbnail URL',
    'Additional Video 2 ID', 'Additional Video 2 Thumbnail URL',
    'Additional Video 3 ID', 'Additional Video 3 Thumbnail URL',
    'Additional Video 4 ID', 'Additional Video 4 Thumbnail URL',
    'Additional Video 5 ID', 'Additional Video 5 Thumbnail URL',
    'Additional Video 6 ID', 'Additional Video 6 Thumbnail URL',
    'Additional Video 7 ID', 'Additional Video 7 Thumbnail URL',
    'Additional Video 8 ID', 'Additional Video 8 Thumbnail URL',
    'Additional Video 9 ID', 'Additional Video 9 Thumbnail URL',
    'Instagram Account ID', 'Instagram Account ID (New)', 'Mobile App Deep Link',
    'Product Link', 'App Link Destination', 'Call Extension Phone Data ID', 'Call to Action',
    'Additional Call To Action 5', 'Additional Call To Action 6',
    'Additional Call To Action 7', 'Additional Call To Action 8',
    'Additional Call To Action 9', 'Call to Action Link', 'Call to Action WhatsApp Number',
    'Marketing Message Primary Text', 'Marketing Message Auto Reply - Body Text',
    'Marketing Message Auto Reply - Image Hash', 'Marketing Message Auto Reply - Video ID',
    'Marketing Message Auto Reply - Button 1 - Text',
    'Marketing Message Auto Reply - Button 1 - Type',
    'Marketing Message Auto Reply - Button 1 - URL',
    'Marketing Message Button 1 - Button Text', 'Marketing Message Button 1 - Type',
    'Marketing Message Button 1 - Response Text', 'Marketing Message Button 1 - Image Hash',
    'Marketing Message Button 1 - Video ID',
    'Marketing Message Button 1 - Video Thumbnail URL',
    'Marketing Message Button 1 - Call to Action Button - Type',
    'Marketing Message Button 1 - Call to Action Button - Text',
    'Marketing Message Button 1 - Call to Action Button - URL',
    'Marketing Message Button 2 - Button Text', 'Marketing Message Button 2 - Type',
    'Marketing Message Button 2 - Response Text', 'Marketing Message Button 2 - Image Hash',
    'Marketing Message Button 2 - Video ID',
    'Marketing Message Button 2 - Video Thumbnail URL',
    'Marketing Message Button 2 - Call to Action Button - Type',
    'Marketing Message Button 2 - Call to Action Button - Text',
    'Marketing Message Button 2 - Call to Action Button - URL',
    'Additional Custom Tracking Specs', 'Video Retargeting', 'Lead Form ID', 'Permalink',
    'Force Single Link', 'Format Option', 'Dynamic Ad Voice', 'Creative Optimization',
    'Template URL', 'Android App Name', 'Android Package Name', 'Deep Link For Android',
    'Facebook App ID', 'iOS App Name', 'iOS App Store ID', 'Deep Link For iOS',
    'iPad App Name', 'iPad App Store ID', 'Deep Link For iPad',
    'iPhone App Name', 'iPhone App Store ID', 'Deep Link For iPhone',
    'Deep link to website', 'Windows Store ID', 'Windows App Name',
    'Deep Link For Windows Phone', 'Add End Card', 'Dynamic Ads Ad Context',
    'Page Welcome Message', 'App Destination', 'App Destination Page ID', 'Use Page as Actor',
    'Image Overlay Template', 'Image Overlay Text Type', 'Image Overlay Text Font',
    'Image Overlay Position', 'Image Overlay Theme Color', 'Image Overlay Float With Margin',
    'Image Layer 1 - layer_type', 'Image Layer 1 - image_source',
    'Image Layer 1 - overlay_shape', 'Image Layer 1 - text_font',
    'Image Layer 1 - shape_color', 'Image Layer 1 - text_color',
    'Image Layer 1 - content_type', 'Image Layer 1 - price', 'Image Layer 1 - low_price',
    'Image Layer 1 - high_price', 'Image Layer 1 - frame_source',
    'Image Layer 1 - frame_image_hash', 'Image Layer 1 - scale',
    'Image Layer 1 - blending_mode', 'Image Layer 1 - opacity',
    'Image Layer 1 - overlay_position', 'Image Layer 1 - pad_image',
    'Image Layer 1 - crop_image', 'Image Layer 2 - layer_type',
    'Image Layer 2 - image_source', 'Image Layer 2 - overlay_shape',
    'Image Layer 2 - text_font', 'Image Layer 2 - shape_color',
    'Image Layer 2 - text_color', 'Image Layer 2 - content_type', 'Image Layer 2 - price',
    'Image Layer 2 - low_price', 'Image Layer 2 - high_price',
    'Image Layer 2 - frame_source', 'Image Layer 2 - frame_image_hash',
    'Image Layer 2 - scale', 'Image Layer 2 - blending_mode', 'Image Layer 2 - opacity',
    'Image Layer 2 - overlay_position', 'Image Layer 2 - pad_image',
    'Image Layer 2 - crop_image', 'Image Layer 3 - layer_type',
    'Image Layer 3 - image_source', 'Image Layer 3 - overlay_shape',
    'Image Layer 3 - text_font', 'Image Layer 3 - shape_color',
    'Image Layer 3 - text_color', 'Image Layer 3 - content_type', 'Image Layer 3 - price',
    'Image Layer 3 - low_price', 'Image Layer 3 - high_price',
    'Image Layer 3 - frame_source', 'Image Layer 3 - frame_image_hash',
    'Image Layer 3 - scale', 'Image Layer 3 - blending_mode', 'Image Layer 3 - opacity',
    'Image Layer 3 - overlay_position', 'Image Layer 3 - pad_image',
    'Image Layer 3 - crop_image',
    'Product 1 - Link', 'Product 1 - Name', 'Product 1 - Description',
    'Product 1 - Marketing Message - Description', 'Product 1 - Image Hash',
    'Product 1 - Image Crops', 'Product 1 - Video ID', 'Product 1 - Call To Action Link',
    'Product 1 - Mobile App Deep Link', 'Product 1 - Display Link',
    'Product 1 - Place Data', 'Product 1 - Is Static Card',
    'Product 2 - Link', 'Product 2 - Name', 'Product 2 - Description',
    'Product 2 - Marketing Message - Description', 'Product 2 - Image Hash',
    'Product 2 - Image Crops', 'Product 2 - Video ID', 'Product 2 - Call To Action Link',
    'Product 2 - Mobile App Deep Link', 'Product 2 - Display Link',
    'Product 2 - Place Data', 'Product 2 - Is Static Card',
    'Product 3 - Link', 'Product 3 - Name', 'Product 3 - Description',
    'Product 3 - Marketing Message - Description', 'Product 3 - Image Hash',
    'Product 3 - Image Crops', 'Product 3 - Video ID', 'Product 3 - Call To Action Link',
    'Product 3 - Mobile App Deep Link', 'Product 3 - Display Link',
    'Product 3 - Place Data', 'Product 3 - Is Static Card',
    'Product 4 - Link', 'Product 4 - Name', 'Product 4 - Description',
    'Product 4 - Marketing Message - Description', 'Product 4 - Image Hash',
    'Product 4 - Image Crops', 'Product 4 - Video ID', 'Product 4 - Call To Action Link',
    'Product 4 - Mobile App Deep Link', 'Product 4 - Display Link',
    'Product 4 - Place Data', 'Product 4 - Is Static Card',
    'Product 5 - Link', 'Product 5 - Name', 'Product 5 - Description',
    'Product 5 - Marketing Message - Description', 'Product 5 - Image Hash',
    'Product 5 - Image Crops', 'Product 5 - Video ID', 'Product 5 - Call To Action Link',
    'Product 5 - Mobile App Deep Link', 'Product 5 - Display Link',
    'Product 5 - Place Data', 'Product 5 - Is Static Card',
    'Product 6 - Link', 'Product 6 - Name', 'Product 6 - Description',
    'Product 6 - Marketing Message - Description', 'Product 6 - Image Hash',
    'Product 6 - Image Crops', 'Product 6 - Video ID', 'Product 6 - Call To Action Link',
    'Product 6 - Mobile App Deep Link', 'Product 6 - Display Link',
    'Product 6 - Place Data', 'Product 6 - Is Static Card',
    'Product 7 - Link', 'Product 7 - Name', 'Product 7 - Description',
    'Product 7 - Marketing Message - Description', 'Product 7 - Image Hash',
    'Product 7 - Image Crops', 'Product 7 - Video ID', 'Product 7 - Call To Action Link',
    'Product 7 - Mobile App Deep Link', 'Product 7 - Display Link',
    'Product 7 - Place Data', 'Product 7 - Is Static Card',
    'Product 8 - Link', 'Product 8 - Name', 'Product 8 - Description',
    'Product 8 - Marketing Message - Description', 'Product 8 - Image Hash',
    'Product 8 - Image Crops', 'Product 8 - Video ID', 'Product 8 - Call To Action Link',
    'Product 8 - Mobile App Deep Link', 'Product 8 - Display Link',
    'Product 8 - Place Data', 'Product 8 - Is Static Card',
    'Product 9 - Link', 'Product 9 - Name', 'Product 9 - Description',
    'Product 9 - Marketing Message - Description', 'Product 9 - Image Hash',
    'Product 9 - Image Crops', 'Product 9 - Video ID', 'Product 9 - Call To Action Link',
    'Product 9 - Mobile App Deep Link', 'Product 9 - Display Link',
    'Product 9 - Place Data', 'Product 9 - Is Static Card',
    'Product 10 - Link', 'Product 10 - Name', 'Product 10 - Description',
    'Product 10 - Marketing Message - Description', 'Product 10 - Image Hash',
    'Product 10 - Image Crops', 'Product 10 - Video ID', 'Product 10 - Call To Action Link',
    'Product 10 - Mobile App Deep Link', 'Product 10 - Display Link',
    'Product 10 - Place Data', 'Product 10 - Is Static Card',
    'Product Sales Channel',
    'Additional Dynamic Creative Call To Action Type 5',
    'Additional Dynamic Creative Call To Action Type 6',
    'Additional Dynamic Creative Call To Action Type 7',
    'Additional Dynamic Creative Call To Action Type 8',
    'Additional Dynamic Creative Call To Action Type 9',
    'Degrees of Freedom Type', 'Creative Destination Type', 'Creative Onsite Destinations',
    'Mockup ID', 'Text Transformations', 'Ad Stop Time', 'Ad Start Time',
]

COL = {h: i for i, h in enumerate(HEADERS)}
ATTRIBUTION = '[{"event_type":"CLICK_THROUGH","window_days":7},{"event_type":"VIEW_THROUGH","window_days":1},{"event_type":"ENGAGED_VIDEO_VIEW","window_days":1}]'

FB_LANGUAGES = [
    "Afrikaans", "Albanian", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian",
    "Bengali", "Bosnian", "Bulgarian", "Catalan", "Chinese (Simplified)",
    "Chinese (Traditional)", "Croatian", "Czech", "Danish", "Dutch", "English",
    "Estonian", "Finnish", "French", "Galician", "Georgian", "German", "Greek",
    "Gujarati", "Hebrew", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese",
    "Kannada", "Kazakh", "Korean", "Kurdish (Kurmanji)", "Latvian", "Lithuanian",
    "Macedonian", "Malay", "Malayalam", "Marathi", "Mongolian", "Nepali", "Norwegian",
    "Persian", "Polish", "Portuguese (Brazil)", "Portuguese (Portugal)", "Punjabi",
    "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish",
    "Swahili", "Swedish", "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian",
    "Urdu", "Uzbek", "Vietnamese", "Welsh",
]

# ─── База текстов (загружается один раз при старте) ───────────────────────────

@st.cache_resource
def load_texts_db():
    db_path = os.path.join(os.path.dirname(__file__), 'texts_db.json')
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('texts', [])
        except Exception:
            return []
    return []

TEXTS_DB = load_texts_db()

# ─── Генерация XLSX ───────────────────────────────────────────────────────────

def generate_xlsx(gd, cab, langs):
    now = datetime.now()

    # Сдвиг времени старта (только в DB-режиме)
    if gd.get('start_offset_hours', 0):
        now = now + timedelta(hours=gd['start_offset_hours'])

    h = now.hour % 12 or 12
    ap = 'am' if now.hour < 12 else 'pm'
    now_str = f"{now.strftime('%m/%d/%Y')} {h}:{now.strftime('%M:%S')} {ap}"
    cab_last3 = cab['cab_id'][-3:]

    # Рандомизация бюджета ±7 (только в DB-режиме)
    budget = gd['budget']
    if gd.get('db_mode'):
        budget = max(1.0, budget + random.randint(-7, 7))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(HEADERS)

    for n in range(1, gd['adset_count'] + 1):
        adset_name = f"{gd['seller']}-{cab['cab_id']}-{cab['creo_str']}-{n}"
        ad_name = f"{cab['creo_str']}.{cab_last3}.{n}"
        camp_name = (f"{gd['offer_name']}.{gd['seller']}.{cab['cab_id']}"
                     f"_{gd['buyer_code']}:{gd['buyer_code']}")
        url_tags = f"{gd['url_tags_base']}={cab['pixel_id']}"

        row = [''] * len(HEADERS)

        def s(k, v):
            if k in COL:
                row[COL[k]] = v

        s('Campaign Name', camp_name)
        s('Campaign Status', 'PAUSED')
        s('Campaign Objective', 'Outcome Leads')
        s('Buying Type', 'AUCTION')
        s('New Objective', 'Yes')

        if gd['budget_type'] == 'CBO':
            s('Campaign Daily Budget', budget)
            s('Campaign Bid Strategy', 'Highest volume or value')

        s('Ad Set Run Status', 'ACTIVE')
        s('Ad Set Lifetime Impressions', 0)
        s('Ad Set Name', adset_name)
        s('Ad Set Time Start', now_str)
        s('Ad Set Lifetime Budget', 0)
        s('Use Accelerated Delivery', 'No')
        s('Is Budget Scheduling Enabled For Ad Set', 'No')
        s('Ad Set High Demand Periods', '[]')

        if cab['fp_id']:
            s('Link Object ID', f"o:{cab['fp_id']}")

        s('Optimized Conversion Tracking Pixels', f"tp:{cab['pixel_id']}")
        s('Optimized Event', 'LEAD')
        s('Link', cab['offer_url'])
        s('Countries', gd['countries'])
        s('Location Types', 'home, recent')

        if gd['gender'] != 'All':
            s('Gender', gd['gender'])

        s('Age Min', gd['age_min'])
        s('Age Max', gd['age_max'])
        if gd['geo_locales']:
            s('Locales', gd['geo_locales'])

        s('Advantage Audience', 1)
        s('Individual Setting', 'age: On, gender: On')
        s('Age Range', f"{gd['age_min']}, {gd['age_max']}")
        s('User Operating System', 'All')
        s('Brand Safety Inventory Filtering Levels', 'FACEBOOK_RELAXED, AN_RELAXED')
        s('Optimization Goal', 'OFFSITE_CONVERSIONS')
        s('Attribution Spec', ATTRIBUTION)
        s('Billing Event', 'IMPRESSIONS')
        s('Regional Regulated Categories', 'VOLUNTARY_VERIFICATION')

        if gd['budget_type'] == 'ABO':
            s('Ad Set Daily Budget', budget)
            s('Ad Set Bid Strategy', 'Highest volume or value')

        s('Ad Status', 'ACTIVE')
        s('Ad Name', ad_name)
        s('Dynamic Creative Ad Format', 'Single Video')
        s('Default Language', gd['main_lang'])
        s('Title', gd['main_title'])
        s('Body', gd['main_body'])
        s('Display Link', gd['display_link'])
        s('Optimize text per person', 'No')
        s('Conversion Tracking Pixels', f"tp:{cab['pixel_id']}")
        s('Creative Type', 'Link Page Post Ad')
        s('URL Tags', url_tags)
        s('Call to Action', 'LEARN_MORE')
        s('Video ID', f"v:{cab['main_video']}")

        # Доп. языки — видосы только если есть основной
        for i, ld in enumerate(langs, 1):
            s(f'Additional Language {i}', ld['lang'])
            s(f'Additional Title {i}', ld['title'])
            s(f'Additional Body {i}', ld['body'])
            # Русский всегда получает оффер-урл кабинета, остальные — amazon
            if ld['lang'] == 'Russian':
                s(f'Additional Link {i}', cab['offer_url'])
            elif gd['amazon_url']:
                s(f'Additional Link {i}', gd['amazon_url'])
            if gd['secondary_video'] and cab['main_video']:
                s(f'Additional Video {i} ID', f"v:{gd['secondary_video']}")

        ws.append(row)

    ws.freeze_panes = 'A2'
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()

# ─── UI ───────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="FB Ad Generator", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .main { background-color: #1a1a2e; }
    .block-container { padding-top: 1.5rem; }
    h1 { color: #e94560; }
    h2, h3 { color: #7ec8e3; }
    .stTextInput > label, .stNumberInput > label,
    .stSelectbox > label, .stTextArea > label { color: #eaeaea; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ FB Ad Generator")
st.caption("v2.0 · multi-cabinet · один клик → N файлов")

tab1, tab2, tab3, tab4 = st.tabs(["⚙ Глобально", "🗂 Кабинеты", "🎯 Таргет", "🌐 Языки"])

# ── Таб 1: Глобально ─────────────────────────────────────────────────────────
with tab1:
    st.subheader("Нейминг")
    c1, c2, c3 = st.columns(3)
    offer_name  = c1.text_input("Оффер", placeholder="Ber")
    seller      = c2.text_input("Селлер", placeholder="GH")
    buyer_code  = c3.text_input("Метка баера (КК)", placeholder="RR")
    if offer_name and seller and buyer_code:
        st.caption(f"→ `{offer_name}.{seller}.[КАБИНЕТ]_{buyer_code}:{buyer_code}`")

    st.subheader("Структура и бюджет")
    c1, c2, c3 = st.columns(3)
    adset_count  = c1.number_input("Кол-во адсетов", min_value=1, max_value=50, value=5)
    budget       = c2.number_input("Дневной бюджет ($)", min_value=1.0, value=50.0, step=1.0)
    budget_type  = c3.selectbox("Тип бюджета", ["ABO", "CBO"])

    st.subheader("Ссылки")
    display_link = st.text_input("Display Link", placeholder="example.com")
    amazon_url   = st.text_input("Amazon URL (для доп. языков — не русского)")

    st.subheader("URL Tags")
    url_tags_base = st.text_input(
        "База (до =) — пиксель каждого каба добавится автоматически",
        value="sub_id_1=1&sub_id_2=seller&sub_id_3=geo&sub_id_4=age&sub_id_5={{ad.name}}&pixel"
    )
    st.caption("Итог: `[база]=[pixel_id кабинета]`")

    st.subheader("Amazon видос (доп. языки, одинаков для всех кабов)")
    secondary_video = st.text_input("Video ID (без v:)", placeholder="1234567890")
    st.caption("Ставится только если у каба заполнен основной Video ID")

# ── Таб 2: Кабинеты ──────────────────────────────────────────────────────────
with tab2:
    st.subheader("Кабинеты")
    st.caption("Один ряд = один кабинет = один XLSX файл")

    if 'cab_count' not in st.session_state:
        st.session_state.cab_count = 1

    c1, c2 = st.columns([1, 6])
    if c1.button("＋ Добавить"):
        st.session_state.cab_count += 1
    if c2.button("－ Удалить") and st.session_state.cab_count > 1:
        st.session_state.cab_count -= 1

    cab_data = []
    for i in range(st.session_state.cab_count):
        st.markdown(f"**Кабинет {i+1}**")
        cols = st.columns([2, 2, 2, 1, 2, 3])
        cab_id    = cols[0].text_input("ID кабинета *",           key=f"cab_{i}")
        fp_id     = cols[1].text_input("ID фанки (без o:) *",     key=f"fp_{i}")
        pixel_id  = cols[2].text_input("ID пикселя *",            key=f"px_{i}")
        creo      = cols[3].text_input("Крео (УУ) *",             key=f"cr_{i}", value="01")
        main_vid  = cols[4].text_input("Video ID осн. (без v:) *", key=f"mv_{i}")
        offer_url_cab = cols[5].text_input("URL оффера *",         key=f"ou_{i}")
        cab_data.append({
            'cab_id': cab_id.strip(),
            'fp_id': fp_id.strip(),
            'pixel_id': pixel_id.strip(),
            'creo_str': str(int(creo.strip())).zfill(2) if creo.strip().isdigit() else creo.strip(),
            'main_video': main_vid.strip(),
            'offer_url': offer_url_cab.strip(),
        })

# ── Таб 3: Таргет ────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Таргетинг")
    c1, c2 = st.columns(2)
    countries   = c1.text_input("Гео (страны через запятую)", value="UZ")
    geo_locales = c2.text_input("Locales (языки гео)", value="Russian")

    c1, c2, c3 = st.columns(3)
    age_min = c1.number_input("Возраст от", min_value=13, max_value=65, value=18)
    age_max = c2.number_input("Возраст до", min_value=13, max_value=65, value=65)
    gender  = c3.selectbox("Пол", ["All", "Men", "Women"])

# ── Таб 4: Языки ─────────────────────────────────────────────────────────────
with tab4:
    # ── Режим базы данных (новое) ──────────────────────────────────────────────
    db_mode = False
    db_product_idx = None

    if TEXTS_DB:
        st.subheader("🗃 База текстов")
        db_mode = st.checkbox(
            "Взять тексты из базы (texts_db.json)",
            help="Автоматически подставит заголовок и тело объявления из базы продуктов. "
                 "Заодно включает рандомизацию бюджета, времени старта и возраста."
        )
        if db_mode:
            product_labels = [
                f"Продукт {i+1}: {p['ru_title'][:60]}…" if len(p['ru_title']) > 60
                else f"Продукт {i+1}: {p['ru_title']}"
                for i, p in enumerate(TEXTS_DB)
            ]
            product_labels.insert(0, "🎲 Случайный продукт")
            chosen = st.selectbox("Выберите продукт", product_labels, index=0)
            if chosen.startswith("🎲"):
                db_product_idx = None  # определится при нажатии кнопки
            else:
                db_product_idx = product_labels.index(chosen) - 1  # сдвиг из-за вставки

            st.info(
                "При DB-режиме: бюджет ±7$, старт +0–4 ч, возраст 23 или 24, "
                "порядок языков перемешивается автоматически."
            )
        st.divider()
    else:
        st.info("texts_db.json не найден рядом с app.py — ручной режим")

    st.subheader("Основной язык")
    c1, c2 = st.columns([1, 2])
    main_lang  = c1.selectbox("Язык", FB_LANGUAGES,
                               index=FB_LANGUAGES.index("Russian"))
    main_title = c2.text_input("Title (основной язык)", disabled=db_mode)
    main_body  = st.text_area("Body (основной язык)", height=100, disabled=db_mode)

    if db_mode:
        st.caption("↑ Поля заблокированы — текст подтянется из базы при генерации")

    st.subheader("Дополнительные языки")

    if db_mode:
        st.caption(
            "DB-режим: языки из базы (10 вариантов, порядок будет перемешан при генерации). "
            "Ручное добавление недоступно."
        )
        lang_data = []  # заполнится из базы при нажатии кнопки
    else:
        if 'lang_count' not in st.session_state:
            st.session_state.lang_count = 0

        c1, c2 = st.columns([1, 6])
        if c1.button("＋ Добавить язык") and st.session_state.lang_count < 9:
            st.session_state.lang_count += 1
        if c2.button("－ Удалить язык") and st.session_state.lang_count > 0:
            st.session_state.lang_count -= 1

        lang_data = []
        for i in range(st.session_state.lang_count):
            st.markdown(f"**Язык {i+1}**")
            c1, c2 = st.columns([1, 2])
            lang  = c1.selectbox("Язык", FB_LANGUAGES, key=f"lang_{i}")
            title = c2.text_input("Title", key=f"ltitle_{i}")
            body  = st.text_area("Body", key=f"lbody_{i}", height=80)
            lang_data.append({'lang': lang, 'title': title, 'body': body})

# ── Кнопка генерации ─────────────────────────────────────────────────────────
st.divider()
if st.button("🚀 ГЕНЕРИРОВАТЬ", type="primary", use_container_width=True):
    errors = []
    if not offer_name:  errors.append("Оффер")
    if not seller:      errors.append("Селлер")
    if not buyer_code:  errors.append("Метка баера")
    if not db_mode and age_min >= age_max:
        errors.append("Возраст: от должен быть меньше до")

    for i, cab in enumerate(cab_data, 1):
        if not cab['cab_id']:   errors.append(f"Кабинет {i}: ID")
        if not cab['pixel_id']: errors.append(f"Кабинет {i}: пиксель")
        if not cab['offer_url']: errors.append(f"Кабинет {i}: URL оффера")
        if not cab['main_video']: errors.append(f"Кабинет {i}: Video ID (обязателен для импорта)")

    if errors:
        st.error("Не заполнено:\n- " + "\n- ".join(errors))
    else:
        # ── DB-режим: подставляем тексты и рандомизируем ──────────────────────
        final_main_title = main_title
        final_main_body  = main_body
        final_age_min    = int(age_min)
        final_age_max    = int(age_max)
        start_offset_hours = 0

        if db_mode and TEXTS_DB:
            # Выбор продукта
            if db_product_idx is None:
                product = random.choice(TEXTS_DB)
            else:
                product = TEXTS_DB[db_product_idx]

            final_main_title = product['ru_title']
            final_main_body  = product['ru_body']

            # Языки из базы
            tr = product['translations']
            lang_data = [
                {'lang': lang, 'title': tr[lang]['title'], 'body': tr[lang]['body']}
                for lang in tr
            ]
            # Перемешать порядок языков
            random.shuffle(lang_data)
            # Ограничить 9-ю слотами (лимит FB)
            lang_data = lang_data[:9]

            # Возраст: 23 или 24
            final_age_min = random.choice([23, 24])
            final_age_max = int(age_max)

            # Сдвиг времени старта: 0–4 часа
            start_offset_hours = random.randint(0, 4)

        gd = {
            'offer_name': offer_name, 'seller': seller, 'buyer_code': buyer_code,
            'adset_count': int(adset_count), 'budget_type': budget_type, 'budget': float(budget),
            'display_link': display_link, 'amazon_url': amazon_url,
            'url_tags_base': url_tags_base, 'secondary_video': secondary_video,
            'countries': countries, 'geo_locales': geo_locales,
            'age_min': final_age_min, 'age_max': final_age_max, 'gender': gender,
            'main_lang': main_lang, 'main_title': final_main_title, 'main_body': final_main_body,
            'db_mode': db_mode,
            'start_offset_hours': start_offset_hours,
        }

        if len(cab_data) == 1:
            # Один файл — скачать напрямую
            cab = cab_data[0]
            xlsx = generate_xlsx(gd, cab, lang_data)
            camp_name = f"{offer_name}.{seller}.{cab['cab_id']}_{buyer_code}-{buyer_code}"
            st.download_button(
                label=f"⬇ Скачать {camp_name}.xlsx",
                data=xlsx,
                file_name=f"{camp_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # Несколько файлов — ZIP
            zip_buf = io.BytesIO()
            with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
                for cab in cab_data:
                    xlsx = generate_xlsx(gd, cab, lang_data)
                    safe = f"{offer_name}.{seller}.{cab['cab_id']}_{buyer_code}-{buyer_code}.xlsx"
                    zf.writestr(safe, xlsx)
            zip_buf.seek(0)
            st.download_button(
                label=f"⬇ Скачать все {len(cab_data)} файлов (ZIP)",
                data=zip_buf.getvalue(),
                file_name=f"{offer_name}_campaigns.zip",
                mime="application/zip"
            )
        st.success(f"Сгенерировано файлов: {len(cab_data)}")
