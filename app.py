import psycopg, re,hashlib
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

conn = psycopg.connect(
    "dbname=py2501 user=py2501 password=cruipi72failou host=student.endor.be port=5433"
)

Glo_Username = " "

cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/game', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            error = 0

            if re.match("/<script/i", username) or re.match("/<script/i", password):
                error+=1

            if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{0,15}$", username) or not re.match(r"^[a-zA-Z][a-zA-Z0-9_]{0,15}$", password):
                error+=1

            if error == 0:
                # Vérifier si le nom d'utilisateur existe déjà dans la table
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM usr WHERE login = %s", (username,))
                    existing_user = cursor.fetchone()

                    if existing_user:
                        # Vérifier si le mot de passe correspond
                        if existing_user[2] == hashlib.sha256(password.encode()).hexdigest():
                            # Rediriger vers une page de succès ou une autre page appropriée
                            return render_template('game.html')
                        else:
                            return render_template('login.html', error="Le mot de passe est incorrect.")
                    else:
                        # Insérer les données dans la base de données
                        cursor.execute("INSERT INTO usr (login,passwd) VALUES (%s, %s)",(username, hashlib.sha256(password.encode()).hexdigest()))
                        conn.commit()

                        cursor.execute("SELECT lvl,hinth,hintv FROM levels WHERE lid = 1")
                        level = cursor.fetchone()
                        return render_template('game.html', level=level[0], hinth=level[1], hintv=level[2])
            else:
                return render_template('login.html', error="Nom d'utilisateur ou mot de passe incorrect.")

    except Exception as e:
        return f"Le problème en question : {str(e)}"

@app.route('/init', methods=['POST'])
def init():
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT lvl, hinth, hintv FROM levels WHERE lid = 1")
            level = cursor.fetchone()
            if level:
                return jsonify(level)
            else:
                return jsonify({"error": "No level found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)