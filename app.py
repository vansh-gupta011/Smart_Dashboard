import streamlit as st
import pandas as pd
import re
import json
import os
import plotly.express as px

# Constants
FILES_JSON_PATH = "files.json"

# Load existing data from JSON
def load_json():
    if os.path.exists(FILES_JSON_PATH):
        with open(FILES_JSON_PATH, "r") as file:
            return json.load(file)
    return {}

# Filter data based on countries and years
def filter_data(df, countries=None, years=None):
    if countries:
        df = df[df["Country"].isin(countries)]
    if years and "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df = df[df["Year"].between(years[0], years[1])]
    return df

# Streamlit UI Configuration
st.set_page_config(page_title="Country Statistics Dashboard", layout="wide")
st.title("📊 Country Statistics Dashboard")
st.sidebar.header("Upload CSV File")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])
existing_data = load_json()

if uploaded_file:
    filename = uploaded_file.name
    if filename in existing_data:
        st.success(f"✅ '{filename}' is already uploaded!")
    else:
        # Process and save the uploaded file to JSON
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        df.fillna(0, inplace=True)  # Replace NaN with 0 for simplicity

        # Save the new file data into JSON storage
        existing_data[filename] = df.to_dict(orient="records")
        with open(FILES_JSON_PATH, "w") as file:
            json.dump(existing_data, file, indent=4)

        st.success("✅ File uploaded and processed successfully!")

# Sidebar - Select dataset to analyze
file_options = list(existing_data.keys())
selected_file = st.sidebar.selectbox("Select a dataset", file_options) if file_options else None

if selected_file:
    # Load the selected dataset into a DataFrame
    df = pd.DataFrame(existing_data[selected_file])

    # User Query Input for Visualization Requests
    user_query = st.text_input("💬 Describe the data visualization you need:")

    if user_query:
        # Extract keywords from user query using regex
        keywords = re.findall(r"\b(population|gdp|density|literacy|coastline|migration|birthrate|deathrate|sector|agriculture|industry|service)\b", user_query, re.IGNORECASE)
        keywords = [k.lower() for k in set(keywords)]

        # Extract country names from user query based on dataset's unique values
        country_match = re.findall(r"\b(?:{})\b".format("|".join(df["Country"].unique())), user_query, re.IGNORECASE)

        # Extract year range from user query (e.g., "from 2001 to 2015")
        year_match = re.search(r"from (\d{4}) to (\d{4})", user_query)
        year_range = (int(year_match.group(1)), int(year_match.group(2))) if year_match else None

        # Filter data based on extracted countries and years
        filtered_df = filter_data(df, countries=country_match, years=year_range)

        # Generate visualizations based on keywords
        fig = None  # Initialize figure variable

        if "literacy" in keywords and "Literacy (%)" in filtered_df.columns:
            fig = px.bar(filtered_df, x="Country", y="Literacy (%)", title="📚 Literacy Rate Across Selected Countries")

        elif "population" in keywords and "Population" in filtered_df.columns:
            fig = px.bar(filtered_df, x="Country", y="Population", title="🌍 Population Distribution")

        elif "gdp" in keywords and "GDP ($ per capita)" in filtered_df.columns:
            fig = px.bar(filtered_df, x="Country", y="GDP ($ per capita)", title="💰 GDP Distribution")

        elif any(k in keywords for k in ["agriculture", "industry", "service"]):
            filtered_df[["Agriculture", "Industry", "Service"]] = filtered_df[["Agriculture", "Industry", "Service"]].apply(pd.to_numeric, errors="coerce")
            long_df = filtered_df.melt(id_vars=["Country"], value_vars=["Agriculture", "Industry", "Service"], var_name="Sector", value_name="Contribution")
            fig = px.bar(long_df, x="Country", y="Contribution", color="Sector", title="Economic Sector Contribution")

        elif "migration" in keywords and "Net migration" in filtered_df.columns:
            fig = px.bar(filtered_df, x="Country", y="Net migration", title="🚀 Net Migration")

        elif any(k in keywords for k in ["birthrate", "deathrate"]):
            available_metrics = [col for col in ["Birthrate", "Deathrate"] if col in filtered_df.columns]
            if available_metrics:
                fig = px.bar(filtered_df, x="Country", y=available_metrics, title="📊 Birthrate & Deathrate by Country")

        else:
            st.warning("⚠️ No valid visualization could be generated for the given query.")

        # Display the figure if it was created
        if fig:
            st.plotly_chart(fig, use_container_width=True)
