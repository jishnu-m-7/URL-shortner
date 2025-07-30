from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use SQLite for demo purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(8), nullable=False)
    re = db.Column(db.String(2048), nullable=False)
    def __repr__(self):
        return f'{self.key}'

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        key=request.form['key']
        re=request.form['re']
        url=URL(key=key,re=re)
        print(url)
        db.session.add(url)
        db.session.commit()
    return render_template('index.html')
    
@app.route('/table')
def table():
    urls=URL.query.all()
    return str(urls)

@app.route('/getUrl/')
@app.route('/getUrl/<key>')
def hello(key=None):
    url=URL.query.filter_by(key=key).first()
    print(url.re)
    if url:
        return redirect(url.re)
    return f"Your key is, {key or 'is invalid'}!"

if __name__ == '__main__':
    app.run(debug=True)