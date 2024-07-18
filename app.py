# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# db=SQLAlchemy(app)


# class todo(db.Model):
#     sno=db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(40),nullable=False)
#     desc=db.Column(db.String(100),nullable=False)
#     date=db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self) -> str:
#         return f"{self.sno} - {self.title}"





# @app.route('/')
# def hello_world():
#     return render_template("index.html")
#     # return 'Hello, World!'


# if __name__== "__main__":
#     app.run(debug=True,port=8000)




from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods =['GET','POST'])
def hello_world():
    if request.method=='POST':
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']
        stodo=todo(title=title, desc=desc)
        db.session.add(stodo)
        db.session.commit()
    alltodo=todo.query.all()
    return render_template("index.html", alltodo=alltodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    stodo=todo.query.filter_by(sno=sno).first()
    db.session.delete(stodo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>', methods =['GET','POST'])
def update(sno):
     if request.method=='POST':
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']
        stodo=todo.query.filter_by(sno=sno).first()
        stodo.title=title
        stodo.desc=desc
        db.session.add(stodo)
        db.session.commit()
        return redirect('/')

        # stodo=todo(title=title, desc=desc)
        
     stodo=todo.query.filter_by(sno=sno).first()
     return render_template("update.html", stodo=stodo)

   
       
        

if __name__ == "__main__":
    # Ensure to run within the application context
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
