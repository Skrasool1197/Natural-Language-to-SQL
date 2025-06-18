# Natural Language to SQL Query Generator

A Streamlit-based application that converts natural language questions into SQL queries using Google's Gemini AI, specifically designed for a retail database system.

## Features

- Natural language to SQL query conversion
- Interactive web interface using Streamlit
- Real-time query execution and result display
- Built-in sample retail database
- Support for complex SQL queries
- Database schema visualization

## Database Schema

The application uses a SQLite database with the following structure:

```sql
customers (customer_id, registration_date, city, gender)
orders (order_id, customer_id, order_date, total_amount, status)
order_items (item_id, order_id, product_name, quantity, unit_price)
```

## Prerequisites

- Python 3.10 or higher
- Google Cloud API key with Gemini AI access

## Setup Instructions

1. Clone the repository:
```bash
git clone <https://github.com/Skrasool1197/Natural-Language-to-SQL.git>
cd <Natural-Language-to-SQL>
```

2. Create and activate a virtual environment:
```bash
python -m venv taskEnv
source taskEnv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

5. Initialize the database:
```bash
python create_database.py
```

6. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Access the application through your web browser (http://localhost:8501)
2. View the database schema by expanding the "Show Database Schema" section
3. Enter your question in natural language (e.g., "Show total sales for each month in 2023")
4. Click "Generate SQL Query" to see the SQL query and its results

## Example Questions

- Count new customers who joined last month
- What is the male to female customer ratio?
- Show total sales for each month in 2023
- Find orders placed by customers in specific cities
- Calculate average order amount by customer gender

## Project Structure

```
.
├── README.md
├── requirements.txt
├── create_database.py    # Database initialization script
├── app.py               # Main Streamlit application
├── retail_db.sqlite     # SQLite database file
└── .env                # Environment variables (create this file)
```

## Notes

- The application uses SQLite for database operations
- Date formats should be in 'YYYY-MM-DD'
- Gender values are 'M' for male and 'F' for female
- Order status can be either 'completed' or 'pending'

## Troubleshooting

1. If you encounter database errors:
   - Ensure the database is created by running `create_database.py`
   - Check if the database file has proper permissions

2. If the API key isn't working:
   - Verify the `.env` file exists and contains the correct API key
   - Ensure the API key has access to Gemini AI services

3. For connection issues:
   - Check if all required packages are installed correctly
   - Verify your internet connection (required for Gemini AI)