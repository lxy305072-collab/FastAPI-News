from passlib.context import CryptContext

#创建一个密码上下文对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#密码加密
def get_hash_password( password: str):
    return pwd_context.hash(password)


#密码验证 , 返回true or false
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

















