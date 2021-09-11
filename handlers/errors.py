from loader import dp, log


@dp.errors_handler()
async def errors_handler(update, exception):
    log.exception(f"Update: {update} \n {exception}")
