import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Spending Pattern Tracker", layout="wide")
st.title("💰 Personal Spending Pattern & Savings Advisor")

uploaded_file = st.file_uploader("📤 Upload your Bank Statement (CSV)", type="csv")

category_keywords = {
    'Food': ['kfc', 'restaurant', 'dominos', 'zomato', 'swiggy'],
    'Transport': ['uber', 'ola', 'bus', 'metro', 'taxi'],
    'Shopping': ['amazon', 'flipkart', 'myntra'],
    'Rent': ['rent', 'landlord'],
    'Bills': ['electricity', 'wifi', 'water'],
    'Others': []
}

def categorize(description):
    description = str(description).lower()
    for category, keywords in category_keywords.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'Others'

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Category'] = df['Description'].apply(categorize)
    
    expenses = df[df['Type'].str.lower() == 'debit']
    income = df[df['Type'].str.lower() == 'credit']

    st.subheader("📊 Monthly Spending Summary")
    monthly_expenses = expenses.groupby(expenses['Date'].dt.to_period("M"))['Amount'].sum()
    st.line_chart(monthly_expenses)

    st.subheader("🍕 Spending by Category")
    category_sum = expenses.groupby('Category')['Amount'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=category_sum, x='Amount', y='Category', ax=ax, palette="viridis")
    st.pyplot(fig)

    st.subheader("💡 Savings Suggestions")
    avg_monthly = monthly_expenses.mean()
    top_category = category_sum.sort_values(by="Amount", ascending=False).iloc[0]
    st.markdown(f"🔹 You spend the most on **{top_category['Category']}** (₹{top_category['Amount']:.2f}). Try reducing it by 10% to save ₹{top_category['Amount']*0.1:.2f}/month.")
    st.markdown(f"🔹 Your average monthly spend is ₹{avg_monthly:.2f}. Target 90% of this to boost savings.")

    st.subheader("📄 Raw Data")
    st.dataframe(df)
else:
    st.info("Upload a CSV file to start analysis.")
