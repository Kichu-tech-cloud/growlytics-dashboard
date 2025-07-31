import streamlit as st
import plotly.express as px

def plot_expenses_dashboard(df):
    st.markdown("### 🔹 Monthly Expense Overview")
    monthly = df.groupby('Month')['Amount'].sum().reset_index()
    fig = px.bar(monthly, x='Month', y='Amount', title="Monthly Expenses", color='Amount')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔹 Department-wise Expense Split")
    dept = df.groupby('Department')['Amount'].sum().reset_index()
    fig2 = px.pie(dept, names='Department', values='Amount', title="Expenses by Department")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🔹 Category-wise Breakdown")
    cat = df.groupby('Category')['Amount'].sum().reset_index()
    fig3 = px.bar(cat, x='Category', y='Amount', title="Expenses by Category", color='Amount')
    st.plotly_chart(fig3, use_container_width=True)

def plot_growth_dashboard(df):
    st.markdown("### 🔹 Monthly Growth Overview")
    monthly = df.groupby('Month')['Amount'].sum().reset_index()
    fig = px.line(monthly, x='Month', y='Amount', markers=True, title="Monthly Growth (Projects + Investments)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔹 Type-wise Growth Split")
    growth_type = df.groupby('Type')['Amount'].sum().reset_index()
    fig2 = px.pie(growth_type, names='Type', values='Amount', title="Growth by Type (Project vs Investor)")
    st.plotly_chart(fig2, use_container_width=True)
