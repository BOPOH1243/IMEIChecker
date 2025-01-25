import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Whitelist  # Импортируйте модели из вашего модуля

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Создаем движок для тестовой базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем сессию для тестов
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем все таблицы
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_session():
    # Создаем сессию для тестов
    session = SessionLocal()
    yield session  # Позволяет использовать session в тестах
    session.close()

def test_user_creation(test_session):
    # Создание нового пользователя
    new_user = User(name="John Doe")
    test_session.add(new_user)
    test_session.commit()
    test_session.refresh(new_user)

    # Проверяем, что пользователь создан
    assert new_user.id is not None
    assert new_user.name == "John Doe"

def test_whitelist_addition(test_session):
    # Создаем пользователя
    new_user = User(name="Jane Doe")
    test_session.add(new_user)
    test_session.commit()
    test_session.refresh(new_user)

    # Добавляем пользователя в whitelist
    whitelist_entry = Whitelist(user_id=new_user.id)
    test_session.add(whitelist_entry)
    test_session.commit()

    # Проверяем, что пользователь добавлен в whitelist
    assert whitelist_entry.id is not None
    assert whitelist_entry.user_id == new_user.id

def test_is_in_whitelist(test_session):
    # Создаем пользователя
    new_user = User(name="Alice")
    test_session.add(new_user)
    test_session.commit()
    test_session.refresh(new_user)

    # Проверяем, что пользователь не в whitelist
    assert not new_user.is_in_whitelist(test_session)

    # Добавляем пользователя в whitelist
    whitelist_entry = Whitelist(user_id=new_user.id)
    test_session.add(whitelist_entry)
    test_session.commit()

    # Проверяем, что пользователь теперь в whitelist
    assert new_user.is_in_whitelist(test_session)
