
# This is the python script, you basically can use this or the notebook
import os
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import json
     

def extract_color_histogram(image_path, bins=(8, 8, 8)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

     

# Directory containing your images
image_dir = '/content/dataset/known_images/class1'

# Dictionary to store image features
features_dict = {}

for img_name in os.listdir(image_dir):
    img_path = os.path.join(image_dir, img_name)
    # Ensure the file is an image
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        features = extract_color_histogram(img_path)
        features_dict[img_name] = features

# Save the features to a file
with open('image_features.pkl', 'wb') as f:
    pickle.dump(features_dict, f)
     

def is_image_known(new_img_path, features_dict, threshold=0.8):
    new_features = extract_color_histogram(new_img_path)
    for img_name, stored_features in features_dict.items():
        similarity = cosine_similarity([new_features], [stored_features])[0][0]
        if similarity >= threshold:
            return True, img_name, similarity
    return False, None, None
with open('image_features.pkl', 'rb') as f:
    features_dict = pickle.load(f)
     

new_image_path = '/content/dataset/known_images/class2/1664430467865.jpg'
known, img_name, similarity = is_image_known(new_image_path, features_dict)

result = {
    'known': known,
    'img_name': img_name,
    'similarity': similarity
}

print(json.dumps(result))

     
