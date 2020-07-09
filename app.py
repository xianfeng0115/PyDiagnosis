from flask import Flask,render_template,request,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
import os,sys
import click
app=Flask(__name__)

@app.route('/test', methods=['GET', 'POST'])
def test():
    a=1
    b=2
    c=a+b
    return render_template('index.html', result=c)
