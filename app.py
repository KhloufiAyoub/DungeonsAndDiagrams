import psycopg, re, hashlib
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime  # Pour gérer les timestamps

app = Flask(__name__)
app.secret_key = "cruipi72failou"

conn = psycopg.connect(
    "dbname=py2501 user=py2501 password=cruipi72failou host=student.endor.be port=5433"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submitlogin', methods=['POST'])
def submitlogin():
    session["level_id"] = None
    session["user_id"] = None
    username = request.form['username']
    password = request.form['password']

    with conn.cursor() as cursor1:
        cursor1.execute("SELECT lid, name FROM levels")
        levels = cursor1.fetchall()

    with conn.cursor() as cursor:
        cursor.execute("SELECT uid, login, passwd FROM usr WHERE login = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Vérifier le mot de passe
            if existing_user[2] == hashlib.sha256(password.encode()).hexdigest():
                session["user_id"] = existing_user[0]
                return render_template('levels.html', levels=levels)
            else:
                return render_template('login.html', error="Le mot de passe est incorrect.")
        else:
            return render_template('login.html', error="L'utilisateur n'existe pas.")

@app.route('/submitregister', methods=['POST'])
def submitregister():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if re.match("/<script/i", username) or re.match("/<script/i", password):
        return render_template('register.html', error="")

    if confirm_password != password:
        return render_template('register.html', error="Les mots de passe ne correspondent pas.")

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9]{1,15}$", username) or not re.match(r"^[a-zA-Z][a-zA-Z0-9]{1,15}$", password):
        return render_template('register.html', error="Non respect des règles de nom d'utilisateur ou de mot de passe.")

    with conn.cursor() as cursor:
        cursor.execute("SELECT uid FROM usr WHERE login = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('register.html', error="Cet utilisateur existe déjà.")

        # Insérer un nouvel utilisateur
        cursor.execute(
            "INSERT INTO usr (login, passwd) VALUES (%s, %s) RETURNING uid",
            (username, hashlib.sha256(password.encode()).hexdigest())
        )
        session["user_id"] = cursor.fetchone()[0]
        conn.commit()
    return render_template('login.html')

@app.route('/game', methods=['POST'])
def game():
    if request.method == 'POST':
        session["level_id"] = request.form['level']
        session["start_time"] = datetime.now().timestamp()  # Enregistrer le temps de début
        return render_template('game.html')

@app.route('/init', methods=['POST'])
def init():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT lvl, hinth, hintv, lid, name FROM levels WHERE lid = %s",
                (session["level_id"],)
            )
            level = cursor.fetchone()
            if level:
                return jsonify(level)
            else:
                return jsonify({"message": "No level found"})
    except Exception as e:
        return jsonify({"message": str(e)})

@app.route('/submitlvl', methods=['POST'])
def submitlvl():
    if request.method == 'POST':
        gridsubmit = request.form['grid']
        with conn.cursor() as cursor:
            cursor.execute("SELECT lvl FROM levels WHERE lid = %s", (session["level_id"],))
            level = cursor.fetchone()
            if level:
                if gridsubmit == level[0]:
                    # Calculer le temps écoulé
                    end_time = datetime.now().timestamp()
                    start_time = session.get("start_time")
                    if start_time:
                        completion_time = int(end_time - start_time)
                        # Enregistrer le score
                        cursor.execute(
                            "INSERT INTO scores (uid, lid, completion_time) VALUES (%s, %s, %s)",
                            (session["user_id"], session["level_id"], completion_time)
                        )
                        conn.commit()
                    return jsonify({"message": "Level completed"})
                else:
                    return jsonify({"message": "Incorrect answer"})
            else:
                return jsonify({"message": "No level found"})

@app.route('/levels')
def levels():
    with conn.cursor() as cursor:
        cursor.execute("SELECT lid, name FROM levels")
        levels = cursor.fetchall()
        return render_template('levels.html', levels=levels)

@app.route('/scores')
def global_scores():
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.login, COUNT(s.sid) as levels_solved, AVG(s.completion_time) as avg_time
                FROM usr u
                LEFT JOIN scores s ON u.uid = s.uid
                GROUP BY u.uid, u.login
                ORDER BY levels_solved DESC, avg_time
                LIMIT 10
            """)
            global_scores = cursor.fetchall()
            return render_template('scores.html', scores=global_scores, level_name=None)
    except Exception as e:
        return render_template('scores.html', error=str(e), scores=[], level_name=None)

@app.route('/scores/<int:lid>')
def level_scores(lid):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM levels WHERE lid = %s", (lid,))
            level_name = cursor.fetchone()
            if not level_name:
                return render_template('scores.html', error="Niveau non trouvé", scores=[], level_name=None)
            level_name = level_name[0]
            cursor.execute("""
                SELECT u.login, s.completion_time
                FROM usr u
                JOIN scores s ON u.uid = s.uid
                WHERE s.lid = %s
                ORDER BY s.completion_time
                LIMIT 10
            """, (lid,))
            level_scores = cursor.fetchall()
            return render_template('scores.html', scores=level_scores, level_name=level_name)
    except Exception as e:
        return render_template('scores.html', error=str(e), scores=[], level_name=None)

if __name__ == '__main__':
    app.run(debug=True)