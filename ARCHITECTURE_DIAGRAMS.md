# 🏗️ ARCHITECTURE DIAGRAMS

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS                                   │
│                    (Visitors & Admin)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌──────────────┐         ┌──────────────┐
        │ Website      │         │ Admin Panel  │
        │ (GitHub      ��         │ (React on    │
        │  Pages)      │         │  Vercel)     │
        │ www.leehyd   │         │ admin.leehyd │
        │ .com         │         │ .com         │
        └──────┬───────┘         └──────┬───────┘
               │                        │
               └────────────┬───────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌──────────────────┐   ┌──────────────────┐
        │  Vercel API      │   │  Vercel API      │
        │  Functions       │   │  Functions       │
        │                  │   │                  │
        │ /api/leads       │   │ /api/blog        │
        │ /api/newsletter  │   │ /api/newsletter  │
        └────────┬─────────┘   └────────┬─────────┘
                 │                      │
        ┌────────┴──────────────────────┴────────┐
        │                                         │
        ▼                                         ▼
    ┌─────────────┐                         ┌──────────────┐
    │  Supabase   │                         │  SendGrid    │
    │  Database   │                         │  Email       │
    │             │                         │              │
    │ - leads     │                         │ - Send       │
    │ - blog      │                         │   emails     │
    │ - users     │                         │ - Track      │
    │ - newsletter│                         │   delivery   │
    └─────────────┘                         └──────────────┘
        │
        ▼
    ┌──────────────┐
    │ Cloudinary   │
    │ Images       │
    │              │
    │ - Store      │
    │ - Optimize   │
    │ - Deliver    │
    └──────────────┘
```

---

## Data Flow: Contact Form Submission

```
User fills form
    │
    ▼
┌─────────────────────────┐
│ Client-side validation  │
│ (HTML5 + JavaScript)    │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────┐
    │ Send to API    │
    │ /api/leads     │
    └────────┬───────┘
             │
             ▼
    ┌────────────────────────┐
    │ Vercel Function        │
    │ - Validate input       │
    │ - Check for spam       │
    │ - Sanitize data        │
    └────────┬───────────────┘
             │
             ├─────────────────────┐
             │                     │
             ▼                     ▼
    ┌──────────────────┐  ┌──────────────��───┐
    │ Save to Supabase │  │ Send Email via   │
    │ leads table      │  │ SendGrid         │
    └──────────────────┘  └──────────────────┘
             │                     │
             ├─────────────────────┤
             │                     │
             ▼                     ▼
    ┌──────────────────────────────────────┐
    │ Return success response to user      │
    │ Show "Thank you" message             │
    └──────────────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────┐
    │ Admin sees new lead in dashboard     │
    │ Can update status and add notes      │
    └──────────────────────────────────────┘
```

---

## Data Flow: Blog Post Creation

```
Admin writes blog post
    │
    ▼
┌──────────────────────┐
│ Admin Panel          │
│ (React)              │
│ - Title              │
│ - Content            │
│ - Featured image     │
│ - Category/tags      │
└──────────┬───────────┘
           │
           ▼
    ┌─────────────────┐
    │ Upload image to │
    │ Cloudinary      │
    └────────┬────────┘
             │
             ▼
    ┌──────────────────────┐
    │ Get image URL        │
    │ from Cloudinary      │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ Send to API              │
    │ POST /api/blog           │
    └──────────┬───────────────┘
               │
               ▼
    ┌─────────────────────��────┐
    │ Vercel Function          │
    │ - Validate data          │
    │ - Generate slug          │
    │ - Check for duplicates   │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ Save to Supabase         │
    │ blog_posts table         │
    │ - Status: draft/published│
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ Return post ID           │
    │ Show success message     │
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ Post appears on website  │
    │ if published             │
    └──────────────────────────┘
```

---

## Database Schema

```
┌─────────────────────────────────────────┐
│           LEADS TABLE                   │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ name (TEXT)                             │
│ email (TEXT)                            │
│ phone (TEXT)                            │
│ company (TEXT)                          │
│ message (TEXT)                          │
│ source (TEXT) - contact/inquiry/career  │
│ status (TEXT) - new/contacted/converted │
│ created_at (TIMESTAMP)                  │
│ updated_at (TIMESTAMP)                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│        BLOG_POSTS TABLE                 │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ title (TEXT)                            │
│ slug (TEXT) - UNIQUE                    │
│ content (TEXT)                          │
│ excerpt (TEXT)                          │
│ featured_image (TEXT)                   │
│ author (TEXT)                           │
│ category (TEXT)                         │
│ tags (TEXT[])                           │
│ status (TEXT) - draft/published         │
│ published_at (TIMESTAMP)                │
│ views_count (INT)                       │
│ created_at (TIMESTAMP)                  │
│ updated_at (TIMESTAMP)                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│   NEWSLETTER_SUBSCRIBERS TABLE          │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ email (TEXT) - UNIQUE                   │
│ verified (BOOLEAN)                      │
│ subscribed_at (TIMESTAMP)               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       ADMIN_USERS TABLE                 │
├─────────────────────────────────────────┤
│ id (PK)                                 │
│ email (TEXT) - UNIQUE                   │
│ password_hash (TEXT)                    │
│ name (TEXT)                             │
│ role (TEXT) - admin/editor/viewer       │
│ created_at (TIMESTAMP)                  │
└─────────────────────────────────────────┘
```

---

## API Endpoints

```
LEADS ENDPOINTS
├── POST /api/leads
│   └── Submit new lead
��       Input: { name, email, phone, company, message, source }
│       Output: { success, message, lead_id }
│
├── GET /api/leads
│   └── Get all leads (admin only)
│       Auth: Bearer token required
│       Output: [{ id, name, email, status, ... }]
│
├── PUT /api/leads/:id
│   └── Update lead status
│       Input: { status }
│       Output: { success, updated_lead }
│
└── DELETE /api/leads/:id
    └── Delete lead
        Output: { success }

BLOG ENDPOINTS
├── GET /api/blog
│   └── Get all published posts
│       Query: ?category=xxx&limit=10&offset=0
│       Output: { posts: [], total, limit, offset }
│
├── GET /api/blog?slug=xxx
│   └── Get single post by slug
│       Output: { id, title, content, ... }
│
├── POST /api/blog
│   └── Create new post (admin only)
│       Input: { title, slug, content, excerpt, ... }
│       Output: { id, title, ... }
│
├── PUT /api/blog/:id
│   └── Update post (admin only)
│       Input: { title, content, status, ... }
│       Output: { id, title, ... }
│
└── DELETE /api/blog/:id
    └── Delete post (admin only)
        Output: { success }

NEWSLETTER ENDPOINTS
└── POST /api/newsletter
    ├── Subscribe
    │   Input: { email, action: 'subscribe' }
    │   Output: { success, message }
    │
    └── Unsubscribe
        Input: { email, action: 'unsubscribe' }
        Output: { success, message }
```

---

## Deployment Pipeline

```
┌──────────────────────────────────────────────────────────┐
│                    DEVELOPER                             │
│              (Makes code changes)                        │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Push to GitHub         │
            │ git push origin main   │
            └────────────┬────��──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │GitHub  │      │Vercel  │      │Vercel  │
    │Pages   │      │API     │      │Admin   │
    │Deploy  │      │Deploy  │      │Deploy  │
    └────┬───┘      └────┬───┘      └────┬───┘
         │               │               │
         ▼               ▼               ▼
    ┌────────────────────────────────────────┐
    │         LIVE WEBSITE                   │
    │  www.leehyd.com                        │
    │  api.leehyd.com                        │
    │  admin.leehyd.com                      │
    └────────────────────────────────────────┘
```

---

## Free Tier Limits

```
┌─────────────────────────────────────────────────────────┐
│              SERVICE LIMITS                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ GitHub Pages                                            │
│ ├─ Storage: Unlimited                                  │
│ ├─ Bandwidth: Unlimited                                │
│ └─ Domains: Unlimited                                  │
│                                                         │
│ Vercel Functions                                        │
│ ├─ Bandwidth: 100GB/month                              │
│ ├─ Invocations: Unlimited                              │
│ └─ Execution time: 30 seconds                          │
│                                                         │
│ Supabase                                                │
│ ├─ Database: 500MB                                     │
│ ├─ Bandwidth: 2GB/month                                │
│ └─ Connections: 10                                     │
│                                                         │
│ SendGrid                                                │
│ ├─ Emails: 100/day                                     │
│ ├─ Contacts: Unlimited                                 │
│ └─ Templates: Unlimited                                │
│                                                         │
│ Cloudinary                                              │
│ ├─ Storage: 25GB                                       │
│ ├─ Bandwidth: 25GB/month                               │
│ └─ Transformations: Unlimited                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Scaling Timeline

```
Month 1-6: FREE TIER
├─ 0-500 leads
├─ 0-3000 emails/month
├─ 0-100GB bandwidth
└─ Cost: ₹0/month

Month 6-12: GROWTH
├─ 500-2000 leads
├─ 3000-15000 emails/month
├─ 100-500GB bandwidth
└─ Cost: ₹0/month (still free)

Month 12-18: EXPANSION
├─ 2000-5000 leads
├─ 15000-50000 emails/month
├─ 500GB+ bandwidth
└─ Cost: ₹1500-2000/month (upgrade needed)

Month 18+: SCALE
├─ 5000+ leads
├─ 50000+ emails/month
├─ 1TB+ bandwidth
└─ Cost: ₹5000-10000/month (enterprise)
```

---

## Technology Stack Visualization

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
│  HTML5 | CSS3 | JavaScript | React (Admin)             │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    API LAYER                            │
│  Node.js | Express | Vercel Functions                  │
└─────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌────────────��─┐
│ DATABASE     │  │ EMAIL        │  │ STORAGE      │
│ Supabase     │  │ SendGrid     │  │ Cloudinary   │
│ PostgreSQL   │  │ SMTP         │  │ CDN          │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

**All diagrams show the complete architecture for Lee Hydraulics website!**
