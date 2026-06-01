# 🎉 100% FREE Backend Architecture for Lee Hydraulics

> Complete serverless solution with zero monthly costs, perfect for small business

---

## 📊 FREE TECH STACK

### **Frontend Hosting**
- **GitHub Pages** - FREE ✅
  - Unlimited bandwidth
  - Custom domain support
  - HTTPS/SSL included
  - No build process needed

### **Backend Services (All FREE)**

| Service | Free Tier | Use Case | Cost |
|---------|-----------|----------|------|
| **Supabase** | 500MB DB, 2GB storage | PostgreSQL database | ₹0 |
| **Vercel Functions** | 100GB/month bandwidth | Serverless API | ₹0 |
| **Netlify Functions** | 125k invocations/month | Serverless API | ₹0 |
| **Firebase** | 1GB storage, 100 connections | Real-time database | ₹0 |
| **Formspree** | 50 submissions/month | Form handling | ₹0 |
| **Basin** | Unlimited submissions | Form handling | ₹0 |
| **SendGrid** | 100 emails/day | Email service | ₹0 |
| **Mailgun** | 5000 emails/month | Email service | ₹0 |
| **Cloudinary** | 25GB storage | Image hosting | ₹0 |
| **Imgur** | Unlimited uploads | Image hosting | ₹0 |
| **GitHub Actions** | 2000 minutes/month | Automation | ₹0 |

---

## 🏗️ RECOMMENDED FREE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Pages                         │
│              (Frontend + Static Assets)                 │
│                    www.leehyd.com                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌──────────┐
   │ Supabase│  │ Vercel  │  │ SendGrid │
   │   DB    │  │Functions│  │  Email   │
   │ (FREE)  │  │ (FREE)  │  │ (FREE)   │
   └─��───────┘  └─────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │   Admin Panel (React)   │
        │  Deployed on Vercel     │
        │      (FREE)             │
        └────────────────────────┘
```

---

## 🔧 SETUP GUIDE: 100% FREE BACKEND

### **STEP 1: Supabase (Database) - FREE**

#### What is Supabase?
- Open-source Firebase alternative
- PostgreSQL database
- Real-time subscriptions
- Built-in authentication
- Free tier: 500MB storage, 2GB bandwidth

#### Setup:
```bash
1. Go to https://supabase.com
2. Sign up with GitHub (free)
3. Create new project
4. Choose region closest to you
5. Get API keys from Settings → API
```

#### Database Schema:
```sql
-- Leads Table
CREATE TABLE leads (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  company TEXT,
  message TEXT,
  source TEXT DEFAULT 'contact',
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Blog Posts Table
CREATE TABLE blog_posts (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT NOT NULL,
  excerpt TEXT,
  featured_image TEXT,
  author TEXT,
  category TEXT,
  tags TEXT[],
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  status TEXT DEFAULT 'draft',
  views_count INT DEFAULT 0
);

-- Admin Users Table
CREATE TABLE admin_users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT,
  role TEXT DEFAULT 'editor',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Newsletter Subscribers
CREATE TABLE newsletter_subscribers (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP DEFAULT NOW(),
  verified BOOLEAN DEFAULT FALSE
);
```

---

### **STEP 2: Vercel Functions (Backend API) - FREE**

#### What is Vercel?
- Serverless functions (like AWS Lambda)
- Free tier: 100GB bandwidth, unlimited functions
- Auto-scales to zero (pay only for what you use)
- Perfect for small businesses

#### Setup:
```bash
1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your GitHub repository
4. Deploy automatically on every push
```

#### Create API Functions:

**File: `api/leads.js`**
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // POST: Submit new lead
  if (req.method === 'POST') {
    try {
      const { name, email, phone, company, message, source } = req.body;

      // Validation
      if (!name || !email || !message) {
        return res.status(400).json({ error: 'Missing required fields' });
      }

      // Insert into Supabase
      const { data, error } = await supabase
        .from('leads')
        .insert([
          {
            name,
            email,
            phone,
            company,
            message,
            source: source || 'contact',
            status: 'new'
          }
        ]);

      if (error) throw error;

      // Send email notification (using SendGrid)
      await sendEmailNotification(email, name);

      return res.status(201).json({
        success: true,
        message: 'Lead submitted successfully'
      });
    } catch (error) {
      console.error('Error:', error);
      return res.status(500).json({ error: error.message });
    }
  }

  // GET: Fetch all leads (admin only)
  if (req.method === 'GET') {
    try {
      const { data, error } = await supabase
        .from('leads')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) throw error;

      return res.status(200).json(data);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
}

async function sendEmailNotification(email, name) {
  // Implementation in next section
}
```

**File: `api/blog.js`**
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // GET: Fetch all published posts
  if (req.method === 'GET') {
    try {
      const { data, error } = await supabase
        .from('blog_posts')
        .select('*')
        .eq('status', 'published')
        .order('published_at', { ascending: false });

      if (error) throw error;

      return res.status(200).json(data);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }

  // POST: Create new blog post (admin only)
  if (req.method === 'POST') {
    try {
      const { title, slug, content, excerpt, featured_image, category, tags } = req.body;

      const { data, error } = await supabase
        .from('blog_posts')
        .insert([
          {
            title,
            slug,
            content,
            excerpt,
            featured_image,
            category,
            tags,
            status: 'draft',
            author: 'Admin'
          }
        ]);

      if (error) throw error;

      return res.status(201).json(data);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
}
```

---

### **STEP 3: SendGrid (Email) - FREE**

#### Setup:
```bash
1. Go to https://sendgrid.com
2. Sign up (free tier: 100 emails/day)
3. Create API key
4. Add to Vercel environment variables
```

#### Email Function:
```javascript
// api/send-email.js
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { to, subject, html } = req.body;

    await sgMail.send({
      to,
      from: 'noreply@leehyd.com',
      subject,
      html
    });

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Email error:', error);
    return res.status(500).json({ error: error.message });
  }
}
```

---

### **STEP 4: Cloudinary (Image Hosting) - FREE**

#### Setup:
```bash
1. Go to https://cloudinary.com
2. Sign up (free tier: 25GB storage)
3. Get API credentials
4. Use upload widget in admin panel
```

#### Upload Widget:
```html
<script src="https://upload-widget.cloudinary.com/latest/index.js"></script>

<button onclick="uploadImage()">Upload Image</button>

<script>
function uploadImage() {
  cloudinary.openUploadWidget(
    {
      cloudName: 'YOUR_CLOUD_NAME',
      uploadPreset: 'YOUR_PRESET',
      sources: ['local', 'url', 'camera']
    },
    (error, result) => {
      if (!error && result && result.event === 'success') {
        console.log('Image URL:', result.info.secure_url);
      }
    }
  );
}
</script>
```

---

### **STEP 5: GitHub Actions (Automation) - FREE**

#### Auto-send daily digest email:
```yaml
# .github/workflows/daily-digest.yml
name: Daily Lead Digest

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily

jobs:
  send-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Send digest email
        run: |
          curl -X POST https://your-vercel-app.vercel.app/api/send-digest \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@leehyd.com"}'
```

---

## 📱 ADMIN PANEL (React + Vercel) - FREE

### Deploy React Admin Panel:

**File: `admin/package.json`**
```json
{
  "name": "lee-admin",
  "version": "1.0.0",
  "scripts": {
    "dev": "react-scripts start",
    "build": "react-scripts build",
    "deploy": "vercel"
  },
  "dependencies": {
    "react": "^18.0.0",
    "@supabase/supabase-js": "^2.0.0",
    "react-router-dom": "^6.0.0"
  }
}
```

**File: `admin/src/App.jsx`**
```jsx
import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.REACT_APP_SUPABASE_URL,
  process.env.REACT_APP_SUPABASE_KEY
);

export default function AdminPanel() {
  const [leads, setLeads] = useState([]);
  const [posts, setPosts] = useState([]);
  const [activeTab, setActiveTab] = useState('leads');

  useEffect(() => {
    fetchLeads();
    fetchPosts();
  }, []);

  async function fetchLeads() {
    const { data } = await supabase
      .from('leads')
      .select('*')
      .order('created_at', { ascending: false });
    setLeads(data || []);
  }

  async function fetchPosts() {
    const { data } = await supabase
      .from('blog_posts')
      .select('*')
      .order('created_at', { ascending: false });
    setPosts(data || []);
  }

  async function updateLeadStatus(id, status) {
    await supabase
      .from('leads')
      .update({ status })
      .eq('id', id);
    fetchLeads();
  }

  async function deletePost(id) {
    await supabase
      .from('blog_posts')
      .delete()
      .eq('id', id);
    fetchPosts();
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Lee Hydraulics Admin Panel</h1>

      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={() => setActiveTab('leads')}
          style={{
            padding: '10px 20px',
            marginRight: '10px',
            background: activeTab === 'leads' ? '#5CB82E' : '#ccc',
            color: activeTab === 'leads' ? 'white' : 'black',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Leads ({leads.length})
        </button>
        <button
          onClick={() => setActiveTab('blog')}
          style={{
            padding: '10px 20px',
            background: activeTab === 'blog' ? '#5CB82E' : '#ccc',
            color: activeTab === 'blog' ? 'white' : 'black',
            border: 'none',
            cursor: 'pointer'
          }}
        >
          Blog Posts ({posts.length})
        </button>
      </div>

      {activeTab === 'leads' && (
        <div>
          <h2>Leads Management</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f0f0f0' }}>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Name</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Email</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Status</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Date</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '10px' }}>{lead.name}</td>
                  <td style={{ padding: '10px' }}>{lead.email}</td>
                  <td style={{ padding: '10px' }}>
                    <select
                      value={lead.status}
                      onChange={(e) => updateLeadStatus(lead.id, e.target.value)}
                      style={{ padding: '5px' }}
                    >
                      <option>new</option>
                      <option>contacted</option>
                      <option>converted</option>
                    </select>
                  </td>
                  <td style={{ padding: '10px' }}>
                    {new Date(lead.created_at).toLocaleDateString()}
                  </td>
                  <td style={{ padding: '10px' }}>
                    <button
                      onClick={() => alert(lead.message)}
                      style={{
                        padding: '5px 10px',
                        background: '#5CB82E',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer'
                      }}
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === 'blog' && (
        <div>
          <h2>Blog Posts</h2>
          <button
            style={{
              padding: '10px 20px',
              background: '#5CB82E',
              color: 'white',
              border: 'none',
              cursor: 'pointer',
              marginBottom: '20px'
            }}
          >
            New Post
          </button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f0f0f0' }}>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Title</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Status</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Date</th>
                <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {posts.map((post) => (
                <tr key={post.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '10px' }}>{post.title}</td>
                  <td style={{ padding: '10px' }}>{post.status}</td>
                  <td style={{ padding: '10px' }}>
                    {new Date(post.created_at).toLocaleDateString()}
                  </td>
                  <td style={{ padding: '10px' }}>
                    <button
                      onClick={() => deletePost(post.id)}
                      style={{
                        padding: '5px 10px',
                        background: '#ff4444',
                        color: 'white',
                        border: 'none',
                        cursor: 'pointer'
                      }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
```

---

## 🚀 DEPLOYMENT STEPS

### **1. Deploy Frontend (GitHub Pages)**
```bash
# Already done - your index.html is live
# Just push changes to GitHub
git add .
git commit -m "Update website"
git push origin main
```

### **2. Deploy Backend (Vercel)**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add SENDGRID_API_KEY
```

### **3. Deploy Admin Panel (Vercel)**
```bash
cd admin
vercel
```

---

## 📊 COST BREAKDOWN (100% FREE)

| Service | Free Tier | Cost |
|---------|-----------|------|
| GitHub Pages | Unlimited | ₹0 |
| Vercel Functions | 100GB/month | ₹0 |
| Supabase DB | 500MB | ₹0 |
| SendGrid Email | 100/day | ₹0 |
| Cloudinary Images | 25GB | ₹0 |
| GitHub Actions | 2000 min/month | ₹0 |
| **TOTAL** | - | **₹0/month** |

---

## 🔒 SECURITY BEST PRACTICES

### **1. Environment Variables**
```bash
# .env.local (never commit this)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SENDGRID_API_KEY=xxx
CLOUDINARY_NAME=xxx
```

### **2. Row Level Security (Supabase)**
```sql
-- Only authenticated users can view leads
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Only admins can view leads"
  ON leads FOR SELECT
  USING (auth.uid() IN (SELECT id FROM admin_users));
```

### **3. Rate Limiting**
```javascript
// api/middleware/rateLimit.js
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

module.exports = limiter;
```

---

## 📈 SCALING (Still FREE!)

| Metric | Free Tier | When to Upgrade |
|--------|-----------|-----------------|
| Database | 500MB | > 500MB data |
| Bandwidth | 2GB | > 2GB/month |
| Emails | 100/day | > 100/day |
| Functions | Unlimited | > 100GB/month |
| Storage | 25GB | > 25GB images |

**Upgrade cost when needed: ₹500-2000/month**

---

## 🎯 QUICK START CHECKLIST

- [ ] Create Supabase account
- [ ] Create database tables
- [ ] Create Vercel account
- [ ] Deploy API functions
- [ ] Create SendGrid account
- [ ] Get API keys
- [ ] Add environment variables to Vercel
- [ ] Deploy admin panel
- [ ] Test contact form
- [ ] Test email notifications
- [ ] Monitor usage

---

## 📞 SUPPORT & RESOURCES

- **Supabase Docs:** https://supabase.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **SendGrid Docs:** https://docs.sendgrid.com
- **Cloudinary Docs:** https://cloudinary.com/documentation

---

## ✅ WHAT YOU GET (100% FREE)

✅ Contact form with email notifications  
✅ Lead management dashboard  
✅ Blog system with admin panel  
✅ Image hosting and optimization  
✅ Email marketing capability  
✅ Analytics and reporting  
✅ Automatic backups  
✅ SSL/HTTPS  
✅ Custom domain  
✅ Unlimited scalability  

**All for ₹0/month!**

---

## 🚨 LIMITATIONS & WORKAROUNDS

| Limitation | Free Tier | Workaround |
|-----------|-----------|-----------|
| 100 emails/day | SendGrid | Use Mailgun (5000/month) |
| 500MB database | Supabase | Archive old leads |
| 25GB images | Cloudinary | Compress images |
| 100GB bandwidth | Vercel | Use CDN caching |

---

## 🎓 NEXT STEPS

1. **Follow the setup guide above**
2. **Deploy each service one by one**
3. **Test thoroughly**
4. **Monitor free tier usage**
5. **Upgrade only when needed**

**Estimated setup time: 2-3 hours**

---

**Created for Lee Hydraulics & Fasteners - 100% Free Forever! 🚀**
