import streamlit as st
import requests
import random
import openai

openai.api_key=st.secrets["openai_api_key"]

# Function to generate outfit recommendations using ChatGPT
def generate_outfit_recommendations(user_inputs):
    # Generate outfit recommendations using ChatGPT
    prompt = f"User Inputs: {user_inputs}\n\nAI: Generate outfit recommendation for the user."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=5,  # Number of outfit recommendations to generate
        stop=None,
    )

    recommendations = []
    outfit_keywords = []

    for choice in response.choices:
        recommendation = choice["text"].strip()
        recommendations.append(recommendation)

        # Ask ChatGPT for outfit keywords
        keywords_prompt = f"Outfit: {recommendation}\n\nAI: Provide clothes list in this statement in comma separated values."
        keywords_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=keywords_prompt,
            max_tokens=100,
            temperature=0.3,
            n=1,  # Number of keyword suggestions to generate
            stop=None,
        )

        outfit_keywords.append(keywords_response.choices[0]["text"].strip())

    return recommendations, outfit_keywords

# Function to fetch product information from Amazon API
def fetch_product_info(product_name):
    # Placeholder implementation using Amazon API
    # Send a request to the Amazon API to search for the product
    # Retrieve and return the product information (e.g., title, price, image URL)

    # Placeholder code to generate dummy product information
    product_info = {
        "title": "Product Title",
        "price": "$99.99",
        "image_url": "https://example.com/product_image.jpg"
    }
    return product_info

# Streamlit app
def main():
    st.title("AI Stylist Guide")
    
    # User inputs
    event_type = st.selectbox("Event Type", ["Casual", "Formal", "Party", "Work", "Other"])
    color_preference = st.text_input("Color Preference", "")
    style_preference = st.text_input("Style Preference", "")
    gender_preference=st.selectbox("Gender Preference", ["Male","Female","No Preference"])
    custom_response = st.text_input("Custom Request", "")

    # Submit Button
    if st.button("Submit"):
        user_inputs = f"Event Type: {event_type}\nColor Preference: {color_preference}\nStyle Preference: {style_preference}\nCustom Response: {custom_response}\nGender Preference: {gender_preference}"

        if user_inputs:
            outfit_recommendations, outfit_keywords = generate_outfit_recommendations(user_inputs)
            st.subheader("Outfit Recommendations")
            for i, outfit in enumerate(outfit_recommendations):
                st.write(f"Outfit {i + 1}: {outfit}")
                st.write(f"Keywords: {outfit_keywords[i].split(',')}")
                st.write("---")
        else:
            st.warning("Please enter your preferences.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
