import json
import urllib.request

API_URL = "https://tv.moviemasti.net/api/v1/live/channels?category=all"

def main():
    req = urllib.request.Request(
        API_URL,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    channels = data.get("items", []) if isinstance(data, dict) else data

    # EXTM3U with standard attributes
    m3u_lines = ["#EXTM3U\n"]
    for item in channels:
        ch_id = item.get("id", "")
        name = item.get("name", "Unknown").strip()
        logo = item.get("logo_url", "")
        url = item.get("stream_url", "").strip()
        category = item.get("category", "Live TV")

        if url:
            # Full IPTV specification line: tvg-id, tvg-name, tvg-logo, group-title
            m3u_lines.append(
                f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{name}\n{url}\n'
            )

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.writelines(m3u_lines)

if __name__ == "__main__":
    main()
