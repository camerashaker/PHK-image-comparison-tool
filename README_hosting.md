# 🚀 Image Comparison Tool - Web Hosting Guide

## 📁 Files for Web Deployment

- `web_app.py` - Main web application (simplified, upload-based)
- `web_requirements.txt` - Dependencies for web hosting
- `README_hosting.md` - This file with hosting instructions

## 🌐 Best Hosting Options

### 1. 🆓 **Streamlit Cloud (Recommended - FREE)**

**Steps:**
1. Push these files to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your repository
5. Point to `web_app.py` as the main file

**Pros:**
- ✅ **Completely free**
- ✅ **Built for Streamlit** 
- ✅ **Auto-deploys from GitHub**
- ✅ **No server management**

**Limits:**
- 1GB RAM, 1 CPU core
- Good for moderate usage

### 2. 🚀 **Railway (Very Easy)**

**Steps:**
1. Push to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect GitHub and deploy
4. Set start command: `streamlit run web_app.py --server.port $PORT`

**Pros:**
- ✅ **Simple deployment**
- ✅ **Generous free tier**
- ✅ **Good performance**

### 3. 🔧 **Heroku (Popular)**

**Additional files needed:**
- `Procfile`: `web: streamlit run web_app.py --server.port=$PORT --server.address=0.0.0.0`
- `runtime.txt`: `python-3.11.0`

## 📦 Quick Deployment Setup

### For Streamlit Cloud:
```bash
# 1. Create GitHub repo
git init
git add web_app.py web_requirements.txt README_hosting.md
git commit -m "Initial web app"
git remote add origin https://github.com/yourusername/image-comparison-tool
git push -u origin main

# 2. Go to share.streamlit.io and deploy!
```

### For Railway:
```bash
# Same as above, then:
# 1. Go to railway.app
# 2. "Deploy from GitHub"
# 3. Select your repo
# 4. It will auto-detect Streamlit!
```

## 🔧 Key Differences from Local Version

**Web Version (`web_app.py`):**
- ✅ **File uploads** instead of local directories
- ✅ **Simplified UI** for better web performance
- ✅ **No heavy dependencies** (removed opencv, scikit-image)
- ✅ **Limited to 5 comparisons** for performance
- ✅ **Ultra-fast perceptual hashing** only

**Local Version (`image_comparison_tool.py`):**
- 🏠 **Local file access**
- 🔍 **Multiple comparison algorithms**
- 📊 **Unlimited comparisons**
- 💾 **Full feature set**

## 🎯 Features in Web Version

- **📤 Drag & drop file uploads**
- **🔍 Automatic image matching** using perceptual hashing
- **🏆 Side-by-side comparisons** with rating system
- **📊 Live results summary**
- **⚡ Fast performance** optimized for web

## 🚀 Go Live in 5 Minutes!

1. **Copy files** to new folder
2. **Push to GitHub** 
3. **Go to share.streamlit.io**
4. **Click "Deploy"**
5. **Share your URL!** 🎉

Your web app will be live at: `https://yourappname.streamlit.app`

## 💡 Pro Tips

- **Keep image files under 5MB** each for best performance
- **Use JPEG format** when possible (smaller file sizes)
- **Limit to 10-20 images** per upload session
- **Test locally first:** `streamlit run web_app.py` 