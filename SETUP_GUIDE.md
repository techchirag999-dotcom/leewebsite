# 🚀 COMPLETE SETUP GUIDE: 100% FREE BACKEND

> Step-by-step guide to deploy Lee Hydraulics with zero monthly costs

---

## 📋 PREREQUISITES

- GitHub account (free)
- Custom domain (₹200-500/year)
- 30 minutes of setup time

---

## ✅ STEP 1: SUPABASE SETUP (Database)

### 1.1 Create Supabase Account
```
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (recommended)
4. Create new organization
```

### 1.2 Create Project
```
1. Click "New Project"
2. Name: "lee-hydraulics"
3. Database password: Create strong password
4. Region: Choose closest to India (Singapore or Mumbai)
5. Click "Create new project"
6. Wait 2-3 minutes for setup
```

### 1.3 Get API Keys
```
1. Go to Settings → API
2. Copy these values:
   - Project URL (SUPABASE_URL)
   - anon public key (SUPABASE_ANON_KEY)
   - service_role key (SUPABASE_SERVICE_KEY)
3. Save in safe place
```

### 1.4 Create Database Tables
```
1. Go to SQL Editor
2. Click "New Query"
3. Paste the SQL from "database-schema.sql" (see below)
4. Click "Run"
5. Repeat for all tables
```

**database-schema.sql:**
```sql
-- Create leads table
CREATE TABLE leads (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  company TEXT,
  message TEXT NOT NULL,
  source TEXT DEFAULT 'contact',
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create blog_posts table
CREATE TABLE blog_posts (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT NOT NULL,
  excerpt TEXT,
  featured_image TEXT,
  author TEXT DEFAULT 'Admin',
  category TEXT,
  tags TEXT[],
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  status TEXT DEFAULT 'draft',
  views_count INT DEFAULT 0
);

-- Create newsletter_subscribers table
CREATE TABLE newsletter_subscribers (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP DEFAULT NOW(),
  verified BOOLEAN DEFAULT FALSE
);

-- Create admin_users table
CREATE TABLE admin_users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT,
  role TEXT DEFAULT 'editor',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- Create indexes for faster queries
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_blog_slug ON blog_posts(slug);
CREATE INDEX idx_blog_status ON blog_posts(status);
CREATE INDEX idx_newsletter_email ON newsletter_subscribers(email);
```

---

## ✅ STEP 2: SENDGRID SETUP (Email)

### 2.1 Create SendGrid Account
```
1. Go to https://sendgrid.com
2. Click "Sign Up"
3. Fill in details
4. Verify email
5. Free tier: 100 emails/day
```

### 2.2 Create API Key
```
1. Go to Settings → API Keys
2. Click "Create API Key"
3. Name: "Lee Hydraulics"
4. Select "Full Access"
5. Copy the key (SENDGRID_API_KEY)
6. Save in safe place
```

### 2.3 Verify Sender Email
```
1. Go to Settings → Sender Authentication
2. Click "Verify a Single Sender"
3. Enter: noreply@leehyd.com
4. Verify via email link
```

---

## ✅ STEP 3: VERCEL SETUP (Backend API)

### 3.1 Create Vercel Account
```
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "GitHub"
4. Authorize Vercel
```

### 3.2 Import GitHub Repository
```
1. Click "New Project"
2. Select your GitHub repository
3. Click "Import"
4. Configure project:
   - Framework: Other
   - Root Directory: ./
   - Build Command: npm run build
   - Output Directory: dist
```

### 3.3 Add Environment Variables
```
1. Go to Settings → Environment Variables
2. Add each variable:

SUPABASE_URL = [your-supabase-url]
SUPABASE_ANON_KEY = [your-anon-key]
SENDGRID_API_KEY = [your-sendgrid-key]
ADMIN_EMAIL = admin@leehyd.com
ADMIN_URL = https://admin.leehyd.com
SITE_URL = https://www.leehyd.com

3. Click "Save"
4. Redeploy project
```

### 3.4 Deploy
```
1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Get your API URL: https://your-project.vercel.app
4. Test API: https://your-project.vercel.app/api/leads
```

---

## ✅ STEP 4: CLOUDINARY SETUP (Images)

### 4.1 Create Cloudinary Account
```
1. Go to https://cloudinary.com
2. Click "Sign Up"
3. Fill in details
4. Verify email
5. Free tier: 25GB storage
```

### 4.2 Get API Credentials
```
1. Go to Dashboard
2. Copy:
   - Cloud Name
   - API Key
   - API Secret
3. Save in safe place
```

### 4.3 Create Upload Preset
```
1. Go to Settings → Upload
2. Click "Add upload preset"
3. Name: "lee-hydraulics"
4. Unsigned: Yes
5. Save
```

---

## ✅ STEP 5: ADMIN PANEL DEPLOYMENT

### 5.1 Create Admin React App
```bash
# In your project directory
mkdir admin
cd admin
npx create-react-app .
```

### 5.2 Install Dependencies
```bash
npm install @supabase/supabase-js react-router-dom
```

### 5.3 Create .env.local
```
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_KEY=your-anon-key
REACT_APP_CLOUDINARY_NAME=your-cloud-name
```

### 5.4 Deploy to Vercel
```bash
# From admin directory
npm install -g vercel
vercel
```

---

## ✅ STEP 6: CONNECT CONTACT FORM

### 6.1 Update index.html
```html
<!-- Add this to your contact form -->
<form id="contactForm">
  <input type="text" name="name" placeholder="Your Name" required>
  <input type="email" name="email" placeholder="Your Email" required>
  <input type="tel" name="phone" placeholder="Phone (optional)">
  <input type="text" name="company" placeholder="Company (optional)">
  <textarea name="message" placeholder="Your Message" required></textarea>
  <button type="submit">Send Message</button>
</form>

<script>
document.getElementById('contactForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData);
  
  try {
    const response = await fetch('https://your-vercel-app.vercel.app/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      alert('Thank you! We will contact you soon.');
      e.target.reset();
    } else {
      alert('Error: ' + result.error);
    }
  } catch (error) {
    alert('Error submitting form: ' + error.message);
  }
});
</script>
```

---

## ✅ STEP 7: GITHUB PAGES SETUP

### 7.1 Enable GitHub Pages
```
1. Go to GitHub repository
2. Settings → Pages
3. Source: Deploy from branch
4. Branch: main
5. Folder: / (root)
6. Click "Save"
```

### 7.2 Connect Custom Domain
```
1. In GitHub Pages settings:
   - Custom domain: www.leehyd.com
   - Click "Save"
   - Check "Enforce HTTPS"

2. In your domain registrar (GoDaddy, Namecheap, etc.):
   - Go to DNS settings
   - Add A records:
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
   - Add CNAME: www → your-username.github.io
   - Wait 24-48 hours for propagation
```

---

## ✅ STEP 8: TEST EVERYTHING

### 8.1 Test Contact Form
```
1. Go to https://www.leehyd.com
2. Fill contact form
3. Submit
4. Check:
   - Email received in inbox
   - Lead appears in admin panel
   - Status is "new"
```

### 8.2 Test Admin Panel
```
1. Go to https://admin.leehyd.com
2. Login with admin credentials
3. Check:
   - Dashboard shows stats
   - Leads table populated
   - Can update lead status
   - Can create blog post
```

### 8.3 Test Blog
```
1. Create blog post in admin
2. Publish it
3. Go to https://www.leehyd.com/blog
4. Verify post appears
5. Click post and verify content
```

---

## 📊 MONITORING & MAINTENANCE

### Weekly Tasks
- [ ] Check new leads in admin panel
- [ ] Respond to inquiries
- [ ] Monitor email delivery

### Monthly Tasks
- [ ] Review analytics
- [ ] Check free tier usage
- [ ] Publish new blog post
- [ ] Update team/testimonials

### Quarterly Tasks
- [ ] Review and archive old leads
- [ ] Optimize images
- [ ] Update certifications/awards

---

## 🚨 TROUBLESHOOTING

### Contact Form Not Submitting
```
1. Check browser console for errors
2. Verify Vercel API URL is correct
3. Check CORS headers in api/leads.js
4. Verify Supabase credentials
```

### Emails Not Sending
```
1. Check SendGrid API key
2. Verify sender email is verified
3. Check spam folder
4. Review SendGrid logs
```

### Admin Panel Not Loading
```
1. Check Vercel deployment status
2. Verify environment variables
3. Check browser console
4. Clear cache and reload
```

### Database Connection Error
```
1. Verify Supabase URL and key
2. Check database is running
3. Verify network connectivity
4. Check Supabase status page
```

---

## 💰 COST SUMMARY

| Service | Free Tier | Cost |
|---------|-----------|------|
| GitHub Pages | Unlimited | ₹0 |
| Vercel Functions | 100GB/month | ₹0 |
| Supabase DB | 500MB | ₹0 |
| SendGrid Email | 100/day | ₹0 |
| Cloudinary Images | 25GB | ₹0 |
| Domain | - | ₹200-500/year |
| **TOTAL** | - | **₹0/month** |

---

## 📞 SUPPORT RESOURCES

- **Supabase Docs:** https://supabase.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **SendGrid Docs:** https://docs.sendgrid.com
- **Cloudinary Docs:** https://cloudinary.com/documentation
- **GitHub Pages:** https://pages.github.com

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Supabase account created
- [ ] Database tables created
- [ ] SendGrid account created
- [ ] API key verified
- [ ] Vercel account created
- [ ] Repository imported
- [ ] Environment variables added
- [ ] API functions deployed
- [ ] Admin panel deployed
- [ ] Contact form connected
- [ ] GitHub Pages enabled
- [ ] Custom domain connected
- [ ] All tests passed
- [ ] Monitoring setup

---

**You're all set! Your website is now live with a complete backend system - all for FREE! 🎉**

---

## 🎓 NEXT STEPS

1. **Customize admin panel** - Add your branding
2. **Create first blog post** - Test the system
3. **Share with team** - Get feedback
4. **Monitor usage** - Track free tier limits
5. **Plan upgrades** - When you need more capacity

---

**Questions? Check the troubleshooting section or contact support for each service.**
