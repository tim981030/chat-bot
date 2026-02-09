from flask import Flask,render_template,request
import os
from dotenv import load_dotenv
from bot import GeminiBot
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #建立一個應用 (app)

my_instruction=f"不要使用 Markdown 格式。"

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
bot = GeminiBot(api_key=api_key,system_instruction=my_instruction)

key=int(os.getenv('KEY'))

SECRET_KEY = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)

class q(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    qt = db.Column(db.String, nullable=False)
    a = db.Column(db.String, nullable=False)

link=os.getenv('LINK')
@app.route('/') #'/' 是「根路徑」，定義主頁要顯示的內容 
def talk():
    return render_template('index.html')

@app.route('/question',methods=['POST'])
def submit():
    content=request.form.get('input')
    text="Q: "+content
    response=bot.send_message(content)
    if response=="0":
        return render_template('wrong.html',link=link)
    text+="\n\nA: "+response
    newq=q(num=(q.query.count()+18580928)^key,qt=content,a=response)
    db.session.add(newq)
    db.session.commit()

    return render_template('question.html',text=text,num=(q.query.count()+18580927)^key,link=link)

@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

@app.route('/query',methods=['POST'])
def qry():
    content=request.form.get('query')
    fl=False
    try:
        content=int(content)
        text=q.query.filter_by(num=content).first()
        return render_template('question.html',text=f"Q: {text.qt}\n\nA: {text.a}",num=text.num,link=link)
    except:
        text=q.query.filter(q.qt.ilike(f'%{content}%')).all()
        sum=len(text)
        qtn=[]
        nm=[]
        for i in text:
            qtn.append(i.qt)
            nm.append(i.num)
        return render_template('list.html',list=qtn,num=nm,sum=sum,link=link)
    

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/query',methods=['GET'])
def kw():
    target=request.args.get('num')
    text=q.query.filter_by(num=int(target)).first()
    return render_template('question.html',text=f"Q: {text.qt}\n\nA: {text.a}",num=text.num,link=link)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True,port=10030)

   
