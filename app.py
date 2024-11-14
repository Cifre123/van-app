import streamlit as st
from PIL import Image
import numpy as np
import cv2
import os
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
from database_functions import add_van, add_image, add_comparison, get_latest_image


IMAGE_DIR = "vans"

def save_image(van_id, image):
    """Saves the image to disk and records it in the database."""
    add_van(van_id)  # Ensure van ID is in the database
    
    van_dir = os.path.join(IMAGE_DIR, van_id)
    os.makedirs(van_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    save_path = os.path.join(van_dir, f"{timestamp}.jpg")
    image.save(save_path)
    
    # Record in the database
    add_image(van_id, save_path)
    return save_path

def compare_images(old_image_path, new_image_path):
    """Compare images and return the image with damages highlighted."""
    old_image = cv2.imread(old_image_path, cv2.IMREAD_GRAYSCALE)
    new_image = cv2.imread(new_image_path, cv2.IMREAD_GRAYSCALE)
    
    if old_image.shape != new_image.shape:
        new_image = cv2.resize(new_image, (old_image.shape[1], old_image.shape[0]))

    score, diff = ssim(old_image, new_image, full=True)
    diff = (diff * 255).astype("uint8")
    _, thresh = cv2.threshold(diff, 128, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_image_colored = cv2.cvtColor(new_image, cv2.COLOR_GRAY2BGR)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(new_image_colored, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    return new_image_colored, score

st.title("Van Damage Detection with Database")

van_id = st.text_input("Enter Van ID")
uploaded_file = st.file_uploader("Upload a new image", type=["jpg", "jpeg", "png"])

if st.button("Save and Compare") and van_id and uploaded_file:
    image = Image.open(uploaded_file)
    saved_image_path = save_image(van_id, image)
    
    old_image_path = get_latest_image(van_id)
    if old_image_path and old_image_path != saved_image_path:
        damage_detected_image, similarity_score = compare_images(old_image_path, saved_image_path)
        
        damage_detected_path = os.path.join(IMAGE_DIR, van_id, "damage_detected.jpg")
        damage_image = Image.fromarray(cv2.cvtColor(damage_detected_image, cv2.COLOR_BGR2RGB))
        damage_image.save(damage_detected_path)
        
        add_comparison(van_id, old_image_path, saved_image_path, similarity_score, damage_detected_path)
        
        st.image(damage_image, caption="Detected Damage", use_column_width=True)
        st.write(f"Similarity Score: {similarity_score}")
    else:
        st.write("No previous image found for comparison, or this is the first image for the van.")
