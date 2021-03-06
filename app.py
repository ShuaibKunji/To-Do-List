from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    dateTime = db.Column(db.DateTime, default=datetime.now)

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
        tasks = Todo.query.order_by(Todo.id).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delTask = Todo.query.get_or_404(id)

    try:
        db.session.delete(delTask)
        db.session.commit()
        return redirect('/')
    except:
        return 'Task could not be deleted. Please retry.'

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    utask = Todo.query.get_or_404(id)
    if request.method == 'POST':
        if utask.task != request.form['task']:
            utask.task = request.form['task']
            utask.dateTime = datetime.now()

            try:
                db.session.commit()
                return redirect('/')
            except:
                return 'Task could not be updated. Please retry.'
        else:
            return redirect('/')
    else:
        return render_template('update.html', task = utask)

if __name__=="__main__":
    app.run(debug=True)