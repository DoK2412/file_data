import database.sql_requests as sql

from datetime import datetime, timedelta

from response_code import ResponseCode
from typing import Any

from database.connection_db import JobDb
from database.parameter_schemes import FolderGlobal, FolderSubsidiary, FileGlobal


async def create_new_folder(request, newFolderName: str, folderParentName: Any):
    if len(newFolderName) == 0:
        return ResponseCode(2, 'internalError').give_answer(request)
    async with JobDb() as pool:
        check_folder_id = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), folderParentName, None)
        if check_folder_id:
            check_folder = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), newFolderName, check_folder_id['id'])
            if check_folder:
                return ResponseCode(2, 'availabilityFileError').give_answer(request)
            new_folder = await pool.fetchrow(sql.NEW_FOLDER_USER, int(request.cookies['user_id']), newFolderName, check_folder_id['id'])
            if new_folder is not None:
                return ResponseCode(1, 'folderOk').give_answer(request)
            else:
                return ResponseCode(2, 'internalError').give_answer(request)
        else:
            return ResponseCode(2, 'notFolderError').give_answer(request)


async def rename_folder(request, newFolderName: str, outfolderName: str):
    if newFolderName is None or outfolderName is None:
        return ResponseCode(2, 'notParameterError').give_answer(request)
    async with JobDb() as pool:
        check_folder = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), outfolderName, None)
        if check_folder is not None:
            await pool.fetchrow(sql.UPDATA_FOLDER, int(request.cookies['user_id']), newFolderName, outfolderName)
            return ResponseCode(1, 'renameFolderOk').give_answer(request)
        else:
            return ResponseCode(2, 'notFolderError').give_answer(request)


async def get_folder(request):
    all_folder = list()
    glob_folder = dict()

    async with JobDb() as pool:
        user_folder = await pool.fetch(sql.GET_USER_FOLDER_MAIN, int(request.cookies['user_id']))
        if user_folder:
            for i_folders in user_folder:
                if i_folders[2] is not glob_folder:
                    folders = FolderGlobal(**i_folders)
                    glob_folder[i_folders[2]] = folders
                folder = await pool.fetch(sql.GET_USER_FOLDER,int(request.cookies['user_id']), i_folders[0])
                if folder:
                    for i_folder in folder:
                        fold = FolderSubsidiary(**i_folder)
                        glob_folder[i_folders[2]].folder_content.append(fold)
                    all_folder.append(glob_folder[i_folders[2]])
                    glob_folder= dict()
                else:
                    return ResponseCode(1, {'folder': glob_folder}).give_answer(request)

                # get_file = await pool.fetch(sql.GET_FILE, int(request.cookies['user_id']), None, i_folders[0])
                # if get_file:
                #     for i_file in get_file:
                #         print(i_file)
                #         file = FileGlobal(**i_file)
                #         # file_list.append(file)
            return ResponseCode(1, {'folder': all_folder}).give_answer(request)

        else:
            return ResponseCode(1, {'folder': all_folder}).give_answer(request)


async def getting_fold(request, id_folder):
    async with JobDb() as pool:
        folder_data = await pool.fetch(sql.GET_USER_FOLDER_ADD, int(request.cookies['user_id']), id_folder)
        if folder_data:
            folders = FolderGlobal(**folder_data[0])
            folder = await pool.fetch(sql.GET_USER_FOLDER, int(request.cookies['user_id']), id_folder)
            if folder:
                for i_folder in folder:
                    fold = FolderSubsidiary(**i_folder)
                    folders.folder_content.append(fold)
            get_file = await pool.fetch(sql.GET_FILE, int(request.cookies['user_id']), None, id_folder)
            if get_file:
                file_list = list()
                for i_file in get_file:
                    file = FileGlobal(**i_file)
                    file_list.append(file)
                folders.file_content.append(file_list)
            return ResponseCode(1, {'folder': [folders]}).give_answer(request)
        else:
            return ResponseCode(1, {'folder': []}).give_answer(request)


async def delet_folder(request, id_folder: int):
    try:
        list_folder = list()
        list_id_file = list()
        new_time = datetime.now() + timedelta(seconds=2592000)

        async def check_folder(id: int):
            file_id_list = await id_file_in_folder(int(request.cookies['user_id']), id)
            list_id_file.extend(file_id_list)
            folder_nested = await pool.fetch(sql.GET_USER_FOLDER, int(request.cookies['user_id']), id)
            if folder_nested is not None:
                for i_folder in folder_nested:
                    list_folder.append(i_folder['id'])
                    await check_folder(i_folder['id'])

        async def id_file_in_folder(id_folder, id_user):
            list_id_file = list()
            async with JobDb() as pool:
                file_id = await pool.fetch(sql.CHECK_ID_FILE,id_folder, id_user)
                if file_id:
                    for i_file in file_id:
                        list_id_file.append(i_file['id'])
            return list_id_file

        async with JobDb() as pool:
            folder = await pool.fetch(sql.GET_USER_FOLDER_ADD, int(request.cookies['user_id']), id_folder)
            if len(folder) > 0:
                list_folder.append(folder[0]['id'])
                file_id_list = await id_file_in_folder(int(request.cookies['user_id']), folder[0]['id'])
                list_id_file.extend(file_id_list)
                folder_nested = await pool.fetch(sql.GET_USER_FOLDER, int(request.cookies['user_id']), id_folder)
                if folder_nested is not None:
                    for i_folder in folder_nested:
                        list_folder.append(i_folder['id'])
                        await check_folder(i_folder['id'])
            else:
                return ResponseCode(2, 'notFolderError').give_answer(request)

            for i_delete in list_folder:
                await pool.fetch(sql.UPDATA_DELETE_FOLDER, True, new_time, i_delete)
            for i_file in list_id_file:
                await pool.fetch(sql.DELETE_USER_FILE, i_file, int(request.cookies['user_id']), True, new_time)

            return ResponseCode(1)
    except Exception as exc:
        return ResponseCode(2, 'internalError').give_answer(request)


async def add_file(request, file_name, content, folder_name):
    try:
        now_date = datetime.now()

        async with JobDb() as pool:
            id_folder = (await pool.fetch(sql.GET_FOLDER_ID_NAME, int(request.cookies['user_id']), folder_name))[0]['id']
            if id_folder:
                check_file = await pool.fetch(sql.CHECK_FILE, file_name, int(request.cookies['user_id']), None)
                if check_file:
                    return ResponseCode(2, 'availabilityFileError').give_answer(request)
                else:
                    await pool.fetch(sql.NEW_FILE_USER, int(request.cookies['user_id']), id_folder, file_name, now_date, content)
                    return ResponseCode(1, 'fileOk').give_answer(request)
            else:
                return ResponseCode(2, 'notFolderError').give_answer(request)
    except Exception as exp:
        return ResponseCode(2, 'internalError').give_answer(request)


async def rename_files(request, new_file_name, out_file_name):
    async with JobDb() as pool:
        id_folder = (await pool.fetch(sql.CHECK_FILE, out_file_name, int(request.cookies['user_id']), None))
        if len(id_folder) > 0:
            await pool.fetch(sql.UPDATA_NAME_FILE, new_file_name, id_folder[0]['id'])
            return ResponseCode(1, 'renameFileOk').give_answer(request)
        else:
            return ResponseCode(2, 'notFileError').give_answer(request)


async def delete_files(request, id_file):
    new_data = datetime.now()

    async with JobDb() as pool:
        check_file = await pool.fetch(sql.CHECK_FILE, None, int(request.cookies['user_id']), id_file)
        if check_file:
            await pool.fetch(sql.DELETE_USER_FILE, id_file, int(request.cookies['user_id']), True, new_data)
            return ResponseCode(1, 'deleteFileOk').give_answer(request)
        else:
            return ResponseCode(2, 'notFileError').give_answer(request)


async def get_fil(request, id_file):
    async with JobDb() as pool:
        get_file = await pool.fetch(sql.GET_FILE, int(request.cookies['user_id']), id_file, None)
        if get_file:
            file = FileGlobal(**get_file[0])
            return ResponseCode(1, file).give_answer(request)
        else:
            return ResponseCode(1, []).give_answer(request)


async def get_file_folder_all(request, id_folder):
    file_list = list()
    async with JobDb() as pool:
        get_file = await pool.fetch(sql.GET_FILE, int(request.cookies['user_id']), None, id_folder)
        if get_file:
            for i_file in get_file:
                file = FileGlobal(**i_file)
                file_list.append(file)
            return ResponseCode(1, file_list).give_answer(request)
        else:
            return ResponseCode(1, []).give_answer(request)


async def updata_content_file(request, content, id_file, id_folder):
    try:
        async with JobDb() as pool:
            await pool.fetch(sql.UPDATA_CONTENT_FILE,content, int(request.cookies['user_id']), id_folder, id_file)
            return ResponseCode(1, 'updateСontentFileOK').give_answer(request)
    except Exception as exc:
        return ResponseCode(2, 'internalError').give_answer(request)

