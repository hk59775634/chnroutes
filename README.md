# chnroutes

自动从 [APNIC Delegated Statistics](https://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest) 提取并聚合**中国大陆** IPv4 / IPv6 路由表，供路由器、OpenVPN、Clash、iptables 等分流场景使用。

- 默认分支：`main`
- 更新频率：**每天 00:00 UTC**（北京时间 08:00），也可在 [Actions](https://github.com/hk59775634/chnroutes/actions) 手动触发
- 数据格式：每行一个 CIDR（如 `1.0.1.0/24`）

## 文件说明

| 文件 | 说明 |
|------|------|
| `chnroutes.txt` | 中国大陆 IPv4（兼容旧版工具命名） |
| `chnroutes-v4` | 中国大陆 IPv4 |
| `chnroutes-v6` | 中国大陆 IPv6 |
| `metadata.json` | 更新时间、条目数量等元信息 |

---

## 直接下载（复制链接即可）

将下面链接粘贴到浏览器、`wget`、`curl` 或路由器「远程 URL」配置中即可下载。

### GitHub 官方 Raw（海外或已可访问 GitHub 时）

```
https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes.txt
https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes-v4
https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes-v6
https://raw.githubusercontent.com/hk59775634/chnroutes/main/metadata.json
```

### jsDelivr CDN（国内通常较稳定）

```
https://cdn.jsdelivr.net/gh/hk59775634/chnroutes@main/chnroutes.txt
https://cdn.jsdelivr.net/gh/hk59775634/chnroutes@main/chnroutes-v4
https://cdn.jsdelivr.net/gh/hk59775634/chnroutes@main/chnroutes-v6
https://cdn.jsdelivr.net/gh/hk59775634/chnroutes@main/metadata.json
```

### GitHub 代理 / 镜像（前缀 + 官方 Raw 地址）

以下服务为第三方公益或社区代理，**可用性与合规性会变化**，请自行甄别后使用。用法：在官方 Raw 链接前加上代理前缀。

| 代理服务 | 前缀（拼在 `https://raw.githubusercontent.com/...` 前面） |
|----------|-----------------------------------------------------------|
| ghproxy.net | `https://ghproxy.net/` |
| gh-proxy.com | `https://gh-proxy.com/` |
| mirror.ghproxy.com | `https://mirror.ghproxy.com/` |
| ghps.cc | `https://ghps.cc/` |

**示例**（通过 ghproxy 下载 `chnroutes-v4`）：

```
https://ghproxy.net/https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes-v4
```

**示例**（通过 gh-proxy 下载 `chnroutes.txt`）：

```
https://gh-proxy.com/https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes.txt
```

### 命令行示例

```bash
# 官方 Raw
curl -fsSL -o chnroutes-v4 \
  https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes-v4

# jsDelivr（国内推荐）
curl -fsSL -o chnroutes-v4 \
  https://cdn.jsdelivr.net/gh/hk59775634/chnroutes@main/chnroutes-v4

# 经 ghproxy
curl -fsSL -o chnroutes-v4 \
  "https://ghproxy.net/https://raw.githubusercontent.com/hk59775634/chnroutes/main/chnroutes-v4"
```

---

## 使用场景

- **VPN 分流**：连接 VPN 后，将中国 IP 走本地网关，减轻隧道负载（参见经典 [chnroutes](https://github.com/jimmyxu/chnroutes) 思路）
- **路由器 / 防火墙**：导入静态路由或地址列表
- **代理规则**：将 CIDR 转为 Clash / Surge / sing-box 的 `ip-cidr` 规则

> 路由表会随运营商分配变化，建议订阅本仓库自动更新，或定期重新下载。

---

## 本地生成

```bash
git clone https://github.com/hk59775634/chnroutes.git
cd chnroutes
python scripts/generate.py --download
```

仅使用已有 `delegated-apnic-latest` 文件、且不做聚合：

```bash
python scripts/generate.py --no-aggregate
```

---

## 数据来源与许可

- 数据来源：[APNIC](https://www.apnic.net/) `delegated-apnic-latest`，筛选 `registry=apnic` 且 `country=CN` 的 IPv4/IPv6 分配记录
- 本仓库脚本与生成文件以 [MIT](LICENSE) 许可发布
- APNIC 数据使用须遵守 [APNIC 使用条款](https://www.apnic.net/about-apnic/whois_search/use-terms/)

---

## 相关项目

- [jimmyxu/chnroutes](https://github.com/jimmyxu/chnroutes) — 早期 OpenVPN 路由脚本
- [misakaio/chnroutes2](https://github.com/misakaio/chnroutes2) — 基于 BGP 的聚合路由
- [windmgc/chnroute_auto](https://github.com/windmgc/chnroute_auto) — 每小时 APNIC 自动更新

---

## 免责声明

本项目仅供学习与网络配置参考。路由数据来自公开注册库，不保证完整覆盖所有「中国可用」或「需直连」的地址段；使用第三方 GitHub 代理时请自行评估安全风险。
