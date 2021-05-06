import os
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
            config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'configs/admin.ini'))
            print(config.sections())
            user = args[0].message.from_user
            print(config['ADMINS']['usernames'])
            print(config['ADMINS']['userids'])
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
