#pip install flask-cors
from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL
from flask_cors import CORS 

mysql = MySQL()
app = Flask(__name__)
CORS(app)
app.config['MYSQL_DATABASE_USER'] = 'emp_user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x'
app.config['MYSQL_DATABASE_DB'] = 'sakila'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)

conn = mysql.connect()

cursor = conn.cursor()

@app.route('/api')
def customers():
	query = "SELECT CONCAT(customer.first_name, ' ', customer.last_name), address, city, `zip code`, SUM(payment.amount), CONCAT(staff.first_name, ' ', staff.last_name) FROM (((customer LEFT JOIN customer_list ON customer.customer_id=customer_list.ID) INNER JOIN payment ON customer.customer_id=payment.customer_id) INNER JOIN staff ON customer.store_id = staff.store_id) WHERE customer.store_id = 1 GROUP BY payment.customer_id, customer.first_name, customer.last_name, staff.first_name, staff.last_name"

	cursor.execute(query)
	data = cursor.fetchall()
	data_as_list = list(data)
	# result_as_dictionary = dict(map(None, str(*[iter(1)]*2)))
	return jsonify(results = data_as_list)
	# return render_template('customers.html', data = data) 

@app.route('/customers_view')
def customers_view():
	return render_template('customers.html')		

if __name__ == "__main__":
	app.run(debug=True)	