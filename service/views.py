from fastapi import APIRouter, Request, Query, Response

from database.parameter_schemes import Folder, FolderRename, AddNewFile, FileRename, UpdataContent
from service.execution_route import create_new_folder, rename_folder, get_folder, getting_fold, delet_folder, add_file, rename_files, delete_files, get_fil, get_file_folder_all, updata_content_file
from response_code import ResponseCode

service_route = APIRouter(
    prefix='/data'
)


@service_route.post('/newFolder')
async def createFolder(request: Request,
                       folder: Folder):
    """
        Функция создания новой папки пользователя
    """
    try:
        result = await create_new_folder(request, folder.newFolderName, folder.folderParentName)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)


@service_route.post('/renameFolder')
async def renameFolder(request: Request,
                       folder: FolderRename):
    """
        Функция переименования папки пользователя
    """
    try:
        result = await rename_folder(request, folder.newFolderName, folder.outFolderName)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.get('/getFolderParent')
async def getting_folders(request: Request):
    """
        Функция получения родительных папок пользователя
    """
    # try:
    result = await get_folder(request)
    return result
    # except Exception as exc:
    #     # log_error.error(f'При выполнении произошла ошибка {exc}')
    #     return ResponseCode(2, 'internalError').give_answer(request)


@service_route.get('/getFolderNested')
async def getting_folder(request: Request,
                         id_folder: int = Query(None, description="Id необходимой папки")):
    """
        Функция получения дочерник папок пользователя
    """
    try:
        result = await getting_fold(request, id_folder)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)


@service_route.get('/deleteFolder')
async def delete_folder(request: Request,
                         id_folder: int = Query(None, description="Id удаляемой папки")):
    """
        Функция удаления папки пользователя
    """
    try:
        result = await delet_folder(request, id_folder)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)


@service_route.post('/addNewFile')
async def add_new_file(request: Request,
                       addFile: AddNewFile):
    """
        Функция добавления файла пользователем
    """
    try:
        result = await add_file(request, addFile.fileName, addFile.content, addFile.folderName)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.post('/renameFile')
async def rename_file(request: Request,
                   renameFales: FileRename):
    try:
        result = await rename_files(request, renameFales.newFileName, renameFales.outFileName)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.get('/deleteFile', tags=['file_data'])
async def rename_file(request: Request,
                      id_file: int = Query(None, description="Id удаляемого файла")):
    try:
        result = await delete_files(request, id_file)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.get('/getFile', tags=['file_data'])
async def get_file(request: Request,
                   id_file: int = Query(None, description="Id необходимого файла")):
    try:
        result = await get_fil(request, id_file)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.get('/getFileFplder', tags=['file_data'])
async def get_file_folder(request: Request,
                          id_folder: int = Query(None, description="Id необходимой папки")):
    try:
        result = await get_file_folder_all(request, id_folder)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)



@service_route.post('/apdataContentFile', tags=['file_data'])
async def get_file_folder(request: Request,
                          content: UpdataContent):
    try:
        result = await updata_content_file(request, content.content, content.id_file, content.id_folder)
        return result
    except Exception as exc:
        # log_error.error(f'При выполнении произошла ошибка {exc}')
        return ResponseCode(2, 'internalError').give_answer(request)
