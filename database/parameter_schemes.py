from pydantic import BaseModel

from fastapi import Query
from typing  import Any


class DataBase(BaseModel):
    """
    Конфигурация Базы Данных
    """
    user: str
    password: str
    db_name: str
    host: str
    port: int


class Config(BaseModel):
    DataBase: DataBase


class Folder(BaseModel):
    newFolderName: str = Query(description='Название папки')
    folderParentName: Any = Query(default=None, description='Название родительной папки')


class FolderRename(BaseModel):
    newFolderName: str = Query(description='Новое название папки')
    outFolderName: str = Query(description='Старое название папки')
