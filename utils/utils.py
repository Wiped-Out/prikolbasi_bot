from loader import log


async def error_except(user_id: int, error: Exception):
    print(error)
    log.info(f"Ошибка у пользователя {user_id}")
    log.exception(error)
