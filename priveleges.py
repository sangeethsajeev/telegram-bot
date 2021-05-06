
import logging
import configparser
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


logger = logging.getLogger('telegram_bot_priveleges.info')

config = configparser.ConfigParser()


def check_priveleges(function):
    def wrapper(*args, **kwargs):
        print(args[0])
        try:
            config.read('configs/admin.ini')
            user = args[0].message.from_user
            if(user['username'] in config['ADMINS']['usernames'] or user['id'] in config['ADMINS']['userids']):
                logger.error(str(user['username'])+" just accessed me!")
                return function(*args, *kwargs)
            else:
                logger.error(str(user['username'])+" just tried to access me!")
                args[0].message.reply_text("You're not my Admin :)..!")
                print("Privelege Not Found!")
                raise PermissionDeniedError
        except Exception as e:
            print(e)
            args[0].message.reply_text("You're not my Admin :)..!")
        
    return wrapper
