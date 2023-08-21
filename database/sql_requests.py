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