import uvicorn

from fastapi import FastAPI

from service.views import service_route

from database.connection_db import JobDb
from log.descriptionlogger import log_error, log_info
from settings import HOST, PORT
from starlette.middleware.sessions import SessionMiddleware



from service.auxiliary_views import background_folder_deletion as bfd



app = FastAPI()
app.include_router(service_route)

app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")


@app.on_event("startup")
async def on_startup():
    '''Функция подключени базы данных на старте приложения'''
    await JobDb().create_pool()
    await bfd()
    log_info.info('База данных подклюбчена')


@app.on_event('shutdown')
async def shutdown_event():
    '''Функция отключения базы данных по окончанию работы'''
    await JobDb().close_pool()
    log_info.info('База данных отключена')



if __name__ == '__main__':
    uvicorn.run(app,
        host=HOST,
        port=PORT
    )