from flask import Flask, render_template, redirect, url_for,request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
	conexion = sqlite3.connect("databases/task.db")
	cursor = conexion.cursor()
	tasks = cursor.execute("SELECT * FROM tasks").fetchall()
	conexion.close()
	return render_template('index.html', tareas = tasks)


@app.route('/create-task', methods= ['POST'])
def create():
	if request.method == 'POST':
		content = request.form['content']
		conexion = sqlite3.connect("databases/task.db")
		cursor = conexion.cursor()
		cursor.execute("INSERT INTO tasks VALUES (null, '{}', 0)".format(content))
		conexion.commit()
		conexion.close()
		return redirect(url_for('home'))

@app.route("/done/<id>")
def done(id):
	conexion = sqlite3.connect("databases/task.db")
	cursor = conexion.cursor()
	bo = cursor.execute("SELECT * FROM tasks WHERE id={}".format(id)).fetchone()[2]
	conexion.close()
	if bo == 1:
		bo = 0
	else:
		bo =1
	conexion = sqlite3.connect("databases/task.db")
	cursor = conexion.cursor()
	cursor.execute("UPDATE tasks SET done={} WHERE id={}".format(bo,id))
	conexion.commit()
	conexion.close()
	return redirect(url_for('home'))


@app.route("/delete/<id>")
def delete(id):
	conexion = sqlite3.connect("databases/task.db")
	cursor = conexion.cursor()
	cursor.execute("DELETE FROM tasks WHERE id={}".format(id))
	conexion.commit()
	conexion.close()
	return redirect(url_for('home'))



if __name__ == '__main__':
	app.run(port =3000, debug= True)
