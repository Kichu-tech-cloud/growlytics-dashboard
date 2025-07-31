import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
import random

# --- Setup ---
st.set_page_config(page_title="Growlytics Dashboard", layout="wide", page_icon="📊")

# --- Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
        font-family: 'Segoe UI', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #e3f2fd;
    }
    .stDataFrame > div {
        overflow-x: auto;
    }
    .block-container {
        padding-top: 1rem;
    }
    .css-hxt7ib, .css-1lcbmhc.e1fqkh3o8, .css-6qob1r.e1fqkh3o4 {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Caching ---
@st.cache_data
def load_csv(path, parse_dates=False):
    return pd.read_csv(path, parse_dates=["Date"] if parse_dates else None)

def save_uploaded_file(file, filename):
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(file.read())

@st.cache_data
def load_sample_sales():
    dates = pd.date_range(start="2024-01-01", periods=120)
    data = {
        "Date": dates,
        "Region": random.choices(["Retail", "Corporate", "Online", "Wholesale"], k=len(dates)),
        "Amount": [random.randint(5000, 15000) for _ in range(len(dates))]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_sample_orders():
    dates = pd.date_range(start="2024-01-01", periods=120)
    data = {
        "Date": dates,
        "Customer": random.choices(["A Corp", "B Ltd", "C Inc"], k=len(dates)),
        "Category": random.choices(["Bulk", "Single", "Subscription"], k=len(dates)),
        "Orders": [random.randint(50, 150) for _ in range(len(dates))]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_sample_traffic():
    dates = pd.date_range(start="2024-01-01", periods=120)
    data = {
        "Date": dates,
        "Channel": random.choices(["SEO", "PPC", "Email", "Social"], k=len(dates)),
        "Visitors": [random.randint(200, 1000) for _ in range(len(dates))]
    }
    return pd.DataFrame(data)

# --- Sidebar ---
st.sidebar.title("📊 Growlytics")
pages = {
    "🏠 Overview": "overview",
    "📈 Sales Report": "sales",
    "📊 Traffic Funnel": "traffic",
    "📦 Orders": "orders",
    "⚙️ Settings": "settings",
    "📤 Upload Files": "upload",
    "📑 Reports": "reports",
    "❓ Help": "help"
}
selection = st.sidebar.radio("", list(pages.keys()))

# --- File Upload ---
if pages[selection] == "upload":
    st.title("📤 Upload CSV Files")
    exp_file = st.file_uploader("Upload Expense CSV", type="csv")
    gro_file = st.file_uploader("Upload Growth CSV", type="csv")
    sales_file = st.file_uploader("Upload Sales CSV", type="csv")
    orders_file = st.file_uploader("Upload Orders CSV", type="csv")
    traffic_file = st.file_uploader("Upload Traffic CSV", type="csv")

    if exp_file: save_uploaded_file(exp_file, "expense_data.csv"); st.success("✅ Expense data uploaded.")
    if gro_file: save_uploaded_file(gro_file, "growth_data.csv"); st.success("✅ Growth data uploaded.")
    if sales_file: save_uploaded_file(sales_file, "sales_data.csv"); st.success("✅ Sales data uploaded.")
    if orders_file: save_uploaded_file(orders_file, "orders_data.csv"); st.success("✅ Orders data uploaded.")
    if traffic_file: save_uploaded_file(traffic_file, "traffic_data.csv"); st.success("✅ Traffic data uploaded.")

# --- Load Data ---
try: expenses = load_csv(os.path.join(UPLOAD_DIR, "expense_data.csv"), parse_dates=True)
except: expenses = pd.read_csv("sample_csv/expense_sample_enhanced.csv", parse_dates=["Date"])

try: growth = load_csv(os.path.join(UPLOAD_DIR, "growth_data.csv"), parse_dates=True)
except: growth = pd.read_csv("sample_csv/growth_sample.csv", parse_dates=["Date"])

try: sales = load_csv(os.path.join(UPLOAD_DIR, "sales_data.csv"), parse_dates=True)
except: sales = load_sample_sales()

try: orders = load_csv(os.path.join(UPLOAD_DIR, "orders_data.csv"), parse_dates=True)
except: orders = load_sample_orders()

try: traffic = load_csv(os.path.join(UPLOAD_DIR, "traffic_data.csv"), parse_dates=True)
except: traffic = load_sample_traffic()

# --- Overview ---
if pages[selection] == "overview":
    st.title("📊 Dashboard Overview")
    col1, col2 = st.columns(2)

    with col1:
        exp_monthly = expenses.groupby(expenses['Date'].dt.to_period("M"))['Amount'].sum().reset_index()
        exp_monthly['Date'] = exp_monthly['Date'].astype(str)
        fig = px.bar(exp_monthly, x="Date", y="Amount", title="Monthly Expenses")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        gro_monthly = growth.groupby(growth['Date'].dt.to_period("M"))['Amount'].sum().reset_index()
        gro_monthly['Date'] = gro_monthly['Date'].astype(str)
        fig = px.line(gro_monthly, x="Date", y="Amount", title="Monthly Growth", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Insights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Expense", f"₹{expenses['Amount'].sum():,.2f}")
    with col2:
        st.metric("📈 Total Growth", f"₹{growth['Amount'].sum():,.2f}")
    with col3:
        st.metric("📦 Total Orders", f"{orders['Orders'].sum()} orders")

# --- Sales Report ---
if pages[selection] == "sales":
    st.title("📈 Sales Report")
    if "Department" in sales.columns:
        st.date_input("Select Date Range", [sales['Date'].min(), sales['Date'].max()])
        dept = st.multiselect("Department", options=sales["Department"].unique(), default=sales["Department"].unique())
        filtered = sales[sales["Department"].isin(dept)]
        fig = px.bar(filtered, x="Date", y="Amount", color="Department", title="Sales by Department")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("📥 Download Sales (Excel)", filtered.to_csv(index=False).encode(), file_name="sales.xlsx")
    else:
        st.subheader("📊 Basic Sales Trend")
        fig = px.line(sales, x="Date", y="Amount", color="Region" if "Region" in sales.columns else None, title="Sales Trend")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("📥 Download Sales (Excel)", sales.to_csv(index=False).encode(), file_name="sales.xlsx")

# --- Traffic Funnel ---
if pages[selection] == "traffic":
    st.title("📊 Traffic Funnel")
    channel = st.multiselect("Channel", traffic["Channel"].unique(), default=traffic["Channel"].unique())
    filtered = traffic[traffic["Channel"].isin(channel)]
    fig = px.area(filtered, x="Date", y="Visitors", color="Channel", title="Traffic by Channel")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered, use_container_width=True, height=400, hide_index=True, column_config={"Channel": st.column_config.TextColumn(width="small")})

# --- Orders ---
if pages[selection] == "orders":
    st.title("📦 Orders")
    fig = px.line(orders, x="Date", y="Orders", color="Category", title="Order Volume")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(orders, use_container_width=True, height=400, hide_index=True, column_config={"Category": st.column_config.TextColumn(width="small")})

# --- Settings ---
if pages[selection] == "settings":
    st.title("⚙️ Profile Settings")
    with st.expander("👤 Edit Profile"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Name", "John Doe")
            st.text_input("Email", "john@example.com")
        with col2:
            st.selectbox("Role", ["Admin", "Analyst", "Viewer"])
            st.checkbox("Receive Reports", True)

    st.subheader("📊 Growth Type Overview")
    pie_data = growth["Type"].value_counts().reset_index()
    pie_data.columns = ["Type", "Count"]
    fig = px.pie(pie_data, names="Type", values="Count", title="Growth by Type")
    st.plotly_chart(fig, use_container_width=True)

# --- Reports ---
if pages[selection] == "reports":
    st.title("📑 Reports")

    st.subheader("🧾 Expense Table")
    st.dataframe(expenses, use_container_width=True, height=350)
    st.download_button("⬇️ Download Expenses", expenses.to_csv(index=False).encode(), file_name="expenses.xlsx")

    st.subheader("📈 Growth Table")
    st.dataframe(growth, use_container_width=True, height=350)
    st.download_button("⬇️ Download Growth", growth.to_csv(index=False).encode(), file_name="growth.xlsx")

    cat = expenses.groupby("Category")["Amount"].sum().reset_index()
    st.plotly_chart(px.pie(cat, names="Category", values="Amount", title="Expense by Category"), use_container_width=True)

    proj = growth.groupby("Project/Investor")["Amount"].sum().reset_index()
    st.plotly_chart(px.bar(proj, x="Project/Investor", y="Amount", title="Growth by Project/Investor"), use_container_width=True)

# --- Help ---
if pages[selection] == "help":
    st.title("❓ Help & Support")
    st.markdown("""
        - 📧 Email: support@growlytics.com  
        - ☎️ Phone: +91-98765-43210  
        - 💬 Live Chat Support (Mon–Fri, 10AM–6PM)
    """)
