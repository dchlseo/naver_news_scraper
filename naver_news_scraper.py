import urllib.request
import urllib.parse
import json
import html
import re
import pandas as pd
from datetime import datetime, timedelta
import argparse
import sys

# ------------------------- API REQUEST ------------------------- #

def get_naver_news(query, display, start, sort, client_id, client_secret):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&display={display}&start={start}&sort={sort}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    if response.getcode() == 200:
        return json.loads(response.read())
    else:
        print("❌ Error Code:", response.getcode())
        return None

# ------------------------- HELPERS ------------------------- #

def clean_html_tags(text):
    return re.sub(r"</?b>", "", html.unescape(text))

def extract_keywords(text):
    return ", ".join(set(re.findall(r"<b>(.*?)</b>", text))) or None

def parse_pub_date(pub_date_str):
    try:
        return datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception as e:
        print("⚠️ Failed to parse pubDate:", pub_date_str)
        return None

# ------------------------- MAIN SCRAPER ------------------------- #

def run_scraper(query, start_date_str, end_date_str, client_id, client_secret):
    display = 100
    sort = "date"
    start = 1

    start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
    end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

    all_records = []

    while True:
        data = get_naver_news(query, display, start, sort, client_id, client_secret)
        if not data or not data.get("items"):
            break

        stop_flag = False

        for item in data["items"]:
            raw_title = html.unescape(item.get("title", ""))
            raw_desc = html.unescape(item.get("description", ""))
            pubDate_full = item.get("pubDate", "")
            pubDate = parse_pub_date(pubDate_full)

            if not pubDate:
                continue

            pub_date = pubDate.date()

            if pub_date < start_date:
                stop_flag = True
                break
            if pub_date > end_date:
                continue

            keywords = extract_keywords(raw_title + raw_desc)
            clean_title = clean_html_tags(raw_title)
            clean_desc = clean_html_tags(raw_desc)

            print(f"📰 {clean_title}")
            print(f"🔗 Link: {item.get('link', '')}")
            print(f"🗞️ Original: {item.get('originallink', '')}")
            print(f"📝 Desc: {clean_desc}")
            print(f"📅 Date: {pub_date}")
            print(f"🔍 Keyword(s): {keywords}\n")

            all_records.append({
                "Date": pub_date.strftime("%Y-%m-%d"),
                "SearchDate": pubDate_full,
                "Keyword": keywords,
                "Title": clean_title,
                "Desc": clean_desc,
                "Link": item.get("link", ""),
                "Original": item.get("originallink", "")
            })

        if stop_flag or len(data["items"]) < display:
            break

        start += display

    df = pd.DataFrame(all_records)
    print(f"\n✅ Total articles collected: {len(df)}")

    # 🧮 Add date-based columns
    df["year"] = pd.to_datetime(df["Date"]).dt.year
    df["month"] = pd.to_datetime(df["Date"]).dt.month
    df["ym"] = pd.to_datetime(df["Date"]).dt.strftime("%Y%m")
    df["yq"] = pd.to_datetime(df["Date"]).dt.to_period("Q").astype(str)

    # Reorder columns: move year, month, ym, yq to the front
    col_order = ["year", "month", "ym", "yq"] + [col for col in df.columns if col not in ["year", "month", "ym", "yq"]]
    df = df[col_order]

    filename = f"./output/naver_news_RESULTS_{query}_{start_date_str}_{end_date_str}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"📁 Saved to: {filename}")
    return df

# ------------------------- ENTRY POINT ------------------------- #

if __name__ == "__main__":
    today_str = datetime.today().strftime("%Y%m%d")

    parser = argparse.ArgumentParser(description="Naver News Scraper")
    parser.add_argument("--query", type=str, default="야놀자리서치", help="Search keyword (default: '야놀자리서치')")
    parser.add_argument("--start_date", type=str, default="20250401", help="Start date in YYYYMMDD format (default: 20250101)")
    parser.add_argument("--end_date", type=str, default=today_str, help=f"End date in YYYYMMDD format (default: {today_str})")

    args = parser.parse_args()

    # 🔐 Your Naver API credentials (리서치 공계)
    client_id = "YOUR_CLIENT_ID"    
    client_secret = "YOUR_CLIENT_SECRET"

    run_scraper(args.query, args.start_date, args.end_date, client_id, client_secret)
