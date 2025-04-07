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
    df = df.copy()
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
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        df.fillna(0, inplace=True)

        existing_data[filename] = df.to_dict(orient="records")
        with open(FILES_JSON_PATH, "w") as file:
            json.dump(existing_data, file, indent=4)

        st.success("✅ File uploaded and processed successfully!")

# Sidebar - Select dataset
file_options = list(existing_data.keys())
selected_file = st.sidebar.selectbox("Select a dataset", file_options) if file_options else None

if selected_file:
    df = pd.DataFrame(existing_data[selected_file])

    # Preview data
    with st.expander("🧾 Dataset Preview"):
        st.dataframe(df.head())
        st.write("Available columns:", list(df.columns))

    # Sidebar Year Range if available
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
        selected_years_sidebar = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))
    else:
        selected_years_sidebar = None

    # User Query
    user_query = st.text_input("💬 Describe the data visualization you need:")

    if user_query:
        escaped_countries = [re.escape(c) for c in df["Country"].unique()]
        country_pattern = r"\b(?:{})\b".format("|".join(escaped_countries))
        country_match = re.findall(country_pattern, user_query, re.IGNORECASE)
        country_match = list(set(map(str.title, country_match)))

        year_match = re.search(r"from (\d{4}) to (\d{4})", user_query)
        year_range = (int(year_match.group(1)), int(year_match.group(2))) if year_match else selected_years_sidebar

        chart_type = "line" if "line" in user_query.lower() else "scatter" if "scatter" in user_query.lower() else "bar"

        keywords = re.findall(r"\b(population|gdp|density|literacy|coastline|migration|birthrate|deathrate|sector|agriculture|industry|service)\b", user_query, re.IGNORECASE)
        keywords = [k.lower() for k in set(keywords)]

        # Filter data
        filtered_df = filter_data(df, countries=country_match, years=year_range)

        # Display extracted info
        with st.expander("🔍 Extracted Filters"):
            st.write("**Keywords:**", keywords)
            st.write("**Countries:**", country_match or "All")
            st.write("**Year Range:**", year_range or "Not specified")
            st.write("**Chart Type:**", chart_type.capitalize())

        # Multiple chart generation
        generated = False
        for keyword in keywords:
            fig = None

            if keyword == "literacy" and "Literacy (%)" in filtered_df.columns:
                y_col = "Literacy (%)"

            elif keyword == "population" and "Population" in filtered_df.columns:
                y_col = "Population"

            elif keyword == "gdp" and "GDP ($ per capita)" in filtered_df.columns:
                y_col = "GDP ($ per capita)"

            elif keyword == "density" and "Pop. Density (per sq. mi.)" in filtered_df.columns:
                y_col = "Pop. Density (per sq. mi.)"

            elif keyword == "migration" and "Net migration" in filtered_df.columns:
                y_col = "Net migration"

            elif keyword in ["birthrate", "deathrate"]:
                cols = []
                if "Birthrate" in filtered_df.columns:
                    cols.append("Birthrate")
                if "Deathrate" in filtered_df.columns:
                    cols.append("Deathrate")
                if cols:
                    fig = px.bar(filtered_df, x="Country", y=cols, title="📊 Birthrate & Deathrate by Country") if chart_type == "bar" else px.line(filtered_df, x="Year", y=cols, color="Country", title="📈 Birthrate & Deathrate Over Years")
                    st.plotly_chart(fig, use_container_width=True)
                    generated = True
                    continue

            elif keyword in ["sector", "agriculture", "industry", "service"]:
                for col in ["Agriculture", "Industry", "Service"]:
                    if col in filtered_df.columns:
                        filtered_df[col] = pd.to_numeric(filtered_df[col], errors="coerce")
                long_df = filtered_df.melt(id_vars=["Country"], value_vars=["Agriculture", "Industry", "Service"], var_name="Sector", value_name="Contribution")
                fig = px.bar(long_df, x="Country", y="Contribution", color="Sector", title="📊 Economic Sector Contribution") if chart_type == "bar" else px.line(long_df, x="Country", y="Contribution", color="Sector", title="📈 Economic Sector Contribution")
                st.plotly_chart(fig, use_container_width=True)
                generated = True
                continue

            else:
                continue

            if y_col:
                if chart_type == "bar":
                    fig = px.bar(filtered_df, x="Country", y=y_col, title=f"{y_col} by Country")
                elif chart_type == "line" and "Year" in filtered_df.columns:
                    fig = px.line(filtered_df, x="Year", y=y_col, color="Country", title=f"{y_col} over Years")
                elif chart_type == "scatter" and "Year" in filtered_df.columns:
                    fig = px.scatter(filtered_df, x="Year", y=y_col, color="Country", title=f"{y_col} Scatter Plot")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    generated = True

        if not generated:
            st.warning("⚠️ No valid visualization could be generated for the given query.")

        # Download filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Data as CSV", csv, f"{selected_file}_filtered.csv", "text/csv")
