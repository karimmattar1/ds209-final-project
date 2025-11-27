# Deployment Checklist - Ready for Berkeley iSchool Server

## ✅ Files Ready (34 files total)

### HTML Pages (5)
- [x] index.html
- [x] explore.html
- [x] compare.html
- [x] similar.html
- [x] analysis.html

### Assets
- [x] static/css/style.css
- [x] static/js/app.js
- [x] static/js/explore.js
- [x] static/js/compare.js
- [x] static/js/similar.js

### Data Files
- [x] static/data/metadata.json
- [x] static/data/players_sample.json

### Generated Charts (7 Altair visualizations)
- [x] static/charts/league_scatter.html
- [x] static/charts/league_tackles.html
- [x] static/charts/league_passing.html
- [x] static/charts/top_gk.html
- [x] static/charts/top_df.html
- [x] static/charts/top_mf.html
- [x] static/charts/top_fw.html

### Configuration
- [x] .htaccess (for Apache server)
- [x] README.md
- [x] DEPLOYMENT_GUIDE.md

---

## 🔧 What You Need From Berkeley

### Information Required:
1. **Server hostname:**
   - Likely: `people.ischool.berkeley.edu` or `ischool.berkeley.edu`
   - Ask professor or IT

2. **Your username:**
   - Usually your CalNet ID or Berkeley email prefix
   - Example: `kmattar` or your actual username

3. **Access method:**
   - SFTP credentials (username + password)
   - Or SSH key
   - Port: Usually 22 (default)

---

## 📤 When You Get Access, Run This:

### Option 1: Command Line Upload
```bash
# Replace YOUR_USERNAME with your actual Berkeley username
# Replace SERVER_HOST with actual hostname (e.g., people.ischool.berkeley.edu)

cd /Users/karimmattar11/Desktop/Berkeley/209_Final_Project

# Upload everything
scp -r 06_Website/* YOUR_USERNAME@SERVER_HOST:~/public_html/football-scout/

# Example:
# scp -r 06_Website/* kmattar@people.ischool.berkeley.edu:~/public_html/football-scout/
```

### Option 2: FileZilla (GUI)
1. Download FileZilla: https://filezilla-project.org/
2. Connect with:
   - Host: sftp://SERVER_HOST
   - Username: YOUR_USERNAME
   - Password: YOUR_PASSWORD
   - Port: 22
3. Navigate to `public_html/` or `www/` directory
4. Create folder: `football-scout`
5. Upload all files from `06_Website/` into that folder

---

## 🌐 Your Final URL Will Be:

Probably one of these:
- `https://people.ischool.berkeley.edu/~YOUR_USERNAME/football-scout/`
- `https://apps-fall.ischool.berkeley.edu/football-scout/`
- `https://groups.ischool.berkeley.edu/football-scout/`

(Exact format depends on how Berkeley structures it)

---

## ✉️ Email Templates Ready to Send:

### To Professor Kwon:
```
Subject: DS209 - Berkeley Server Access for Final Project

Hi Professor Kwon,

I've completed my Football Scout Tool using Altair (all requirements met):
✓ Football (soccer) clarified - not fantasy football
✓ Kaggle dataset link included
✓ Using Altair as primary visualization tool
✓ Website ready to deploy

I need the Berkeley iSchool server details to deploy. Could you provide:
- Server hostname
- My login credentials
- SFTP/SSH access instructions

The site is built and tested locally - ready to upload as soon as I have access.

Thank you!
Karim Mattar
```

### To iSchool IT:
```
Subject: MIDS Student Web Hosting - DS209 Final Project

Hello,

I'm a MIDS student (Karim Mattar) in DS209 and need web hosting for my
final project visualization tool.

Could you please provide:
1. Server hostname for student web hosting
2. My account credentials or activation link
3. SFTP/SSH access information

This is for my final project due in Week 14.

Thank you!
Karim Mattar
```

---

## 🎯 Next Steps

1. **TODAY:** Email professor or IT (use templates above)
2. **Wait for server info** (usually 1-2 business days)
3. **Once you get credentials:** Upload using command or FileZilla
4. **Test deployment:** Visit your URL and verify all features work
5. **Share URL:** Use for usability testing

---

## 📋 Post-Deployment Verification

Once deployed, check:
- [ ] All 5 pages load correctly
- [ ] Navigation works
- [ ] Altair charts render (not blank iframes)
- [ ] JavaScript features work (filters, comparisons)
- [ ] Data loads (no console errors)
- [ ] Works on mobile/tablet
- [ ] Works in different browsers (Chrome, Firefox, Safari)

---

## 🆘 If You Get Stuck

**IT Support:** ischool-help@berkeley.edu
**Professor:** Use office hours or email
**Classmates:** Ask if anyone has deployed yet

Your site is 100% ready - you just need the server access!
