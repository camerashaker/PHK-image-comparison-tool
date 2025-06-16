import streamlit as st
import os
from PIL import Image
import tempfile
import zipfile
from datetime import datetime

st.set_page_config(page_title="PHK Image Comparison Tool - Data Collection", layout="wide")

# Initialize session state
if 'ratings' not in st.session_state:
    st.session_state.ratings = {}
if 'comparison_session' not in st.session_state:
    st.session_state.comparison_session = datetime.now().strftime("%Y%m%d_%H%M%S")

def load_images_from_directory(directory_path):
    """Load all images from a directory"""
    if not os.path.exists(directory_path):
        return {}
    
    images = {}
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    
    for filename in os.listdir(directory_path):
        if any(filename.lower().endswith(ext) for ext in valid_extensions):
            images[filename] = os.path.join(directory_path, filename)
    
    return images

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

def extract_base_name(filename):
    """Extract base name from filename for matching"""
    base = os.path.splitext(filename)[0]
    
    # For processed files, remove the processing suffix
    if '_photo_restoration' in base or '_hybrid_final' in base or '_flux_' in base:
        parts = base.split('_')
        processing_keywords = ['photo', 'restoration', 'color', 'correction', 'flux', 'hybrid', 'final']
        for i, part in enumerate(parts):
            if part in processing_keywords:
                base = '_'.join(parts[:i])
                break
    
    return base

def find_matching_files(original_images, processed_images, photomyne_images):
    """Find matching files using visual similarity"""
    matches = []
    
    original_map = {extract_base_name(f): (f, path) for f, path in original_images.items()}
    processed_map = {}
    
    # Look for final processed images
    for filename, path in processed_images.items():
        if '_hybrid_final.png' in filename or '_final' in filename.lower() or len(processed_images) < 10:
            base_name = extract_base_name(filename)
            processed_map[base_name] = (filename, path)
    
    for base_name, (orig_file, orig_path) in original_map.items():
        processed_info = processed_map.get(base_name, (None, None))
        
        # Find best PhotoMyne match
        photomyne_match, similarity_score = find_best_match(orig_path, photomyne_images)
        
        match_data = {
            'base_name': base_name,
            'original_file': orig_file,
            'original_path': orig_path,
            'processed_file': processed_info[0],
            'processed_path': processed_info[1],
            'photomyne_file': photomyne_match[0] if photomyne_match else None,
            'photomyne_path': photomyne_match[1] if photomyne_match else None,
            'photomyne_similarity': similarity_score
        }
        matches.append(match_data)
    
    return matches

def save_ratings_to_csv():
    """Save ratings data for collection"""
    if not st.session_state.ratings:
        return None
    
    import pandas as pd
    
    # Prepare rating data
    rating_data = []
    for key, value in st.session_state.ratings.items():
        if not key.endswith('_comment'):
            image_name = key.replace('rating_', '').split('_')[0]
            comment_key = f"{key}_comment"
            comment = st.session_state.ratings.get(comment_key, "")
            
            rating_data.append({
                "session_id": st.session_state.comparison_session,
                "timestamp": datetime.now().isoformat(),
                "image_name": image_name,
                "preferred": value,
                "comment": comment
            })
    
    if rating_data:
        df = pd.DataFrame(rating_data)
        csv_data = df.to_csv(index=False)
        return csv_data
    
    return None

def main():
    st.title("📸 PHK Image Comparison Tool - Data Collection")
    st.write("**Help evaluate photo restoration quality!** Compare original vs AI-processed vs PhotoMyne results")
    
    # Mode selection
    st.write("## 🎯 **Choose Comparison Mode**")
    mode = st.radio(
        "Select how you want to compare images:",
        ["🔬 **Pre-loaded Dataset (Recommended for Data Collection)**", "📤 **Upload Your Own Images**"],
        help="Pre-loaded dataset allows immediate comparison of our test images"
    )
    
    original_images = {}
    processed_images = {}
    photomyne_images = {}
    
    if "Pre-loaded Dataset" in mode:
        st.write("### 📊 **Loading Pre-configured Image Sets...**")
        
        # Define image directories (these would be included in the repo)
        image_dirs = {
            "original": "./images/original/",
            "processed": "./images/processed/", 
            "photomyne": "./images/photomyne/"
        }
        
        # Try to load from local directories first
        with st.spinner("Loading image datasets..."):
            original_images = load_images_from_directory(image_dirs["original"])
            processed_images = load_images_from_directory(image_dirs["processed"])
            photomyne_images = load_images_from_directory(image_dirs["photomyne"])
        
        # Display successful loading message with counts
        if any([original_images, processed_images, photomyne_images]):
            st.success(f"✅ **Dataset loaded successfully!**")
            st.info(f"📊 **Loaded:** {len(original_images)} originals • {len(processed_images)} AI processed • {len(photomyne_images)} PhotoMyne")
        else:
            # If no images found, show helpful message
            st.warning("🚧 **Pre-loaded images not found.** This happens in web deployment. Please use upload mode or run locally.")
            st.info("💡 **For full functionality:** Clone the repo and run locally with `streamlit run web_app_preloaded.py`")
            
            # Fall back to upload mode
            st.write("---")
            st.write("### 📤 **Upload Mode (Fallback)**")
            mode = "Upload Your Own Images"
    
    if "Upload Your Own Images" in mode or not any([original_images, processed_images, photomyne_images]):
        st.write("### 📁 **Upload Images for Comparison**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("#### 📸 Original Images")
            original_uploads = st.file_uploader(
                "Upload original photos",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                key="original",
                help="Upload the unprocessed original photos"
            )
            if original_uploads:
                original_images = save_uploaded_files(original_uploads, "original")
                st.success(f"✅ {len(original_images)} original images uploaded")
        
        with col2:
            st.write("#### 🔧 Your AI Processed")
            processed_uploads = st.file_uploader(
                "Upload AI-processed results",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                key="processed",
                help="Upload images processed by your AI pipeline"
            )
            if processed_uploads:
                processed_images = save_uploaded_files(processed_uploads, "processed")
                st.success(f"✅ {len(processed_images)} processed images uploaded")
        
        with col3:
            st.write("#### 📱 PhotoMyne Results")
            photomyne_uploads = st.file_uploader(
                "Upload PhotoMyne results",
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True,
                key="photomyne",
                help="Upload the same photos processed by PhotoMyne"
            )
            if photomyne_uploads:
                photomyne_images = save_uploaded_files(photomyne_uploads, "photomyne")
                st.success(f"✅ {len(photomyne_images)} PhotoMyne images uploaded")
    
    # Only proceed if we have images
    if not original_images:
        st.warning("📤 Please upload some original images to start the comparison!")
        return
    
    # Display image counts
    st.sidebar.write("**📊 Image Counts**")
    st.sidebar.write(f"📸 Original: {len(original_images)}")
    st.sidebar.write(f"🔧 AI Processed: {len(processed_images)}")
    st.sidebar.write(f"📱 PhotoMyne: {len(photomyne_images)}")
    
    st.write("---")
    st.write("## 🔍 **Image Comparisons**")
    
    # Find matches automatically
    with st.spinner("🤖 Finding matching images using AI similarity detection..."):
        matches = find_matching_files(original_images, processed_images, photomyne_images)
    
    # Filter to matches that have at least 2 versions
    valid_matches = []
    for match in matches:
        available_versions = 1  # Original always available
        if match['processed_path']: available_versions += 1
        if match['photomyne_path']: available_versions += 1
        
        if available_versions >= 2:
            valid_matches.append(match)
    
    if not valid_matches:
        st.error("❌ No matching image sets found. Make sure your images have similar names or content.")
        return
    
    # Limit for performance
    max_comparisons = min(len(valid_matches), 10)
    valid_matches = valid_matches[:max_comparisons]
    
    st.success(f"🎯 Found {len(valid_matches)} image sets ready for comparison!")
    
    # Comparison interface
    for i, match in enumerate(valid_matches):
        st.write(f"### 🖼️ **Comparison {i+1}: {match['base_name']}**")
        
        if match['photomyne_path'] and match.get('photomyne_similarity', 0) > 0:
            similarity_pct = match['photomyne_similarity'] * 100
            st.write(f"*PhotoMyne match confidence: {similarity_pct:.1f}%*")
        
        # Build display columns
        display_cols = []
        display_cols.append(("📸 Original", match['original_path']))
        
        if match['processed_path']:
            display_cols.append(("🔧 AI Processed", match['processed_path']))
        
        if match['photomyne_path']:
            display_cols.append(("📱 PhotoMyne", match['photomyne_path']))
        
        # Display images side by side
        if len(display_cols) >= 2:
            cols = st.columns(len(display_cols))
            
            for idx, (title, image_path) in enumerate(display_cols):
                with cols[idx]:
                    st.write(f"**{title}**")
                    img = Image.open(image_path)
                    st.image(img, use_container_width=True)
                    
                    # Show image info
                    width, height = img.size
                    file_size = os.path.getsize(image_path) / (1024 * 1024)
                    st.write(f"📏 {width}x{height} | 💾 {file_size:.1f}MB")
            
            # Rating section
            st.write("#### 🏆 **Which image looks best overall?**")
            
            rating_options = ["Original"]
            if match['processed_path']:
                rating_options.append("AI Processed")
            if match['photomyne_path']:
                rating_options.append("PhotoMyne")
            
            rating_key = f"rating_{match['base_name']}_{i}"
            current_rating = st.session_state.ratings.get(rating_key, None)
            
            # Voting interface
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected = st.radio(
                    "Select the best image:",
                    rating_options,
                    index=rating_options.index(current_rating) if current_rating in rating_options else 0,
                    key=rating_key,
                    horizontal=True
                )
                st.session_state.ratings[rating_key] = selected
            
            with col2:
                # Quick feedback
                feedback_key = f"feedback_{match['base_name']}_{i}"
                feedback = st.selectbox(
                    "Why?",
                    ["", "Better color", "More detail", "Less artifacts", "More natural", "Other"],
                    key=feedback_key
                )
                if feedback:
                    st.session_state.ratings[f"{rating_key}_comment"] = feedback
        
        st.write("---")
    
    # Results summary
    if st.session_state.ratings:
        st.write("## 📊 **Your Rating Summary**")
        
        rating_data = {k: v for k, v in st.session_state.ratings.items() if not k.endswith('_comment')}
        
        if rating_data:
            original_wins = sum(1 for r in rating_data.values() if r == "Original")
            processed_wins = sum(1 for r in rating_data.values() if r == "AI Processed")
            photomyne_wins = sum(1 for r in rating_data.values() if r == "PhotoMyne")
            total = len(rating_data)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📸 Original Preferred", f"{original_wins}/{total}")
            with col2:
                st.metric("🔧 AI Processed Preferred", f"{processed_wins}/{total}")
            with col3:
                st.metric("📱 PhotoMyne Preferred", f"{photomyne_wins}/{total}")
            
            # Winner announcement
            if processed_wins > photomyne_wins and processed_wins > original_wins:
                st.success("🏆 **AI Processing Pipeline Wins!**")
            elif photomyne_wins > processed_wins and photomyne_wins > original_wins:
                st.info("📱 **PhotoMyne Leads**")
            else:
                st.warning("📸 **Original Images Often Preferred**")
            
            # Download results
            csv_data = save_ratings_to_csv()
            if csv_data:
                st.download_button(
                    label="📥 Download Your Ratings (CSV)",
                    data=csv_data,
                    file_name=f"image_ratings_{st.session_state.comparison_session}.csv",
                    mime="text/csv",
                    help="Download your comparison results for analysis"
                )
    
    # Footer
    st.write("---")
    st.write("💡 **Thank you for contributing to photo restoration research!**")
    st.write(f"Session ID: `{st.session_state.comparison_session}`")

if __name__ == "__main__":
    main() 
