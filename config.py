class Config:
    DEBUG = True
    TESTING = True

    #Configuración de base dedatos 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://turquesa:Pr1vadasTurq3sas@localhost:3306/privadasturquesas"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://samuelvazquezver:Pr1vadasTurq3sas@samuelvazquezvera.mysql.pythonanywhere-services.com/samuelvazquezver$privadasturquesas"
    SECRET_KEY = 'configproduccion'

class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = True