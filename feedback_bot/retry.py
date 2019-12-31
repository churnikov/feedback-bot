from loguru import logger
from telegram.error import TimedOut


class Retry:
    def __init__(self, retry_count, function, function_kwargs):
        self.function_kwargs = function_kwargs
        self.function = function
        self.retry_count = retry_count

    def retry(self):
        raise NotImplementedError()


class TelegramTimedOutRetry(Retry):
    def retry(self):
        try:
            return self.function(**self.function_kwargs)
        except TimedOut as e:
            if self.retry_count > 0:
                logger.warning("Got timeout. Retrying.")
                self.retry_count -= 1
                return self.retry()
            else:
                logger.error(
                    "Raising 'TimedOut' exception, because maximum number of reties reached."
                )
                raise e
