"""
generate.py
Supabase からイベントデータを取得し、静的 HTML を生成する。

必要な環境変数:
  SUPABASE_URL   : SupabaseプロジェクトのURL (例: https://xxxx.supabase.co)
  SUPABASE_KEY   : Supabase の anon キー
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── エリアコード定義（アプリ側の constants.dart と合わせること） ──
AREA_NAMES: dict[str, str] = {
    "00": "未定",
    "01": "北海道",
    "02": "青森県",
    "03": "岩手県",
    "04": "宮城県",
    "05": "秋田県",
    "06": "山形県",
    "07": "福島県",
    "08": "茨城県",
    "09": "栃木県",
    "10": "群馬県",
    "11": "埼玉県",
    "12": "千葉県",
    "13": "東京都",
    "14": "神奈川県",
    "15": "新潟県",
    "16": "富山県",
    "17": "石川県",
    "18": "福井県",
    "19": "山梨県",
    "20": "長野県",
    "21": "岐阜県",
    "22": "静岡県",
    "23": "愛知県",
    "24": "三重県",
    "25": "滋賀県",
    "26": "京都府",
    "27": "大阪府",
    "28": "兵庫県",
    "29": "奈良県",
    "30": "和歌山県",
    "31": "鳥取県",
    "32": "島根県",
    "33": "岡山県",
    "34": "広島県",
    "35": "山口県",
    "36": "徳島県",
    "37": "香川県",
    "38": "愛媛県",
    "39": "高知県",
    "40": "福岡県",
    "41": "佐賀県",
    "42": "長崎県",
    "43": "熊本県",
    "44": "大分県",
    "45": "宮崎県",
    "46": "鹿児島県",
    "47": "沖縄県",
    "98": "オンライン",
    "99": "海外"
}


def get_env(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        print(f"ERROR: 環境変数 {key} が設定されていません", file=sys.stderr)
        sys.exit(1)
    return val


def supabase_get(url: str, key: str, table: str, params: dict) -> list[dict]:
    """Supabase REST API から全件取得（1000件超対応）"""
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }
    results = []
    limit = 1000
    offset = 0

    while True:
        p = {**params, "limit": limit, "offset": offset}
        res = requests.get(f"{url}/rest/v1/{table}", headers=headers, params=p, timeout=30)
        res.raise_for_status()
        batch = res.json()
        results.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    return results


def fetch_events(url: str, key: str) -> list[dict]:
    """公開中のイベントをすべて取得"""
    return supabase_get(url, key, "mispla_events", {
        "select": "id,title,max_participants,description,area_code,place,start_time,end_time,host_user,is_public_event",
        "is_public_event": "eq.true",
        "order": "start_time.asc",
    })


def fetch_users(url: str, key: str) -> dict[str, dict]:
    """mispla_users を uid をキーにしたdictで返す"""
    rows = supabase_get(url, key, "mispla_users", {
        "select": "uid,host,username,name,avatar_url",
    })
    return {r["uid"]: r for r in rows}


def fetch_participants(url: str, key: str) -> dict[str, list[dict]]:
    """mispla_participants を event_id をキーにしたdictで返す"""
    rows = supabase_get(url, key, "mispla_participants", {
        "select": "event_id,user_id,status",
    })
    result: dict[str, list] = {}
    for r in rows:
        result.setdefault(r["event_id"], []).append(r)
    return result


def fetch_tags(url: str, key: str) -> dict[str, list[str]]:
    """mispla_tags を event_id をキーにした {event_id: [tag_name, ...]} で返す"""
    rows = supabase_get(url, key, "mispla_tags", {
        "select": "event_id,tag_name",
        "order": "created_at.asc",
    })
    result: dict[str, list] = {}
    for r in rows:
        result.setdefault(r["event_id"], []).append(r["tag_name"])
    return result


def build_events_json(
    events: list[dict],
    users: dict[str, dict],
    participants_by_event: dict[str, list[dict]],
    tags_by_event: dict[str, list[str]],
) -> list[dict]:
    """フロントエンド用にデータを結合・整形する"""
    output = []
    for ev in events:
        host_uid = ev.get("host_user")
        host = users.get(host_uid, {})

        raw_participants = participants_by_event.get(ev["id"], [])
        participants = []
        for p in raw_participants:
            u = users.get(p["user_id"], {})
            participants.append({
                "status":     p["status"],
                "username":   u.get("username", ""),
                "name":       u.get("name", ""),
                "host":       u.get("host", ""),
                "avatar_url": u.get("avatar_url", ""),
            })

        output.append({
            "id":              ev["id"],
            "title":           ev["title"],
            "description":     ev.get("description", ""),
            "max_participants": ev["max_participants"],
            "area_code":       ev.get("area_code", "00"),
            "place":           ev.get("place", ""),
            "start_time":      ev.get("start_time"),
            "end_time":        ev.get("end_time"),
            #"host_uid":        host_uid,
            "host_username":   host.get("username", ""),
            "host_name":       host.get("name", ""),
            "host_host":       host.get("host", ""),
            "host_avatar":     host.get("avatar_url", ""),
            "participants":    participants,
            "tags":           tags_by_event.get(ev["id"], []),
        })

    return output


def generate_html(events_json: list[dict], template_path: Path, output_path: Path) -> None:
    """テンプレートHTMLにデータを埋め込んで出力する"""
    template = template_path.read_text(encoding="utf-8")

    html = template \
        .replace("__EVENTS_JSON__",    json.dumps(events_json, ensure_ascii=False)) \
        .replace("__AREA_NAMES_JSON__", json.dumps(AREA_NAMES, ensure_ascii=False)) \

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ 生成完了: {output_path}  ({len(events_json)} 件のイベント)")


def main() -> None:
    supabase_url = get_env("SUPABASE_URL").rstrip("/")
    supabase_key = get_env("SUPABASE_KEY")

    print("📡 Supabase からデータを取得中...")
    events       = fetch_events(supabase_url, supabase_key)
    users        = fetch_users(supabase_url, supabase_key)
    participants = fetch_participants(supabase_url, supabase_key)
    tags         = fetch_tags(supabase_url, supabase_key)
    print(f"   イベント: {len(events)} 件 / ユーザー: {len(users)} 件")

    events_json = build_events_json(events, users, participants, tags)

    base_dir      = Path(__file__).parent
    template_path = base_dir / "mispla" / "template.html"
    output_path   = base_dir / "mispla" / "events.html"

    generate_html(events_json, template_path, output_path)


if __name__ == "__main__":
    main()