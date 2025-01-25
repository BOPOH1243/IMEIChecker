from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base, SessionLocal, engine

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tg_id = Column(String, nullable=True)
    whitelist = relationship('Whitelist', back_populates='user')

    # Метод для проверки, находится ли пользователь в whitelist
    def is_in_whitelist(self, session: SessionLocal):
        # Проверяем, есть ли у пользователя запись в whitelist
        return session.query(Whitelist).filter(Whitelist.user_id == self.id).first() is not None
    
class Whitelist(Base):
    __tablename__ = 'whitelist'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Вторичный ключ на User
    
    # Связь с User
    user = relationship('User', back_populates='whitelist')

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Пример использования
if __name__ == "__main__":
    # Открытие сессии и выполнение запроса
    with SessionLocal() as session:
        # Пример: проверим, есть ли пользователь с id = 1 в whitelist
        user = session.query(User).filter(User.id == 1).first()
        if user:
            is_in_whitelist = user.is_in_whitelist(session)
            print(f"User with ID {user.id} is {'in' if is_in_whitelist else 'not in'} the whitelist.")
        else:
            print("User not found.")

    print('Все работает корректно')
