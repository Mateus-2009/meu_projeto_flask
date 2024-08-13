from app import db, User, app

# Criação de um novo contexto de aplicação
with app.app_context():
    # Criação de todas as tabelas
    db.create_all()

    # Criação de um usuário de teste
    username = "admin"
    password = "senha123"
    admin = User(username=username, password=password)
    db.session.add(admin)
    db.session.commit()

    print(f"Usuário {username} criado com sucesso!")

    