# Tool: Look up transaction by ID
import pyodbc
import json
import config
def get_transaction_by_id(transaction_id: str) -> str:
    
    conn_str = config.DB_CONN_STRING
    query = f"EXEC dbo.spGetTransactionDetais '{transaction_id}'"
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            #result = cursor.fetchone()

            columns = [column[0] for column in cursor.description]
            if columns:
            # Fetch rows and convert to list of dictionaries
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                for row in rows:
                    row["amount"] = str(row["amount"])  # Convert amount to string
                
                json_data = json.dumps(rows, indent=4)

                return str(json_data)
            else:
                return "Transaction not found."
    except pyodbc.Error as e:
        print (e)
        return f"An error occurred: {e}"    