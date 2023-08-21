from fastapi import APIRouter, Request

from database.parameter_schemes import Folder, FolderRename
from service.execution_route import create_new_folder, rename_folder
from response_code import ResponseCode

service_route = APIRouter(
    prefix='/data'
)


@service_route.post('/newFolder')
async def createFolder(request: Request,
                       folder: Folder):
    result = await create_new_folder(request, folder.newFolderName, folder.folderParentName)
    return result


@service_route.post('/renameFolder')
async def renameFolder(request: Request,
                       folder: FolderRename):

    result = await rename_folder(request, folder.newFolderName, folder.outFolderName)
    return result


@service_route.post('/receivingFolder')
async def createFolder(request: Request,
                       file: Folder):
    pass
    # result = await create_folder(file.file)


@service_route.post('/receivingFolderAll')
async def createFolder(request: Request,
                       file: Folder):
    if request.session['moi'] is None:
        return ResponseCode(2)

    # result = await create_new_folder(file.newFolderName, file.folderParentName)