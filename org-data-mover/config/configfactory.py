from config_dev import ConfigDev
from config_prod import ConfigProd
from config_test import ConfigTest
from config import Config

configs = {'development': ConfigDev, 'production':  ConfigProd, 'test': ConfigTest}


class ConfigFactory:

    @staticmethod
    def create_config(env='development'):
        config = configs[env]()
        return config

if __name__ == "__main__":
    factory = ConfigFactory()
    config = ConfigFactory.create_config('dev')
    val = ConfigFactory.get_value(config, 'SECRET_KEY')
    print val
    val = ConfigFactory.get_value('config', 'DEBUGG') or 10
    print val