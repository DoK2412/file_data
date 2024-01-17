SHECK_USER_ID = '''
--получение id пользователя
SELECT profile_id 
FROM sessions
WHERE 
CASE WHEN bool($1::varchar is not null) THEN sessions.uid = $1::varchar ELSE true END
'''

NEW_FOLDER_USER = '''
--создание новой папки для пользователя
INSERT INTO user_folder 
    (profile_id, folder_name, folder_parent)
VALUES 
    ($1, $2, $3)
RETURNING id
'''

CHECK_FOLDER = '''
-- проверка наличия папки в папке
SELECT id FROM user_folder 
    WHERE 
CASE WHEN bool($1::int is not null) THEN profile_id = $1::int ELSE true END
AND CASE WHEN bool($2::varchar is not null) THEN folder_name = $2::varchar ELSE true END
AND CASE WHEN bool($3::int is not null) THEN folder_parent = $3::int ELSE true END
'''

UPDATA_FOLDER = '''
--обновление имени папки
UPDATE user_folder SET folder_name =$2 WHERE folder_name = $3 and  profile_id = $1 RETURNING id
'''

UPDATA_FOLDER_PARENT = '''
--обновление имени папки
UPDATE user_folder SET folder_parent = $2 WHERE folder_parent = $3 and  profile_id = $1 RETURNING id
'''

GET_USER_FOLDER_MAIN = '''
--получения списка папок пользователя
SELECT * FROM user_folder WHERE profile_id = $1 and folder_parent is null 
'''

GET_USER_FOLDER = '''
--получения списка папок пользователя
SELECT * FROM user_folder WHERE profile_id = $1 and folder_parent = $2
'''

GET_USER_FOLDER_ADD = '''
--получения списка папок пользователя
SELECT * FROM user_folder WHERE profile_id = $1 and id = $2
'''

UPDATA_DELETE_FOLDER = '''
-- установка таймера для удаления папки
UPDATE  user_folder SET active_delete = $1, date_delete = $2 WHERE id = $3
'''

SELECT_DELEDE_FOLDER = '''
-- получение удаляемых папок
SELECT * FROM user_folder WHERE active_delete IS TRUE
'''

DELETE_USER_FOLDER = '''
--окончательное удаление папок
DELETE FROM user_folder WHERE id = $1 and active_delete IS TRUE
'''


NEW_FILE_USER = '''
--создание новой папки для пользователя
INSERT INTO user_files
    (profile_id, id_folder, file_name, create_date, content)
VALUES 
    ($1, $2, $3, $4, $5)
RETURNING id
'''

GET_FOLDER_ID_NAME = '''
-- получение id запрашиваемой папки
SELECT id FROM user_folder WHERE profile_id = $1 and folder_name = $2
'''

CHECK_FILE = '''
-- получения файла по имени
SELECT * FROM user_files WHERE 
    CASE WHEN bool($1::varchar is not null) THEN file_name = $1::varchar ELSE true END
    AND CASE WHEN bool($2::integer is not null) THEN profile_id = $2::integer ELSE true END
    AND CASE WHEN bool($3::integer is not null) THEN id = $3::integer ELSE true END

'''


UPDATA_NAME_FILE = '''
-- установка таймера для удаления папки
UPDATE  user_files SET file_name = $1 WHERE id = $2
'''

DELETE_USER_FILE = '''
--удаление файла пользователя
UPDATE  user_files SET active_delete = $3, date_delete = $4 WHERE id = $1 AND  profile_id = $2

'''


GET_FILE = '''
-- получение сведений о файле
SELECT * FROM user_files WHERE
    CASE WHEN bool($1::integer is not null) THEN profile_id = $1::integer ELSE true END  
    AND CASE WHEN bool($2::integer is not null) THEN id = $2::integer ELSE true END
    AND CASE WHEN bool($3::integer is not null) THEN id_folder = $3::integer ELSE true END
'''


UPDATA_CONTENT_FILE = '''
-- обновление содержимого файла 
UPDATE user_files SET content = $1 WHERE profile_id = $2 AND id_folder = $3 AND id = $4
'''

CHECK_ID_FILE = '''
--получение id файлов в папке
SELECT id from user_files WHERE profile_id = $1 AND id_folder = $2'''


SELECT_DELEDE_FILE = '''
-- получение удаляемых файлов
SELECT * FROM user_files WHERE active_delete IS TRUE
'''

DELETE_USER_FIL = '''
--окончательное удаление папок
DELETE FROM user_files WHERE id = $1 and active_delete IS TRUE
'''