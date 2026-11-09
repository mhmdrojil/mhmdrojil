# Hi, I'm Rojil 👋

Teknik Informatika graduate building full-stack business systems from Gorontalo, Indonesia.

Currently focused on **Permata Tech** — a multi-branch mobile credit (pulsa) management system built on a serverless-first architecture.

---

## 🚀 What I'm Building

### [Permata Tech](https://permatatech.com)
A full-stack business management system for a multi-branch pulsa operation — handling transactions, attendance, payroll, and inventory through Telegram bots and a web dashboard.

**Architecture:**
- **Backend** — Cloudflare Workers (Hono) with service bindings between workers
- **Database** — Supabase (PostgreSQL + PostgREST)
- **Frontend** — React + Next.js apps deployed on Vercel
- **Bots** — Telegram as the primary user interface for field staff
- **Auth** — Clerk (OAuth for dashboard)
- **Monorepo** — pnpm workspaces + Turborepo

```
apps/
├── konterku/   → Internal Apps (React + Vite + TS)

workers/
├── rekap-bot/       → Transaction tracking bot
├── absen-bot/       → Attendance bot with cron reminders
└── backend-api/     → Main REST API (Hono)

packages/
├── @permata/types
├── @permata/services
├── @permata/supabase
├── @permata/lib
└── @permata/backend-adapter
```

---

## 🛠 Tech Stack

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=flat-square&logo=cloudflare&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Hono](https://img.shields.io/badge/Hono-E36002?style=flat-square&logo=hono&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

---

## 📫 Find Me

[![Twitter](https://img.shields.io/badge/@mhmdrojil-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/mhmdrojil)
[![Instagram](https://img.shields.io/badge/@mhmdrojil-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://instagram.com/mhmdrojil)
[![Website](https://img.shields.io/badge/permatatech.com-000000?style=flat-square&logo=vercel&logoColor=white)](https://permatatech.com)

---

> Most of this wouldn't exist without AI-assisted development — proudly built with Claude by Anthropic.
