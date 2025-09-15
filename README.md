# 💹 CapNex — AI-Powered Economic Dashboard & Insights

CapNex is an intelligent economic analytics dashboard designed for researchers, analysts, and policymakers. It provides interactive exploration, visualization, forecasting, capital mix optimization, and AI-driven insights on macroeconomic data.

By combining Streamlit, Prophet, Matplotlib, Pandas, and AI tools, CapNex turns complex datasets into actionable insights for smarter decision-making.

# 🌟 Key Features
🔮 Dashboard

Explore economic datasets interactively by Country and Indicator.

Display first rows of the dataset for quick overview.

Generate time series charts with dynamic plotting of selected indicators.

AI-generated summaries of trends, highlighting whether indicators are increasing, decreasing, or stable.

📈 Forecasting

Forecast future trends for selected indicators using Prophet.

Customize forecast horizon (1–8 quarters).

Automatic trend detection and AI-generated summary for predicted values.

Converts numerical values to billions (B) for readability.

Handles missing data and aggregates multiple rows for robust forecasting.

⚖️ Capital Mix Optimization Analytics

Input working capital and allocate percentages to Cash, Inventory, Receivables, and Payables.

Automatically compute monetary allocations.

Visualize allocations with bar charts.

AI-driven recommendations for liquidity management, inventory optimization, and cash flow improvement.

🤖 Ask CapNex — Economic AI Assistant

Ask natural language questions about the dataset.

AI detects Country and Indicator context to provide accurate summaries.

Maintains question-answer history during the session.

Can summarize entire country data or specific indicators.

# 📂 Project Structure
CapNex/
│── app.py                 # Main Streamlit application
│── data/
│    └── nea_quarterly.csv # National Economic Accounts (Quarterly) dataset
│── requirements.txt       # Python dependencies
│── .env                   # Environment variables (API keys)
└── README.md              # Documentation

# 📊 Dataset

CapNex uses the National Economic Accounts (NEA), Quarterly Data from the IMF Data Portal
Link - https://data.imf.org/en/datasets/IMF.STA:QNEA

Dataset Highlights:

Covers quarterly economic indicators for multiple countries.

Key indicators include: GDP, consumption, investment, government spending, foreign trade, and more.

Available in seasonally adjusted and non-seasonally adjusted formats.

Ideal for time series analysis, forecasting, and AI-driven insights.

Dataset Path: data/nea_quarterly.csv

# ⚡ Quick Start
1️⃣ Clone the Repository
git clone https://github.com/your-username/capnex.git
cd capnex

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows (PowerShell):

.\venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
streamlit run app.py

# 🛠️ Tech Stack

Frontend/UI: Streamlit, Matplotlib

Data Handling: Pandas, NumPy

Time Series Forecasting: Prophet

AI & NLP: HuggingFace Transformers, FinBERT

Vector Search: FAISS + SentenceTransformers

Environment: Python 3.10+, dotenv for secure key management

# 🚀 Future Enhancements

Portfolio Analytics: Evaluate multi-country portfolios and capital allocation strategies.

Advanced Forecasting Models: Integration of ML models for enhanced prediction accuracy.

Expanded News Sources: Incorporate Bloomberg, Reuters, and other APIs for real-time news.

User Customization: Save favorite countries, indicators, and dashboard settings.

Deployment: Streamlit Cloud or Docker for easy sharing and access.

# 🤝 Contributing

Fork the repository.

Create a branch: git checkout -b feature-xyz.

Commit changes: git commit -m "Add feature xyz".

Push to branch: git push origin feature-xyz.

Open a Pull Request.
