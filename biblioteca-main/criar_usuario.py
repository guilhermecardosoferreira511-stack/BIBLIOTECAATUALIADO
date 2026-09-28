# criar_usuario.py
from app import create_app
from app.models.user import get_user_by_username, create_user

app = create_app()

with app.app_context():
    # Verifica se o utilizador já existe usando SQL puro
    if not get_user_by_username("admin"):
        create_user("admin", "123456")
        print("Utilizador 'admin' criado com sucesso via SQL puro!")
    else:
        print("O utilizador 'admin' já existe no banco de dados.")