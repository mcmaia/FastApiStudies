from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users

app = FastAPI()

teste = Base.metadata.create_all(bind=engine)
print(teste)

# @app.get("/healthy")
# def healthy_check():
#     return{'status': 'Healthy'}


# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)
