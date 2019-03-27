import os

from flask import Flask,render_template,redirect,url_for

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField ,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_bootstrap import Bootstrap 

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)#creating a flask instance
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" +os.path.join(basedir,"python.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS ']= False
app.config['SECRET_KEY']="siriyangu"
bootsrap = Bootstrap(app)


db = SQLAlchemy(app)

class PythonCourse(db.Model):#this is a table
	__tablename__= 'python_courses'
	id =  db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(50))
	sub_title =db.Column(db.String(100))
	content = db.Column(db.Text())
	author = db.Column(db.String(20))





class CourseForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(),Length(min=5,max=30)])
	sub_title = StringField('Subtitle',validators=[DataRequired(),Length(min=5,max=30)])
	content = TextAreaField('Content',validators=[DataRequired()])
	author = StringField('Author',validators=[DataRequired(),Length(min=5,max=30)])
	submit = SubmitField('Submit')







	


#home route(localhost:5000)
@app.route('/',methods = ['GET','POST'])
def home():
	form = CourseForm()#iinitializing the courseform
	if form.validate_on_submit():#validating user input

		#Grabbing form data from the user
		title = form.title.data
		sub_title = form.sub_title.data
		author = form.author.data
		content = form.content.data

		#Creating PythonCourse objects/Instance
		#This new_course object stores the data from the form into the database tables
		new_course = PythonCourse(title=title,sub_title=sub_title,author=author,content=content) #this is creation of datatable

		#adding the new_course into the database
		db.session.add(new_course)

		#saving data into the database
		db.session.commit()
		#if successful return the user to the homepage
		return redirect(url_for('home'))

	py_courses = PythonCourse.query.all()

	return render_template('home.html',title='Home Page',courses=py_courses,form=form)

#python route(localhost:5000/python)
@app.route('/python')
def python():
	
	return render_template('python.html', name = 'winnie', title='Python page')

#
#python route(localhost:5000/python/functions)
@app.route('/python/functions')
def functions():
	return render_template('functions.html',title ='Function Page')


@app.route('/python/classes')
def classes():
	return render_template('classes.html', title='Classes Page')

@app.route('/python/<name>')
def intel(name):
	return 'hello ' + name


@app.route('/python/integer/<int:number>')
def nambari(number):
	return 'The number is ' + str(number)























@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'),500



















if __name__ == "__main__":
	app.run(debug = True,port=3000)
