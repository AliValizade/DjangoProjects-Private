from abc import ABC, abstractmethod
import random
from types import NoneType
from typing import Any
from datetime import datetime, timedelta
from kavenegar import *
from redis.exceptions import RedisError

from config.redis_config import RedisConfig



class CustomException(Exception):
    def __init__(self, message):
        super().__init__(message)



class Event(ABC):
    pass

class EmailManager(Event):
    pass


class OtpManager(Event):

    def send_otp_code(phone_number, code):
        try:
            api = KavenegarAPI('#')
            params = {
                'sender' : '#',
                'receptor': phone_number,
                'message' : f'{code} کد تایید شما'
            }
            response = api.sms_send(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)


    @staticmethod    
    def generate_otp_code() -> int:
        random_code = random.randint(10000, 99999)
        return random_code




class RedisManager(RedisConfig):

    def add_to_redis(self, phone_number: str, code: str) -> None:
        try:
           self.redis.set(phone_number, code, ex=timedelta(minutes=2))

        except RedisError as exp:
            raise CustomException("Service temporarily unavailable")

    def get_by_redis(self, phone_number: str) -> str:
        try:
            data = self.redis.get(phone_number)
            return data.decode("utf-8")
        except RedisError as exp:
            raise CustomException("Service temporarily unavailable")
        except (TypeError, ValueError, AttributeError):
            raise CustomException("Not Found")

    def check_exists_redis(self, phone_number: str) -> bool:
        """
        check exists key in redis
        """
        try:
            exists = self.redis.exists(phone_number)
            return exists
        except RedisError as exp:
            raise CustomException("Service temporarily unavailable")


