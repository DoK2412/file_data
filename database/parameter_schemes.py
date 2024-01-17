from pydantic import BaseModel
from datetime import datetime

from fastapi import Query
from typing  import Any, Optional


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


class FolderGlobal(BaseModel):
    id: int
    folder_name: str
    folder_content: Optional[list] = []
    file_content: Optional[list] = []

class FolderSubsidiary(BaseModel):
    id: int
    folder_name: str


class AddNewFile(BaseModel):
    fileName:  str = Query(description='Названия файла')
    content:  str = Query(description='Наполнение файла')
    folderName: str = Query(description='Название папки сохранения')


class FileRename(BaseModel):
    newFileName: str = Query(description='Новое название файла')
    outFileName: str = Query(description='Старое название файла')


class FileGlobal(BaseModel):
    id: int
    id_folder: int
    file_name: str
    date_delete:  Optional[datetime]
    content: str


class UpdataContent(BaseModel):
    id_file: int = Query(description='Id необходимого файла')
    id_folder: int = Query(description='Id необходимой папки')
    content: str = Query(description='Обновление содержимого файла')
