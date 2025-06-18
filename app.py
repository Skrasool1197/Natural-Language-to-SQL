import os
import sqlite3
import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Database Schema Information
schema_info = """
Tables and Columns:

• customers (customer_id, registration_date, city, gender) ['M' or 'F']
• orders (order_id, customer_id, order_date, total_amount, status) ['completed', 'pending']
• order_items (item_id, order_id, product_name, quantity, unit_price)
"""

# Prompt for the LLM
prompt = ["""
You are an expert assistant for generating SQL queries.

## Rules to Follow STRICTLY:

1. Only use the following database schema:

Tables and Columns:

- customers (customer_id, registration_date, city, gender ['M' or 'F'])
- orders (order_id, customer_id, order_date, total_amount, status ['completed', 'pending'])
- order_items (item_id, order_id, product_name, quantity, unit_price)

2. NEVER use any table or column name that is not listed above.

3. MPORTANT: Dates are in 'YYYY-MM-DD' format. For monthly analysis, use:
- strftime('%Y-%m', registration_date)

4. For queries like "last month," **generate SQL using**:
- WHERE strftime('%Y-%m', registration_date) = strftime('%Y-%m', 'now', '-1 month')

5. The 'gender' column uses 'M' for male and 'F' for female.

6. The 'status' column uses 'completed' or 'pending'.

7. Your output should be ONLY the SQL query, NO explanations, NO formatting like ``` or SQL word, NO comments.

8. The SQL should be compatible with SQLite.

9. If the question does not relate to this schema, respond with:
"I cannot generate a SQL query for this question because it does not match the database schema."

10. Use aliases and JOINs correctly when needed. Do not assume column names that do not exist.

## Examples for Guidance:
Q: Count new customers who joined last month.
A: SELECT COUNT(*) FROM customers WHERE registration_date >= DATE('now', '-1 month');

Q: What is the male to female customer ratio?
A: SELECT gender, COUNT(*) FROM customers GROUP BY gender;

Q: Show total sales for each month in 2023.
A: SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS total_sales FROM orders WHERE strftime('%Y', order_date) = '2023' GROUP BY month;

Q: Find orders placed by customers in Mumbai.
A: SELECT * FROM orders WHERE customer_id IN (SELECT customer_id FROM customers WHERE city = 'Mumbai');

Now generate only the SQL query for the user's question.

"""]

# LLM Function
def model_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Query Execution
def read_sql_query(sql, db="retail_db.sqlite"):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        col_names = [description[0] for description in cur.description] if cur.description else []
        conn.close()
        return pd.DataFrame(rows, columns=col_names) if col_names else pd.DataFrame()
    except Exception as e:
        st.error(f"Error executing SQL: {e}")
        return pd.DataFrame()

# Streamlit UI
st.set_page_config(page_title="SQL Query Generator", page_icon="📊", layout="wide")
st.title("🔎 Natural Language to SQL Query Generator")

with st.expander("📂 Show Database Schema"):
    st.code(schema_info)

question = st.text_input("Ask a question about the database:", placeholder="e.g. Count new customers who joined last month.")

def is_error_message(response):
    return response.lower().startswith("i cannot generate")

if st.button("Generate SQL Query"):
    if question:
        generated_response = model_response(question, prompt)
        
        if is_error_message(generated_response):
            st.error(generated_response)
        else:
            st.code(generated_response, language="sql")
            result = read_sql_query(generated_response)

            st.subheader("Query Results:")
            if not result.empty:
                if result.shape == (1, 1):
                    st.success(f"Answer: {result.iloc[0, 0]}")
                else:
                    st.dataframe(result)
            else:
                st.info("No results found or the query did not return data.")
    else:
        st.warning("Please enter a question to generate SQL.")
