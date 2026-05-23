#!/usr/bin/env python3
"""从 APNIC delegated 数据生成中国大陆 IP 路由表。"""

from __future__ import annotations

import argparse
import math
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from ipaddress import IPv4Network, IPv6Network, collapse_addresses
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

APNIC_URLS = [
    "https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest",
    "https://mirror.apnic.net/apnic/stats/apnic/delegated-apnic-latest",
]

V4_REGEX = re.compile(r"^apnic\|cn\|ipv4\|", re.I)
V6_REGEX = re.compile(r"^apnic\|cn\|ipv6\|", re.I)


def download_apnic(dest: Path) -> None:
    last_error: Exception | None = None
    for url in APNIC_URLS:
        try:
            print(f"Downloading {url} ...", file=sys.stderr)
            with urllib.request.urlopen(url, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            print(f"  failed: {exc}", file=sys.stderr)
    raise RuntimeError("无法下载 APNIC delegated 数据") from last_error


def parse_record(line: str) -> IPv4Network | IPv6Network | None:
    parts = line.strip().split("|")
    if len(parts) < 5:
        return None
    rec_type, start, value = parts[2], parts[3], parts[4]
    try:
        if rec_type == "ipv4":
            count = int(value)
            prefix = int(32 - math.log2(count))
            return IPv4Network(f"{start}/{prefix}", strict=False)
        if rec_type == "ipv6":
            return IPv6Network(f"{start}/{value}", strict=False)
    except (ValueError, ArithmeticError):
        return None
    return None


def parse_networks(lines: list[str], pattern: re.Pattern[str]) -> list:
    nets = []
    for line in lines:
        if not pattern.match(line):
            continue
        net = parse_record(line)
        if net is not None:
            nets.append(net)
    return nets


def aggregate_networks(nets: list) -> list:
    if not nets:
        return []
    return sorted(collapse_addresses(nets), key=lambda n: (n.version, n.network_address))


def write_routes(path: Path, nets: list) -> None:
    body = "\n".join(str(n) for n in nets) + ("\n" if nets else "")
    path.write_text(body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="生成中国大陆 IP 路由表")
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "delegated-apnic-latest",
        help="本地 APNIC delegated 文件路径",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="生成前从 APNIC 下载最新 delegated 数据",
    )
    parser.add_argument(
        "--no-aggregate",
        action="store_true",
        help="不做 CIDR 聚合（条目更多）",
    )
    args = parser.parse_args()

    if args.download or not args.input.is_file():
        download_apnic(args.input)

    lines = args.input.read_text(encoding="utf-8", errors="replace").splitlines()
    source = "APNIC delegated-apnic-latest (registry|CN|ipv4|ipv6)"

    v4 = parse_networks(lines, V4_REGEX)
    v6 = parse_networks(lines, V6_REGEX)

    if not args.no_aggregate:
        v4 = aggregate_networks(v4)
        v6 = aggregate_networks(v6)
    else:
        v4 = sorted(v4, key=lambda n: n.network_address)
        v6 = sorted(v6, key=lambda n: n.network_address)

    write_routes(ROOT / "chnroutes-v4", v4)
    write_routes(ROOT / "chnroutes-v6", v6)
    # 兼容旧版仅 IPv4 的 chnroutes.txt
    write_routes(ROOT / "chnroutes.txt", v4)

    meta = ROOT / "metadata.json"
    import json

    meta.write_text(
        json.dumps(
            {
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "ipv4_count": len(v4),
                "ipv6_count": len(v6),
                "source": source,
                "aggregated": not args.no_aggregate,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"IPv4: {len(v4)} routes -> chnroutes-v4, chnroutes.txt")
    print(f"IPv6: {len(v6)} routes -> chnroutes-v6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
