from flask import Flask
import psycopg2
import os
 
app = Flask(__name__)
 
@app.route("/")
def home():
	return "Infrastructure Automation Demo"
 
@app.route("/health")
def health():
	return "ok"
 
@app.route("/db")
def db_test():
	try:
		conn = psycopg2.connect(
    		host=os.environ.get("DB_HOST"),
    		database=os.environ.get("DB_NAME"),
    		user=os.environ.get("DB_USER"),
   			password=os.environ.get("DB_PASS")
		)
		conn.close()
		return "database connection successful"
	except Exception as e:
		return str(e)
 
@app.route("/transaction")
def transaction_test():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
        cur = conn.cursor()
 
        # insert hardcoded value
        cur.execute(
            "INSERT INTO messages (content) VALUES (%s)",
            ("deployment_success",)
        )
 
        # read newest value
        cur.execute(
            "SELECT id, content FROM messages ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
 
        conn.commit()
        cur.close()
        conn.close()
 
        return f"Inserted + Read -> {row[0]} : {row[1]}"
 
    except Exception as e:
        return str(e)
 
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
