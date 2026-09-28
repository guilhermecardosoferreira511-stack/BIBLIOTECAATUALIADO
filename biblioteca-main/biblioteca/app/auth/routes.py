# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.user import get_user_by_username, check_user_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Procura o utilizador via SQL puro (DQL)
        user = get_user_by_username(username)

        # Valida as credenciais
        if user and check_user_password(user["password_hash"], password):
            session["usuario_logado"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("main.index"))
        else:
            erro = "Utilizador ou palavra-passe inválidos."

    return render_template("login.html", erro=erro)


@auth_bp.route("/welcome")
def welcome():
    if "usuario_logado" not in session:
        return redirect(url_for("auth.login"))
    return render_template("welcome.html", usuario=session.get("username"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))