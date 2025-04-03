Smart_Dashboard
📊 Dynamic Data Visualization Dashboard
Smart_Dashboard is an interactive, query-driven data visualization tool built using FastAPI and Streamlit. It allows users to upload CSV files, describe the visualizations they need in natural language, and dynamically generate insightful graphs and charts. The project is designed to simplify data exploration and analysis for both technical and non-technical users.

Features
CSV File Upload: Easily upload datasets for analysis.

Dynamic Query Processing: Generate visualizations based on user queries (e.g., "Plot literacy rate across India and Pakistan").

Interactive Visualizations: Supports bar charts, line charts, scatter plots, and more using Plotly.

Data Filtering: Filter data by countries, years, or specific metrics.

Predefined Categories: Automatically classify queries into categories like GDP analysis, literacy rate tracking, migration patterns, etc.

User-Friendly Interface: Built with Streamlit for a seamless user experience.

Technologies Used
FastAPI: Backend framework for handling file uploads and preprocessing.

Streamlit: Frontend framework for interactive dashboards.

Plotly: Library for creating dynamic visualizations.

Pandas: Data manipulation and analysis library.

OpenAI GPT Model (Optional): For advanced query classification (if integrated).

Installation
Follow these steps to set up the project locally:

1. Clone the Repository
bash
git clone https://github.com/yourusername/Smart_Dashboard.git
cd Smart_Dashboard
2. Create a Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Run FastAPI Backend
Start the backend server to handle file uploads:

bash
uvicorn main:app --reload
5. Run Streamlit Frontend
Launch the Streamlit dashboard for querying and visualizing data:

bash
streamlit run app.py
Usage
Uploading a CSV File:
Open the Streamlit dashboard.

Upload your CSV file using the sidebar uploader.

Querying Data:
Enter your query in the text input field (e.g., "Plot GDP per capita across countries").

View dynamically generated visualizations based on your query.

Example Queries:
"Show population distribution across countries."

"Compare literacy rates between India and Pakistan."

"Visualize migration trends from 2000 to 2020."

"Analyze GDP per capita vs. literacy rate."

Project Structure
text
Smart_Dashboard/
├── main.py                # FastAPI backend for file uploads and preprocessing
├── app.py                 # Streamlit frontend for querying and visualizing data
├── files.json             # JSON storage for uploaded datasets
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
