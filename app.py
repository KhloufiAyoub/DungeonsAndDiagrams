import psycopg, re, hashlib
from flask import Flask, render_template, request, jsonify, session, send_file
from datetime import datetime

app = Flask(__name__)
app.secret_key = "cruipi72failou"

conn = psycopg.connect(
    "dbname=py2501 user=py2501 password=cruipi72failou host=student.endor.be port=5433"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/giveUp')
def giveUp():
    with conn.cursor() as cursor:
        cursor.execute("SELECT lid, name FROM levels")
        levels = cursor.fetchall()

    session["level_id"] = None
    return render_template('levels.html', levels=levels)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
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
            if existing_user[2] == hashlib.sha256(password.encode()).hexdigest():
                session["user_id"] = existing_user[0]
                return render_template('levels.html', levels=levels)
            else:
                return render_template('login.html', error="Le mot de passe est incorrect.")
        else:
            return render_template('login.html', error="")

@app.route('/signup', methods=['POST'])
def signup():
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

        cursor.execute(
            "INSERT INTO usr (login, passwd) VALUES (%s, %s) RETURNING uid",
            (username, hashlib.sha256(password.encode()).hexdigest())
        )
        conn.commit()
    return render_template('login.html')

@app.route('/game', methods=['POST'])
def game():
    if request.method == 'POST':
        session["level_id"] = request.form['level']
        session["start_time"] = datetime.now().timestamp()
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
                return jsonify({"message": "Aucun niveau trouvé"})
    except Exception as e:
        return jsonify({"message": str(e)})

@app.route('/result', methods=['POST'])
def result():
    if not session.get("user_id") or not session.get("level_id"):
        return jsonify({"message": "Utilisateur ou niveau non spécifié"})

    gridsubmit = request.form.get('grid', '').strip()
    if not gridsubmit:
        return jsonify({"message": "Aucune grille soumise"})

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT lvl FROM levels WHERE lid = %s", (session["level_id"],))
            level = cursor.fetchone()
            if not level:
                return jsonify({"message": "Aucun niveau trouvé"})

            if gridsubmit == level[0]:
                end_time = datetime.now().timestamp()
                start_time = session.get("start_time")
                if not start_time:
                    return jsonify({"message": "Temps de départ non défini"})
                completion_time = int(end_time - start_time)

                cursor.execute(
                    "SELECT completion_time FROM scores WHERE uid = %s AND lid = %s",
                    (session["user_id"], session["level_id"])
                )
                existing_score = cursor.fetchone()

                if existing_score:
                    if completion_time < existing_score[0]:
                        cursor.execute(
                            "UPDATE scores SET completion_time = %s WHERE uid = %s AND lid = %s",
                            (completion_time, session["user_id"], session["level_id"])
                        )
                        conn.commit()
                        return jsonify({"message": "Score mis à jour avec un meilleur temps"})
                    else:
                        return jsonify({"message": "Niveau accompli, mais le temps n'est pas meilleur"})
                else:
                    cursor.execute(
                        "INSERT INTO scores (uid, lid, completion_time) VALUES (%s, %s, %s)",
                        (session["user_id"], session["level_id"], completion_time)
                    )
                    conn.commit()
                    return jsonify({"message": "Niveau accompli, score enregistré"})
            else:
                return jsonify({"message": "Mauvaise réponse"})
    except Exception as e:
        return jsonify({"message": str(e)})

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
                LIMIT 10""")
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

@app.route('/level-image/<int:lid>')
def level_image(lid):
    with conn.cursor() as cursor:
        cursor.execute("SELECT completion_time FROM scores WHERE uid = %s AND lid = %s", (session["user_id"], lid))
        score = cursor.fetchone()

        image_path = f"static/img/levels-solved/level-{lid}.png" if score else f"static/img/levels/level-{lid}.png"

        response = send_file(image_path, mimetype='image/png')
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response


if __name__ == '__main__':
    app.run(debug=True)