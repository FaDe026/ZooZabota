from sqlalchemy import select
from src.models.user import UserModel
from src.database import async_sessionmaker, engine
from src.utils.hashing import get_password_hash

async def create_admin_user():
    async with engine.begin() as conn:
        session = async_sessionmaker(bind=conn)()
        try:
            result = await session.execute(
                select(UserModel).where(UserModel.username == "admin")
            )
            existing_user = result.scalar_one_or_none()

            if not existing_user:
                admin = UserModel(
                    username="admin",
                    password=get_password_hash("admin"),
                    email="admin@example.com",
                    role="Admin"
                )
                session.add(admin)
                await session.commit()
                print("Пользователь 'admin' создан.")
            else:
                print("ℹПользователь 'admin' уже существует.")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании админа: {e}")
        finally:
            await session.close()