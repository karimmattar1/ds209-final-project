# Deployment Guide - Football Scout Tool

## Deploying to Berkeley iSchool Server

### Prerequisites
- Access to Berkeley iSchool server
- FTP/SFTP client (FileZilla, Cyberduck, or command-line `scp`)
- Your Berkeley credentials

---

## Step 1: Prepare Files for Deployment

All necessary files are already generated in the `06_Website/` directory:

✓ HTML pages (index.html, explore.html, compare.html, similar.html, analysis.html)
✓ CSS stylesheet (static/css/style.css)
✓ JavaScript files (static/js/*.js)
✓ Generated Altair charts (static/charts/*.html)
✓ Processed data files (static/data/*.json)

---

## Step 2: Upload Files

### Option A: Using FileZilla or Cyberduck

1. Connect to Berkeley iSchool server:
   - Host: `ischool.berkeley.edu` (or specific host provided)
   - Protocol: SFTP
   - Username: Your Berkeley username
   - Password: Your Berkeley password

2. Navigate to your public_html or designated web directory

3. Upload the entire `06_Website/` folder contents:
   ```
   /your-web-directory/
   ├── index.html
   ├── explore.html
   ├── compare.html
   ├── similar.html
   ├── analysis.html
   └── static/
       ├── css/
       ├── js/
       ├── charts/
       └── data/
   ```

4. Ensure file permissions are set correctly:
   - HTML files: 644
   - Directories: 755

### Option B: Using Command Line (scp)

```bash
# From your local machine, navigate to project directory
cd /Users/karimmattar11/Desktop/Berkeley/209_Final_Project

# Upload entire website directory
scp -r 06_Website/* your_username@ischool.berkeley.edu:~/public_html/

# Or to a specific directory
scp -r 06_Website/* your_username@ischool.berkeley.edu:~/public_html/football-scout/
```

---

## Step 3: Verify Deployment

1. Open your web browser

2. Navigate to your Berkeley URL:
   ```
   https://people.ischool.berkeley.edu/~your_username/
   # or
   https://people.ischool.berkeley.edu/~your_username/football-scout/
   ```

3. Test all pages:
   - [ ] Home page loads with statistics
   - [ ] Explorer page shows interactive scatter plot
   - [ ] Compare page shows player search
   - [ ] Similar players page works
   - [ ] Analysis page displays charts in iframes

---

## Step 4: Troubleshooting

### Charts Not Loading
- Check that `static/charts/` directory uploaded completely
- Verify file paths are relative (not absolute)
- Check browser console for errors (F12 → Console)

### Data Not Loading
- Ensure `static/data/metadata.json` and `players_sample.json` are uploaded
- Check CORS headers (should be fine with same-origin)
- Verify JSON files are valid

### Styling Issues
- Confirm `static/css/style.css` uploaded successfully
- Check browser cache (hard refresh with Cmd+Shift+R or Ctrl+F5)

### JavaScript Errors
- Open browser console (F12) to see specific errors
- Verify all `.js` files in `static/js/` uploaded
- Check that Vega/Vega-Lite CDN links are accessible

---

## Step 5: Testing Checklist

After deployment, verify:

- [ ] Navigation menu works on all pages
- [ ] Altair charts render correctly
- [ ] Interactive features work (tooltips, filters, dropdowns)
- [ ] Charts can be exported
- [ ] Page loads quickly (< 3 seconds)
- [ ] Responsive design works on mobile
- [ ] All links work (no 404 errors)

---

## File Size Optimization (Optional)

If you need to reduce file size:

1. **Reduce data sample:**
   ```python
   # In generate_charts.py, reduce sample size
   df_export = df.head(200)  # Instead of 500
   ```

2. **Compress charts:**
   - Remove unused chart files
   - Use Vega-Lite JSON specs instead of full HTML

3. **Optimize images:**
   - If you add images later, use compressed formats

---

## Maintenance

### Updating Data

To update with new season data:

1. Download new CSV from Kaggle
2. Replace `data/players_data_light-2024_2025.csv`
3. Run `python3 generate_charts.py`
4. Re-upload `static/charts/` and `static/data/` directories

### Adding New Features

1. Edit HTML pages to add new sections
2. Create new visualization functions in `modules/visualizations.py`
3. Generate charts with `generate_charts.py`
4. Add JavaScript if needed
5. Test locally with `python3 run_server.py`
6. Upload modified files

---

## Security Considerations

- No sensitive data is included (all public FBref statistics)
- No server-side processing required
- No user input stored (all client-side)
- Uses HTTPS by default on Berkeley servers

---

## URLs and Links

Your deployed site will be accessible at:

**Primary URL:**
```
https://people.ischool.berkeley.edu/~your_username/
```

**Alternative (if in subfolder):**
```
https://people.ischool.berkeley.edu/~your_username/football-scout/
```

Update README.md and proposal with your actual deployment URL before final submission!

---

## For Usability Testing

When recruiting participants:

1. Share the deployed URL (not localhost)
2. Test on different devices (desktop, tablet, mobile)
3. Test on different browsers (Chrome, Firefox, Safari)
4. Record screen during testing
5. Take notes on any issues participants encounter

---

## Support

For Berkeley iSchool server issues:
- Contact: ischool-help@berkeley.edu
- Documentation: https://www.ischool.berkeley.edu/intranet/technology

For project-specific issues:
- Refer to README.md
- Check browser console for errors
- Verify all files uploaded correctly

---

## Final Checklist Before Presentation

- [ ] All pages deployed and accessible
- [ ] URL works on different devices
- [ ] Charts render correctly
- [ ] No console errors
- [ ] Responsive design working
- [ ] Add deployment URL to presentation slides
- [ ] Create 2-3 minute video demo
- [ ] Test with different browsers
- [ ] Screenshot key features for presentation

---

## Success! 🎉

Your Football Scout Tool is now live and ready for:
- Usability testing
- Final presentation
- Demonstration to class

Remember to update your proposal and final report with the live URL!
