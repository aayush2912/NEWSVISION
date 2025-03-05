import streamlit as st
import requests

# --- Initialize Session State for Search History & Bookmarks ---
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []
if "bookmarked_articles" not in st.session_state:
    st.session_state["bookmarked_articles"] = []

# Set page title and description
st.set_page_config(page_title="NewsVision - Personalized News Recommendation", page_icon="📰")
st.title("📰 NewsVision")
st.title("Personalized News Recommendation System")
st.write("Enter a news topic or headline, and we'll recommend similar articles!")

# --- Autocomplete Suggestions ---
suggestions = [
    "Climate change policies",
    "US Elections 2024",
    "AI in healthcare",
    "Cryptocurrency market trends",
    "Stock market predictions",
    "Sports updates on FIFA World Cup",
    "Latest advancements in space technology"
]

# --- User Input with Autocomplete ---
user_input = st.text_input("🔍 Enter a news headline or topic:", placeholder="e.g., Climate change policies")
if user_input:
    matches = [s for s in suggestions if user_input.lower() in s.lower()]
    if matches:
        st.write("🔹 Suggested Topics:")
        for match in matches:
            st.markdown(f"- {match}")

# --- API Call Function ---
def get_recommendations(title):
    url = "http://127.0.0.1:5000/recommend"  # Update with deployed URL if hosted online
    payload = {"title": title}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json().get("recommended_articles", [])
    else:
        return None

# --- Submit Button ---
if st.button("Get Recommendations"):
    if user_input:
        # Add to Search History
        st.session_state["search_history"].append(user_input)

        recommendations = get_recommendations(user_input)

        if recommendations:
            st.subheader("📌 Recommended Articles:")
            for i, article in enumerate(recommendations, 1):
                st.markdown(f"**{i}. 🔹 {article['title']}**\n\n_Category: {article['category']}_")

                # Like & Dislike Buttons
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button(f"👍 Like {i}", key=f"like_{i}"):
                        st.success("Thank you for your feedback! 👍")
                with col2:
                    if st.button(f"👎 Dislike {i}", key=f"dislike_{i}"):
                        st.warning("Noted! We'll improve recommendations. 👎")
                with col3:
                    if st.button(f"📌 Bookmark {i}", key=f"bookmark_{i}"):
                        st.session_state["bookmarked_articles"].append(article)
                        st.info("Article bookmarked! 📌")
        else:
            st.error("No recommendations found. Try another topic.")
    else:
        st.warning("Please enter a news topic to get recommendations.")

# --- Search History Section ---
if st.session_state["search_history"]:
    st.subheader("🔍 Search History")
    for past_query in st.session_state["search_history"][-5:]:  # Show last 5 searches
        st.markdown(f"- {past_query}")

# --- Bookmarked Articles Section ---
if st.session_state["bookmarked_articles"]:
    st.subheader("📌 Saved Articles")
    for article in st.session_state["bookmarked_articles"]:
        st.markdown(f"**🔹 {article['title']}**\n\n_Category: {article['category']}_")

# --- Footer ---
st.markdown("---")
st.write("**BERT-based Content Filtering** for AI-powered news recommendations.")