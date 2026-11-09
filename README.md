# Hi, I'm Rojil 👋

Teknik Informatika graduate building full-stack business systems from Gorontalo, Indonesia.

Currently focused on **Permata Tech** — a multi-branch mobile credit (pulsa) management system built on a serverless-first architecture.

---

## 🚀 What I'm Building

### [Permata Tech](https://permatatech.com)
A full-stack business management system for a multi-branch pulsa operation — handling transactions, attendance, payroll, and inventory through Telegram bots and a web dashboard.

**Architecture:**
- **Backend** — 4 Cloudflare Workers (Hono): REST API + 2 Telegram bots + log consumer, wired with service bindings
- **Database** — Supabase (PostgreSQL + PostgREST), 27 tables
- **Frontend** — React + Vite dashboard (Konterku), deployed on Vercel and packaged for Android with Capacitor
- **Bots** — Telegram as the primary user interface for field staff
- **Auth** — Supabase Auth (dashboard login)
- **Monorepo** — pnpm workspaces + Turborepo

```
apps/
└── konterku/            → Internal dashboard (React + Vite + TS, Capacitor Android)

worker/
├── rekap-bot/           → Transactions, balance, debts, daily reports (Telegram)
├── absen-bot/           → Attendance, bonus, payroll, evaluation (Telegram + cron)
├── backend-api/         → REST API (Hono), called by dashboard and bots
└── tail-worker/         → Centralized logging / Tail consumer

packages/
├── @permata/types
├── @permata/services
├── @permata/supabase
├── @permata/lib
├── @permata/backend-adapter
├── @permata/bavovoa
└── @permata/tsconfig
```

---

## 🛠 Tech Stack

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=flat-square&logo=cloudflare&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Hono](https://img.shields.io/badge/Hono-E36002?style=flat-square&logo=hono&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

---

## 📊 GitHub Stats

<!-- STATS:START -->
**Repos** 14 · **Public** 11 · **Private** 3 · **Stars** 0 · **Forks** 0 · **Followers** 0 · **Following** 0 · **Commits** 1,885

_Updated 2026-11-09 18:39 UTC_

### Languages
```
TypeScript     █████████████████░  95.8%
C++            █░░░░░░░░░░░░░░░░░   4.1%
```

| Recently updated | ★ | Language |
| --- | --: | --- |
| [HumidityMonitoringRoom](https://github.com/mhmdrojil/HumidityMonitoringRoom) | 0 | C++ |
| [ESP32AutomaticDrying](https://github.com/mhmdrojil/ESP32AutomaticDrying) — an automatic drying ESP32 using Fuzzy Mamdani model | 0 | C++ |
| [ironDetector](https://github.com/mhmdrojil/ironDetector) — an iron detector for trash classification using fuzzy mamdani model | 0 | C++ |
| [pulseDetectorHealth](https://github.com/mhmdrojil/pulseDetectorHealth) | 0 | C++ |
| [fingerprintLock](https://github.com/mhmdrojil/fingerprintLock) — a fingerprint door lock using bluetooth android | 0 | C++ |
<!-- STATS:END -->

_Refreshed automatically every day by [`.github/workflows/readme-stats.yml`](.github/workflows/readme-stats.yml)._

---

> Most of this wouldn't exist without AI-assisted development — proudly built with [opencode](https://opencode.ai).
