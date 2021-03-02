from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_item = request.form['task']
        new_task = Todo(task = task_item)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'The task could not be added. Please retry.'        
    else:
        tasks = Todo.query.order_by(Todo.date).all()
        return render_template("index.html", tasks=tasks)

if __name__=="__main__":
    app.run(debug=True)