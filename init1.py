from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
from datetime import date
#from app import app


###Initialize the app from Flask
app = Flask(__name__)
##app.secret_key = "secret key"

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='fatear',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s and pwd = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['firstname']
    lname = request.form['lastname']
    nname = request.form['nickname']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, NULL, %s)'
        cursor.execute(ins, (username, password, fname, lname, nname))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor()
    
    query = '''SELECT username, title, reviewText, reviewDate
            FROM reviewSong NATURAL JOIN song
            WHERE reviewDate > (SELECT lastlogin FROM user WHERE username = %s)
            AND username IN ( SELECT u.username
                            FROM user u
                            INNER JOIN friend f ON (u.username = f.user1 OR u.username = f.user2)
                            WHERE (f.user1 = %s OR f.user2 = %s)
                            AND f.acceptStatus = 'Accepted'
                            AND u.username != %s)
            OR username IN ( SELECT u.username
                            FROM user u
                            INNER JOIN follows f ON u.username = f.follows
                            WHERE f.follower = %s);'''
    cursor.execute(query, (user, user, user, user, user))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=user, posts=data)

@app.route('/newsong')
def newsong():
    user = session['username']
    cursor = conn.cursor()
    
    query = '''SELECT CONCAT(a.fname , ' ' , a.lname) AS name, s.title, s.releaseDate
                FROM artist a
                NATURAL JOIN artistperformssong p
                NATURAL JOIN song s
                WHERE s.releaseDate > (SELECT lastlogin FROM user WHERE username = %s)
                AND artistID IN (SELECT artistID FROM userfanofartist
                                WHERE username = %s);'''
    cursor.execute(query, (user, user))
    data = cursor.fetchall()
    cursor.close()
    return render_template('newsong.html', username=user, new_song=data)

        
@app.route('/post_review', methods=['GET', 'POST'])
def post_review():
    username = session['username']
    title = request.form.get('title1')
    review = request.form.get('review')
    datenow = date.today()
    cursor = conn.cursor()
    query = '''INSERT INTO reviewsong 
                VALUES(%s, (SELECT songID FROM song s WHERE s.title = %s), %s, %s);'''
    cursor.execute(query, (username, title, review, datenow))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/post_rating', methods=['GET', 'POST'])
def post_rating():
    username = session['username']
    title = request.form.get('title2')
    rating = request.form.get('rating')
    datenow = date.today()
    cursor = conn.cursor()
    query = '''INSERT INTO ratesong
                VALUES(%s, (SELECT songID FROM song s WHERE s.title = %s), %s, %s);'''
    cursor.execute(query, (username, title, rating, datenow))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/select_genre', methods=["GET", "POST"])
def select_genre():
    genre = request.form['genre']
    cursor = conn.cursor()
    query = ''' SELECT s.title, AVG(rs.stars) as avg_rating
                FROM song s
                INNER JOIN songGenre sg ON s.songID = sg.songID
                LEFT JOIN rateSong rs ON s.songID = rs.songID
                WHERE sg.genre = %s
                GROUP BY s.title
                ORDER BY avg_rating DESC;'''
    cursor.execute(query, (genre))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('select_song.html', song_list=data)
    else:
        #returns an error message to the html page
        error = 'Genre does not exist'
        return render_template('home.html', error=error)

@app.route('/select_artist', methods=["GET", "POST"])
def select_artist():
    artist = request.form['artist']
    cursor = conn.cursor()
    query = ''' SELECT s.title, CONCAT(fname , ' ' , lname) AS name
                FROM song s
                JOIN artistperformssong AS p ON s.songID = p.songID
                JOIN artist a ON a.artistID = p.artistID
                WHERE CONCAT(fname , ' ' , lname) = %s;'''
    cursor.execute(query, (artist))
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('select_song.html', song_list=data)
    else:
        #returns an error message to the html page
        error = 'Artist does not exist'
        return render_template('home.html', error=error)

@app.route('/show_review', methods=["GET", "POST"])
def show_review():
    title = request.form.get('songtitle')
    cursor = conn.cursor()
    query = '''SELECT re.username, re.reviewText, re.reviewDate
                FROM song s
                JOIN reviewsong re ON s.songID = re.songID
                WHERE s.title = %s;'''
    cursor.execute(query, title)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_review.html', song_title=title, reviews=data)

@app.route('/select_user', methods=["GET", "POST"])
def select_user():
    cursor = conn.cursor()
    query = 'SELECT username FROM user;'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    error = None
    if(data):
        return render_template('select_user.html', user_list=data)
    else:
        #returns an error message to the html page
        error = 'Can find users'
        return render_template('home.html', error=error)

@app.route('/show_user', methods=["GET", "POST"])
def show_user():
    username = request.form.get('username')
    return render_template('show_user.html', user=username)

@app.route('/show_friend', methods=["GET", "POST"])
def show_friend():
    username = request.form.get('username')
    cursor = conn.cursor()
    query = '''SELECT u.username, u.fname, u.lname
                FROM user u
                INNER JOIN friend f ON (u.username = f.user1 OR u.username = f.user2)
                WHERE (f.user1 = %s OR f.user2 = %s)
                AND f.acceptStatus = 'Accepted'
                AND u.username != %s;'''
    cursor.execute(query, (username,username,username))
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_friend.html', user=username, friends=data)

@app.route('/show_follower', methods=["GET", "POST"])
def show_follower():
    username = request.form.get('username')
    cursor = conn.cursor()
    query = '''SELECT u.username, u.fname, u.lname
                FROM user u
                INNER JOIN follows f ON u.username = f.follower
                WHERE f.follows = %s;'''
    cursor.execute(query, username)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_follower.html', user=username, followers=data)

@app.route('/show_follow', methods=["GET", "POST"])
def show_follow():
    username = request.form.get('username')
    cursor = conn.cursor()
    query = '''SELECT u.username, u.fname, u.lname
                FROM user u
                INNER JOIN follows f ON u.username = f.follows
                WHERE f.follower = %s;'''
    cursor.execute(query, username)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_follow.html', user=username, follows=data)

@app.route('/show_user_review', methods=["GET", "POST"])
def show_user_review():
    username = request.form.get('username')
    cursor = conn.cursor()
    query = '''SELECT s.title, r.reviewText, r.reviewDate
                FROM song s
                JOIN reviewsong r ON s.songID = r.songID
                WHERE username = %s;'''
    cursor.execute(query, username)
    data = cursor.fetchall()
    cursor.close()
    return render_template('user_review.html', user=username, posts=data)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
