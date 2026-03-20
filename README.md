# Lee Hydraulics & Fasteners (P) Ltd.
### Corporate Portfolio Website

> Precision manufacturer of DTH hammers, hydraulic fittings, drill bits, and industrial fasteners.  
> Est. 1991 · Hyderabad, India · Serving 17+ countries

---

## 🌐 Live Site
**[www.leehyd.com](https://www.leehyd.com)**  
Hosted on GitHub Pages with custom domain.

---

## 📁 Repository Structure

```
leehyd-site/
├── index.html        ← Complete 7-page portfolio website (single file)
├── 404.html          ← Custom 404 with auto-redirect
├── CNAME             ← Custom domain: www.leehyd.com
├── robots.txt        ← Search engine crawl rules
├── sitemap.xml       ← SEO sitemap
└── README.md         ← This file
```

---

## 🚀 Deployment (GitHub Pages)

### Step 1 — Create Repository
```bash
# On GitHub.com → New repository
# Name: leehyd-site  (or your-username.github.io for root domain)
# Visibility: Public
# Do NOT initialise with README
```

### Step 2 — Push Files
```bash
git init
git add .
git commit -m "Initial site deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/leehyd-site.git
git push -u origin main
```

### Step 3 — Enable GitHub Pages
```
GitHub → Repository → Settings → Pages
Source: Deploy from branch → main → / (root)
Save
```
Site will be live at `https://YOUR_USERNAME.github.io/leehyd-site` within 2 minutes.

### Step 4 — Connect Custom Domain

**In GitHub Pages settings:**
```
Custom domain: www.leehyd.com → Save
✓ Enforce HTTPS (tick this — free SSL via Let's Encrypt)
```

**In your domain registrar (DNS settings):**
```
Type    Name    Value                   TTL
A       @       185.199.108.153         3600
A       @       185.199.109.153         3600
A       @       185.199.110.153         3600
A       @       185.199.111.153         3600
CNAME   www     YOUR_USERNAME.github.io 3600
```

DNS propagation: **24–48 hours**. After that, `https://www.leehyd.com` will serve your site.

---

## 🗄️ Database Plan

The current site is **fully static** — no database needed for:
- All 7 pages (Home, About, Segments, Capabilities, Investors, Careers, Contact)
- All animations, cursor, responsive layouts
- OEM logos, certifications, team cards

### When to add a database

| Feature | Tool | Monthly Cost |
|---|---|---|
| Contact form submissions | Supabase (free tier) | ₹0 |
| Press release CMS | Contentful free tier | ₹0 |
| Investor document library | Supabase + Storage | ₹0–800 |
| Career applications | Supabase or Airtable | ₹0–500 |
| Analytics | Plausible or GA4 | ₹0 |

**Recommended stack if needed:**  
`GitHub Pages (static) + Supabase (PostgreSQL) + Netlify Forms`

---

## ✏️ How to Update Content

All content lives in `index.html`. Use Ctrl+F to find sections:

| Section | Search for |
|---|---|
| Hero text | `powers the impossible` |
| Stats numbers | `hs-n` |
| About founder | `Rajesh Kumar Lee` |
| Team cards | `cards-grid` |
| Timeline | `1991` |
| Segments | `pg-segments` |
| OEM logos | `oem-row` |
| Contact info | `leehyd.com` |
| Footer | `site-footer` |

---

## 🎨 Design System

| Token | Value | Usage |
|---|---|---|
| `--g1` | `#5CB82E` | Primary green — buttons, links, accents |
| `--g2` | `#6ECF3B` | Hover state |
| `--g3` | `#A8E070` | Italic serif accents, pale tints |
| `--ink` | `#07090B` | Page background |
| `--ink2` | `#0C1016` | Surface / card background |
| `--silver` | `#8795A5` | Body text |
| `--cream` | `#ECE7DC` | Primary text |

**Fonts:** Cormorant Garamond (display) · DM Sans (body)

---

## 📱 Responsive Breakpoints

| Breakpoint | Layout |
|---|---|
| > 1024px | Full desktop — all grids, full nav |
| 768–1024px | Tablet — hamburger menu, 2-col grids |
| < 640px | Mobile — single column, touch-optimised |

---

## 📜 Licence
© 2025 Lee Hydraulics & Fasteners (P) Ltd. All rights reserved.
