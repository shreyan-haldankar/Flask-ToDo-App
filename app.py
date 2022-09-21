from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

print("Made by Shreyan Haldankar")

# Creating a model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable= False)
    completed = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime, default = datetime.utcnow )

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content = task_content)


        try:
            # Adding new task to our db session
            db.session.add(new_task)
            # commit
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:

        # Querying the db
        tasks = Todo.query.order_by(Todo.created).all()
        return render_template('index.html', tasks = tasks)
        


@app.route('/delete/<int:id>')
def delete(id):
    # Querying the task to be deleted
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # Deleting the task we want to get deleted from the db
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error while deleting the task"


@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        # Setting the current task's content to the new task content in the input box
        task.content = request.form['content']

        try:
            # Saving the updated task
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error while updating the task"
            
    else:
        return render_template('update.html', task = task)


if __name__ == "__main__":
    app.run(debug=True)
