import streamlit as st
import os
from PIL import Image
import tempfile
import zipfile

st.set_page_config(page_title="Image Comparison Tool - Web Version", layout="wide")

# Initialize session state
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}

def save_uploaded_files(uploaded_files, category):
    """Save uploaded files to temporary directory"""
    if not uploaded_files:
        return {}
    
    temp_dir = tempfile.mkdtemp(prefix=f"{category}_")
    file_mapping = {}
    
    for uploaded_file in uploaded_files:
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_mapping[uploaded_file.name] = temp_path
    
    return file_mapping

def calculate_perceptual_hash_similarity(img1, img2):
    """Compare images using perceptual hashing"""
    try:
        def get_hash(img):
            img_small = img.convert('L').resize((8, 8), Image.Resampling.LANCZOS)
            pixels = list(img_small.getdata())
            avg = sum(pixels) / len(pixels)
            return ''.join(['1' if pixel > avg else '0' for pixel in pixels])
        
        hash1 = get_hash(img1)
        hash2 = get_hash(img2)
        
        diff_bits = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
        return 1.0 - (diff_bits / 64.0)
        
    except Exception:
        return 0.0

def find_best_match(original_path, target_images, threshold=0.3):
    """Find best matching image"""
    if not original_path or not os.path.exists(original_path):
        return None, 0.0
    
    best_match = None
    best_score = 0.0
    
    original_img = Image.open(original_path)
    
    for filename, path in target_images.items():
        if not os.path.exists(path):
            continue
            
        target_img = Image.open(path)
        score = calculate_perceptual_hash_similarity(original_img, target_img)
        
        if score > best_score and score > threshold:
            best_score = score
            best_match = (filename, path)
    
    return best_match, best_score

def main():
    st.title("📸 Image Comparison Tool - Web Version")
    st.write("Upload and compare images automatically using AI matching")
    
    # File upload sections
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### 📸 Original Images")
        original_uploads = st.file_uploader(
            "Upload original images",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="original"
        )
        
        original_images = {}
        if original_uploads:
            original_images = save_uploaded_files(original_uploads, "original")
            st.success(f"✅ {len(original_images)} uploaded")
    
    with col2:
        st.write("### 🔧 Your Processed Images")
        processed_uploads = st.file_uploader(
            "Upload your processed results",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="processed"
        )
        
        processed_images = {}
        if processed_uploads:
            processed_images = save_uploaded_files(processed_uploads, "processed")
            st.success(f"✅ {len(processed_images)} uploaded")
    
    with col3:
        st.write("### 📱 PhotoMyne Images")
        photomyne_uploads = st.file_uploader(
            "Upload PhotoMyne results",
            type=['jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            key="photomyne"
        )
        
        photomyne_images = {}
        if photomyne_uploads:
            photomyne_images = save_uploaded_files(photomyne_uploads, "photomyne")
            st.success(f"✅ {len(photomyne_images)} uploaded")
    
    # Only proceed if we have images
    if not original_images:
        st.warning("📤 Please upload some original images to start!")
        return
    
    st.write("---")
    st.write("## 🔍 Image Comparisons")
    
    # Show comparisons
    max_comparisons = min(len(original_images), 5)  # Limit for web performance
    
    for i, (orig_filename, orig_path) in enumerate(list(original_images.items())[:max_comparisons]):
        st.write(f"### Comparison {i+1}: {orig_filename}")
        
        # Find matches
        processed_match, proc_score = find_best_match(orig_path, processed_images)
        photomyne_match, photo_score = find_best_match(orig_path, photomyne_images)
        
        # Display images
        display_cols = []
        display_cols.append(("📸 Original", orig_path))
        
        if processed_match:
            display_cols.append((f"🔧 Processed (similarity: {proc_score:.1%})", processed_match[1]))
        
        if photomyne_match:
            display_cols.append((f"📱 PhotoMyne (similarity: {photo_score:.1%})", photomyne_match[1]))
        
        if len(display_cols) > 1:
            cols = st.columns(len(display_cols))
            
            for idx, (title, image_path) in enumerate(display_cols):
                with cols[idx]:
                    st.write(f"**{title}**")
                    img = Image.open(image_path)
                    st.image(img, use_container_width=True)
            
            # Rating section
            if len(display_cols) >= 2:
                rating_options = ["Original"]
                if processed_match:
                    rating_options.append("Your Processed")
                if photomyne_match:
                    rating_options.append("PhotoMyne")
                
                rating_key = f"rating_{i}"
                selected = st.radio(
                    "🏆 Which looks best?",
                    rating_options,
                    key=rating_key,
                    horizontal=True
                )
                st.session_state.ratings[rating_key] = selected
        else:
            st.write("📸 Original image only - upload processed/PhotoMyne images for comparison")
            img = Image.open(orig_path)
            st.image(img, width=300)
        
        st.write("---")
    
    # Show summary if we have ratings
    if st.session_state.ratings:
        st.write("## 📊 Results Summary")
        
        ratings = list(st.session_state.ratings.values())
        original_wins = ratings.count("Original")
        processed_wins = ratings.count("Your Processed")
        photomyne_wins = ratings.count("PhotoMyne")
        total = len(ratings)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📸 Original Wins", f"{original_wins}/{total}")
        with col2:
            st.metric("🔧 Your Processed Wins", f"{processed_wins}/{total}")
        with col3:
            st.metric("📱 PhotoMyne Wins", f"{photomyne_wins}/{total}")
        
        # Declare winner
        if processed_wins > photomyne_wins and processed_wins > original_wins:
            st.success("🏆 **Your Processing Pipeline is winning!**")
        elif photomyne_wins > processed_wins and photomyne_wins > original_wins:
            st.info("📱 **PhotoMyne is leading**")
        else:
            st.warning("📸 **Original images preferred**")

if __name__ == "__main__":
    main() 