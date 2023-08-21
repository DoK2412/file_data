
from response_code import ResponseCode
from typing import Any

from database.connection_db import JobDb
import database.sql_requests as sql


async def create_new_folder(request, newFolderName: str, folderParentName: Any):
    if len(newFolderName) == 0:
        return ResponseCode(4)
    async with JobDb() as pool:
        check_folder_id = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), folderParentName, None)
        check_folder = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), newFolderName, check_folder_id['id'])
        if check_folder:
            return ResponseCode(11)
        new_folder = await pool.fetchrow(sql.NEW_FOLDER_USER, int(request.cookies['user_id']), newFolderName, check_folder_id['id'])
        if new_folder is not None:
            return ResponseCode(1)
        else:
            return ResponseCode(2)


async def rename_folder(request, newFolderName: str, outfolderName: str):
    if newFolderName is None or outfolderName is None:
        return ResponseCode(4)
    async with JobDb() as pool:
        check_folder = await pool.fetchrow(sql.CHECK_FOLDER, int(request.cookies['user_id']), outfolderName, None)
        if check_folder is not None:
            rename = await pool.fetchrow(sql.UPDATA_FOLDER, int(request.cookies['user_id']), newFolderName, outfolderName)
            return ResponseCode(1)
        else:
            return ResponseCode(10)









