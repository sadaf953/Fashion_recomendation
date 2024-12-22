import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import display, HTML
import hashlib
import random

# Load the dataset
fashion_data = pd.read_csv("/kaggle/input/myntra-fashion-dataset/Myntra Fasion Clothing.csv")

# Rename columns
fashion_data.columns = [
    'URL', 'Product_id', 'BrandName', 'Category', 'Individual_category',
    'Category_by_Gender', 'Description', 'DiscountPrice', 'OriginalPrice',
    'DiscountOffer', 'SizeOption', 'Ratings', 'Reviews'
]

# Check for null values and clean the data
fashion_data = fashion_data.dropna()

# Calculate the weighted score for recommendations
mr = fashion_data['Ratings'].mean()
m = fashion_data['Reviews'].quantile(0.9)
n = fashion_data['Reviews']
a = fashion_data['Ratings']

fashion_data['Score'] = (n / (n + m) * a) + (m / (m + n) * mr)

# Sort by score
recommendations = fashion_data.sort_values('Score', ascending=False)
top_recommendations = recommendations.head(10)

# Display the top 10 recommendations with images
html_content = '<div style="display: flex; flex-wrap: wrap;">'
for index, row in top_recommendations.iterrows():
    html_content += f"""
    <div style="flex: 1 0 30%; box-sizing: border-box; padding: 10px; text-align: center;">
        <img src="{row['URL']}" style="width: 100px; height: 150px;"><br>
        <strong>Brand:</strong> {row['BrandName']}<br>
        <strong>Average Rating:</strong> {row['Ratings']}<br>
        <strong>Score:</strong> {row['Score']}<br>
        <strong>Price:</strong> {row['DiscountPrice']}<br>
    </div>
    """
html_content += '</div>'
display(HTML(html_content))

# Additional code from the first script
class ClothesItem:
    def __init__(self, description, category_by_gender, age_group, height_range_str, size, style, occasion, color):
        self.description = description
        self.gender = category_by_gender
        self.age_group = age_group
        self.height_range = parse_height_range(height_range_str)
        self.size = size
        self.style = style
        self.occasion = occasion
        self.color = color

class Person:
    def __init__(self, gender, age, height, size, preferences, occasion, skin_color):
        self.gender = gender
        self.age = age
        self.height = height
        self.size = size
        self.preferences = preferences
        self.occasion = occasion
        self.skin_color = skin_color

def parse_height_range(height_range_str):
    height_range_str = height_range_str.replace('range(', '').replace(')', '')    
    start, end = map(int, height_range_str.split(','))
    height_range = range(start, end)
    return height_range

def filter_clothes(clothes_list, person):
    filtered_clothes = []
    for item in clothes_list:
        if (item.gender == person.gender and 
            item.age_group == get_age_group(person.age) and 
            person.height in item.height_range and 
            person.size == item.size and 
            item.style in person.preferences and 
            item.occasion == person.occasion and 
            item.color in get_compatible_colors(person.skin_color)):
            filtered_clothes.append(item)
    return filtered_clothes

def get_age_group(age):
    if age < 18:
        return "child"
    elif age < 30:
        return "young_adult"
    elif age < 50:
        return "adult"
    else:
        return "senior"

def get_compatible_colors(skin_color):
    color_dict = {
        "fair": ["white", "light blue", "pastel colors", "lavender", "soft pink", "mint green", "peach", "silver", "gold", "rose"],
        "light": ["pastel shades", "light gray", "soft yellow", "sky blue", "lavender", "soft green", "blush pink", "champagne", "taupe", "rose gold"],
        "medium": ["black", "red", "navy blue", "olive green", "mustard yellow", "rust orange", "teal", "burgundy", "eggplant purple", "camel"],
        "olive": ["earth tones", "olive green", "mustard yellow", "rust orange", "burnt sienna", "khaki", "taupe", "brick red", "deep purple", "gold"],
        "tan": ["warm neutrals", "coral", "peach", "terracotta", "salmon pink", "mint green", "camel", "copper", "bronze", "teal"],
        "caramel": ["rich jewel tones", "chocolate brown", "emerald green", "sapphire blue", "ruby red", "deep purple", "mustard yellow", "burnt orange", "burgundy", "gold"],
        "brown": ["deep earth tones", "chocolate brown", "olive green", "burnt orange", "mahogany", "deep teal", "aubergine", "maroon", "charcoal gray", "bronze"],
        "dark_brown": ["rich earthy shades", "chocolate brown", "aubergine", "forest green", "deep teal", "burgundy", "charcoal gray", "navy blue", "black", "gold"],
        "deep_brown": ["bold jewel tones", "royal blue", "emerald green", "deep purple", "rich burgundy", "sapphire blue", "ruby red", "plum", "burnt orange", "gold"],
        "ebony": ["vibrant colors", "bright red", "electric blue", "sunny yellow", "fuchsia pink", "orange", "lime green", "turquoise", "deep purple", "silver"]
    }
    return color_dict.get(skin_color, [])

def rate_outfit(outfit, person):
    # Implementing the rating logic
    return random.uniform(0, 1)

def recommend_outfits(clothes_list, person):
    filtered_clothes = filter_clothes(clothes_list, person)
    rated_outfits = [(outfit, rate_outfit(outfit, person)) for outfit in filtered_clothes]
    sorted_outfits = sorted(rated_outfits, key=lambda x: x[1], reverse=True)
    return sorted_outfits

def unique_outfit_code(outfit):
    outfit_info = f"{outfit.description}-{outfit.gender}-{outfit.age_group}-{outfit.height_range}-{outfit.size}-{outfit.style}-{outfit.occasion}-{outfit.color}"
    hashed_info = hashlib.sha1(outfit_info.encode()).hexdigest()
    return hashed_info[:10]

# Creating the clothes list and person object
clothes_list = [
    ClothesItem(
        row['Description'],  
        row['Category_by_Gender'],  
        get_age_group(30),  # Placeholder age, modify as needed
        f"range({165 - 5}, {165 + 5})",  # Placeholder height range, modify as needed
        row['SizeOption'],  
        row['Category'],  
        "everyday",  # Placeholder occasion, modify as needed
        "color"  # Placeholder color, modify as needed
    )  
    for _, row in fashion_data.iterrows()
]
person = Person("Female", 30, 165, "M", ["casual"], "everyday", "medium")

# Getting recommendations
recommended_outfits = recommend_outfits(clothes_list, person)
for outfit, rating in recommended_outfits:
    print(outfit.description, '|', unique_outfit_code(outfit), '|', rating)

