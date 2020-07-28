# -*- coding:utf-8 -*-
# author:fei2232
import hashlib,base64,random,string



class UserService():

    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%(user_info.user_id, user_info.user_name, user_info.user_pwd, user_info.user_id)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s"%(base64.encodebytes(pwd.encode("utf-8")),salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length = 16):
        keylist = [random.choice((string.ascii_letters+string.digits)) for i in range(length)]
        return ("".join(keylist))