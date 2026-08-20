<div align="center">

# INCY

**Cross-platform proxy client built on [Xray-core](https://github.com/XTLS/Xray-core)**

[![Website](https://img.shields.io/badge/incy.cc-6c5ce7?style=flat-square&logo=safari&logoColor=white)](https://incy.cc)
[![Docs](https://img.shields.io/badge/Documentation-346DDB?style=flat-square&logo=gitbook&logoColor=white)](https://docs.incy.cc)
[![Report a bug](https://img.shields.io/badge/Report_a_bug-feedback.incy.cc-2ea44f?style=flat-square&logo=github&logoColor=white)](https://feedback.incy.cc)
[![iOS](https://img.shields.io/badge/iOS-App_Store-0D96F6?style=flat-square&logo=app-store&logoColor=white)](https://apps.apple.com/ru/app/incy/id6756943388)
[![Android](https://img.shields.io/badge/Android-Google_Play-414141?style=flat-square&logo=google-play&logoColor=white)](https://play.google.com/store/apps/details?id=llc.itdev.incy)
[![Telegram](https://img.shields.io/badge/Telegram-incy__public-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/incy_public)

</div>

## Downloads

### Mobile & TV

| Platform | Link |
|:---------|:-----|
| iOS / Apple TV / macOS | [App Store](https://apps.apple.com/ru/app/incy/id6756943388) |
| Android / Android TV | [Google Play](https://play.google.com/store/apps/details?id=llc.itdev.incy) |
| Android APK (sideload) | [Download APK](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/Incy.apk) |

### Desktop

> [!WARNING]
> The desktop client is **pre-alpha**. It is usable day to day, but expect rough
> edges and breaking changes between releases. Please report anything you hit at
> [feedback.incy.cc](https://feedback.incy.cc) — that is exactly what this stage
> is for.

| Platform | Installer | Portable |
|:---------|:----------|:---------|
| Windows (x64 / ARM64) | [Setup](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-windows-setup.exe) | [ZIP](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-windows-portable.zip) |
| macOS (Apple Silicon) | [DMG](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-macos-arm64.dmg) | — |
| macOS (Intel) | [DMG](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-macos-intel.dmg) | — |
| Linux (x64) | [DEB](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-x64.deb) · [RPM](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-x64.rpm) · [Arch](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-x64.pkg.tar.zst) | [ZIP](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-x64-portable.zip) |
| Linux (ARM64) | [DEB](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-arm64.deb) · [RPM](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-arm64.rpm) | [ZIP](https://github.com/INCY-DEV/incy-platforms/releases/latest/download/incy-linux-arm64-portable.zip) |

## Protocols

`VLESS (Reality)` `VMess` `Trojan` `Shadowsocks` `Hysteria2` `SOCKS5` `WireGuard`

## Features

| | Mobile & TV | Desktop |
|:--|:-:|:-:|
| **Subscriptions** — add by URL, QR or share link, with auto-refresh | ✅ | ✅ |
| **Routing profiles** — split traffic by domain/IP into proxy, direct or block, with separate remote and domestic DNS | ✅ | ✅ |
| **Full config import** — raw Xray JSON, including observatory, balancers and custom geo files | ✅ | ✅ |
| **TLS fragmentation** — fragment ClientHello past DPI; packet type, length and interval are configurable | ✅ | ✅ |
| **Kill switch** — cut traffic if the tunnel drops, so nothing escapes through the gap | ✅ | ✅ |
| **Per-app proxy** — route or exclude individual apps | Android | ✅ |
| **Send to TV** — push a subscription or a single server to Apple TV / Android TV by QR or pairing code | ✅ | — |
| **Shortcuts & widgets** — connect, disconnect and check status without opening the app | ✅ | Tray |
| **Customization** — 16 app icons and several themes | ✅ | ✅ |

**Privacy** — servers, keys and subscriptions never leave your device. Mobile
builds include Firebase Crashlytics for crash reports; the desktop client sends
no telemetry at all.

## Documentation

Setup guides, configuration reference and troubleshooting —
**[docs.incy.cc](https://docs.incy.cc)**

## Bug reports & feature requests

> [!IMPORTANT]
> All reports go through **[feedback.incy.cc](https://feedback.incy.cc)** — the
> only place we track them. Anything sent to chat, DMs or GitHub issues will get
> lost.

Include the app version, your platform, and what you expected to happen instead.
For tunnel problems, attach the logs from Settings.

Questions, setup help and general discussion — [@incy_public](https://t.me/incy_public).

## Support the project

INCY is free, collects nothing and sells nothing. If it is useful to you, a
donation keeps it that way.

- **[@incyhelperbot](https://t.me/incyhelperbot)** — cards, Telegram Stars, and support
- **[OxaPay](https://pay.oxapay.com/16388144)** — BTC, ETH, USDT and others

## Legal

INCY does not provide VPN services. Users are responsible for their own servers and must comply with local laws.
