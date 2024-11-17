from fastapi import FastAPI

from auth import routes as auth_routes
from users import routes as user_routes
from reminder import routes as reminder_routes


app = FastAPI(root_path="/api")


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(reminder_routes.router)
