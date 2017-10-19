import random

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import Form
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY']='very hard to guess string'
bootstrap = Bootstrap(app)


class GuessNumberForm(Form):
    number = IntegerField(u'输入数字（0-1000）：', validators=[DataRequired(u'输入一个有效数字'),
                                                        NumberRange(0, 1000, u'请输入0~1000以内的数字！')])
    submit = SubmitField(u'提交')


@app.route('/')
def index():
    session['number'] = random.randint(0,1000)
    session['times'] = 2
    return render_template('index.html')


@app.route('/guess', methods=['GET','POST'])
def guess():
    times = session['times']
    result = session.get('number')
    form = GuessNumberForm()
    answer = form.number.data
    if form.validate_on_submit():
        times -= 1
        session['times'] = times
        if times == 0:
            flash(u'你输了..wawawa')
            return redirect(url_for('index'))
        elif answer > result:
            flash(u'太大了，你还剩下%s次机会' %times)
        elif answer < result:
            flash(u'太小了，你还剩下%s次机会' %times)
        else:
            flash(u'you win')
            return redirect(url_for('index'))
        return redirect(url_for('guess'))
    return render_template('guess.html', form=form)


if __name__ == '__main__':
    app.run()