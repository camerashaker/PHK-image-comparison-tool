# 📸 PHK Image Comparison Tool

**AI-powered image comparison tool for evaluating photo restoration results**

Compare original photos vs your AI processing pipeline vs PhotoMyne results using advanced computer vision matching and user voting.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://phk-image-comparison.streamlit.app)

## 🎯 **Overview**

This tool helps evaluate the quality of photo restoration pipelines by:
- **🔍 Automatically matching images** across different sources using perceptual hashing
- **🏆 Side-by-side comparisons** with voting system
- **📊 Statistical analysis** of preferences and results
- **⚡ Fast visual similarity algorithms** for efficient processing

## ✨ **Features**

### **🌐 Web Version** (`web_app.py`)
- **📤 Drag & drop file uploads** - No local setup required
- **🔍 AI-powered automatic matching** using perceptual hashing
- **🏆 Interactive comparison interface** with voting
- **📊 Live results dashboard** with statistics
- **⚡ Optimized for web performance** (limited to 5 comparisons)

### **🖥️ Local Version** (`image_comparison_tool.py`)
- **📁 Local directory access** for large image sets
- **🔬 Multiple comparison algorithms** (hash, thumbnail, sampling, grid, full SSIM)
- **📊 Unlimited comparisons** with advanced filtering
- **💾 Export ratings** to JSON files
- **🎛️ Fine-tuned controls** for power users

## 🚀 **Quick Start**

### **Web Version (Recommended)**
1. **Visit:** [phk-image-comparison.streamlit.app](https://phk-image-comparison.streamlit.app)
2. **Upload images:** Drag & drop your original, processed, and PhotoMyne images
3. **Compare & vote:** Rate which images look best
4. **View results:** See live statistics and winner

### **Local Development**
```bash
# Clone repository
git clone https://github.com/camerashaker/PHK-image-comparison-tool.git
cd PHK-image-comparison-tool

# Install dependencies
pip install -r web_requirements.txt

# Run web version
streamlit run web_app.py

# OR run full local version (requires additional dependencies)
pip install -r requirements_image_comparison.txt
streamlit run image_comparison_tool.py
```

## 📁 **File Structure**

```
PHK-image-comparison-tool/
├── web_app.py                     # 🌐 Web version - simplified, upload-based
├── image_comparison_tool.py       # 🖥️ Local version - full featured
├── image_comparison_tool_web.py   # 🔧 Web version - extended (alternative)
├── web_requirements.txt           # 📦 Minimal dependencies for web
├── requirements_image_comparison.txt # 📦 Full dependencies for local
├── Procfile                       # 🚀 Heroku deployment config
├── README_hosting.md              # 📚 Detailed hosting guide
└── README.md                      # 📖 This file
```

## 🔧 **How It Works**

### **1. Image Matching**
- **Perceptual Hashing:** Converts images to 8x8 grayscale fingerprints
- **Visual Similarity:** Compares structural patterns, not just filenames
- **Smart Filtering:** Handles different naming conventions automatically

### **2. Comparison Algorithms**
- **🚀 Perceptual Hash:** Ultra-fast, 64-bit image fingerprints
- **⚡ Thumbnail:** 32x32 normalized correlation
- **🏃 Pixel Sampling:** Every Nth pixel analysis
- **🔍 Grid Regions:** 4x4 regional comparisons
- **🎯 Full SSIM:** Complete structural similarity (local only)

### **3. Rating System**
- **Interactive voting** on side-by-side comparisons
- **Live statistics** with percentage breakdowns
- **Comment system** for detailed feedback
- **Export capabilities** for further analysis

## 🌐 **Deployment Options**

### **1. Streamlit Cloud (FREE & Recommended)**
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your GitHub repo
4. **Live in 5 minutes!** 🎉

### **2. Heroku**
```bash
# Using included Procfile
git push heroku main-bucket
```

### **3. Railway**
- Auto-detects Streamlit
- Deploy directly from GitHub

### **4. Local Development**
```bash
streamlit run web_app.py
# Runs on http://localhost:8501
```

## 🔬 **Technical Details**

### **Image Processing**
- **Supported formats:** JPG, PNG, WEBP, TIFF, BMP
- **Similarity threshold:** Adjustable (default: 30%)
- **Performance:** ~100x faster than full pixel analysis
- **Memory efficient:** Uses temporary file handling

### **Matching Logic**
```python
# Example similarity calculation
def calculate_perceptual_hash_similarity(img1, img2):
    # Convert to 8x8 grayscale
    # Generate binary hash
    # Compare bit differences
    # Return similarity score (0-1)
```

## 📊 **Use Cases**

- **📷 Photo Restoration Evaluation:** Compare AI enhancement vs commercial tools
- **🤖 Algorithm Testing:** A/B test different processing pipelines
- **📈 Quality Assessment:** Quantify image improvement effectiveness
- **👥 User Studies:** Gather preference data from multiple users
- **🏆 Competitive Analysis:** Benchmark against PhotoMyne, Remini, etc.

## 🛠️ **Requirements**

### **Web Version (Minimal)**
```
streamlit
pandas
pillow
numpy
```

### **Local Version (Full)**
```
streamlit
pandas
pillow
numpy
opencv-python
scikit-image
```

## 🎯 **Performance Tips**

- **Web Version:** Limit to 10-20 images for best performance
- **File Sizes:** Keep images under 5MB each
- **Format:** Use JPEG when possible for faster uploads
- **Matching:** Perceptual hash is 100x faster than full analysis

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature-name`
3. **Make changes & test**
4. **Submit pull request**

## 📝 **License**

MIT License - feel free to use for commercial or personal projects.

## 📧 **Contact**

- **GitHub:** [@camerashaker](https://github.com/camerashaker)
- **Issues:** [GitHub Issues](https://github.com/camerashaker/PHK-image-comparison-tool/issues)

---

## 🎉 **Try It Now!**

**🌐 Web App:** [phk-image-comparison.streamlit.app](https://phk-image-comparison.streamlit.app)

Upload your images and see which photo restoration approach wins! 🏆
