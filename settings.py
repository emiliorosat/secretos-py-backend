from dotenv import load_dotenv
import dotenv
import os
import sys

is_prod = os.environ.get('IS_HEROKU', None)
load_dotenv()

jwtSecret = os.environ.get('JWT_SECRET') or os.getenv("JWT_SECRET")

env = dotenv.dotenv_values()
if(jwtSecret == None):
    jwtSecret = env["JWT_SECRET"].encode("utf-8")

print(jwtSecret)
#print( env["JWT_SECRET"] )

#if is_prod:
#    print("is prod")
#else:
    #jwtSecret = os.environ.get("JWT_SECRET")
#    print( os.getenv("JWT_SECRET") )



#if 'JWT_SECRET' in os.environ:
#    print("Has in environ")
#else:
#    print("no Env")



#if(jwtSecret == None):

