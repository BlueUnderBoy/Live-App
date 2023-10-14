from tv_app import app
from flask import request, render_template, redirect, session, url_for
from tv_app.models.loregs import User
from tv_app.models.emissions import Show
from tv_app.models.aime import Aime
from datetime import datetime
from tv_app.config.mysqlconnection import connectToMySQL


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id']
    }
    user = User.get_one(data)
    mshows = Show.get_mine(data)
    oshows = Show.get_others(data)
    return render_template('user_page.html', user = user, mshows = mshows, oshows = oshows)

@app.route('/shows/<int:show_id>')
def display(show_id):
    if 'user_id' not in session:
        return redirect('/')
    show = Show.get_one(show_id)
    data = {
        'user_id' : session['user_id'],
        'show_id' : show_id
    }
    user = Show.allinfo(data)
    followers = Aime.gal(data)
    return render_template('showpage.html', show = show, user = user, followers = followers)

@app.route('/create_show')
def addshow():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_fav.html')

@app.route('/addshow', methods=['POST'])
def saveshow():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title' : request.form['title'],
        'network' : request.form['network'],
        'reldate' : request.form['reldate'], 
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    valid = Show.validation_show(data)
    if valid:
        rdate = datetime.strptime(request.form['reldate'], '%Y-%m-%d')
        data['reldate'] = datetime.strftime(rdate, "%B %d, %Y")
        print(data['reldate'])
        Show.save(data)
        return redirect('/dashboard')
    return redirect('/create_show')

@app.route('/like/<int:show_id>')
def favorite(show_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'show_id' : show_id
    }
    count = Aime.user_like(data)
    if count < 1:
        Aime.save(data)
        nlc = Aime.get_likes(data)
        ndata = {
            'show_id' : show_id,
            'likes' : nlc
        }
        Show.ulike(ndata)
    else:
        Aime.deletelike(data)
        ulc = Aime.get_likes(data)
        udata = {
            'show_id' : show_id,
            'likes' : ulc
        }
        Show.ulike(udata)
    return redirect('/dashboard')


@app.route('/shows/update/<int:show_id>')
def update(show_id):
    if 'user_id' not in session:
        return redirect('/') 
    session['show_id'] = show_id
    show = Show.get_one(show_id)
    sd = show.description
    cv = datetime.strptime(show.reldate, '%B %d, %Y')
    sy = datetime.strftime(cv, '%Y-%m-%d')
    return render_template('edit_fav.html', show = show, sy = sy, sd = sd)

@app.route('/shows/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id' : session['show_id'],
        'title' : request.form['title'],
        'network' : request.form['network'],
        'reldate' : request.form['reldate'],
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    valid = Show.validation_show(data)
    if valid: 
        Show.update(data)  
        show = Show.get_one(session['show_id'])
        user = User.get_one(data)
        cv = datetime.strptime(show.reldate, '%Y-%m-%d')
        sy = datetime.strftime(cv, '%B %d, %Y')
        return render_template('showpage.html', show = show, user = user, sy = sy)
    return redirect(url_for('update', show_id = session['show_id']))

@app.route('/shows/delete/<int:show_id>')
def delete(show_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': show_id
    }
    Show.delete(data)
    Aime.deletelike(data)
    Aime.delete(show_id)
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')