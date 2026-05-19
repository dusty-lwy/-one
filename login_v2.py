import sqlite3
import random
import string

#第一层：搭建基本的东西
class DBHelper:
    #创建文件和操作手
    def __init__(self,db_name = 'user.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
    #数据库方法：增加，查找
    def execute(self,sql,params=()):
        self.cur.execute(sql,params)
        self.conn.commit()
    #数据库方法：执行查询，只返回一条结果
    def query(self, sql, params=()):
        self.cur.execute(sql, params)
        return self.cur.fetchone()
    #数据库方法：查询，拎出来
    def query_all(self,sql,params=()):
        self.cur.execute(sql,params)
        return self.cur.fetchall()
    #结束关闭操作手和数据库
    def close(self):
        self.cur.close()
        self.conn.close()
#第二层：功能层
class UserSystem:
    def __init__(self):
        self.db = DBHelper()
        self.db.cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)
        ''')

    def get_random_account(self):# 自动生成账户密码用法（可自选）
        user_name = "admin_" + ''.join(random.sample(string.ascii_lowercase, 4))
        password = ''.join(random.sample(string.digits, 6))
        return user_name, password

    def init_admin(self):  # 创建管理员账号

        result = self.db.query("SELECT * FROM user WHERE id = 1")

        # 如果查到了数据，说明管理员已存在，什么都不做
        if result:
            return False, None, None

        uname, pwd = self.get_random_account()
        self.db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (uname, pwd))
        return  True,uname,pwd

    def register(self,uname,pwd):
        res = self.db.execute("SELECT * FROM user WHERE username = ?", (uname,))  # 在存储表中，查找账户是否存在

        if res:  # 若存在，则提醒换一个
            return False,'该账户已经被注册过了，换一个试试吧~'

             # 若不存在，则将数据储存，注册成功
        self.db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (uname, pwd))
        return True,'注册成功！现在你可以用这个账户登录啦！'


    def login(self,uname,pwd):
        result = self.db.query(
            "SELECT id FROM user WHERE username = ? AND password = ?",
            (uname, pwd)
        )
        if result:
            return True, "登录成功"
        return False, "账号或密码错误"

    def check_admin_key(self, key):
            """验证管理员密钥"""
            return key == "admin666666"

    def get_admin_info(self):
            """获取管理员账号信息"""
            return self.db.query("SELECT username, password FROM user WHERE id = 1")
    def get_all_users(self):
            """获取所有已注册用户"""
            return self.db.query_all("SELECT id, username,password FROM user")

    def close(self):
            """关闭数据库"""
            self.db.close()

    # 第三层：交互表现层 —— main 菜单
    # 只负责：打印文字、接收用户输入、判断选项


def main():
    system = UserSystem()

    # --- 启动时检查管理员账号 ---
    created, uname, pwd = system.init_admin()
    if created:
        print("已自动生成管理员账号")
        print(f"账号: {uname}")
        print(f"密码: {pwd}")

        # --- 主循环 ---
    while True:
        print('\n======== 简易用户登录系统 ========')
        print('1. 用户登录')
        print('2. 用户注册')
        print('3. 账户查询（管理员专属）')
        print('4. 退出系统')
        choice = input('请输入你的选择: ').strip()

            # ---------- 1. 登录 ----------
        if choice == '1':
            username = input("请输入账号: ").strip()
            password = input("请输入密码: ").strip()
            success, msg = system.login(username, password)
            print(msg)

        # ---------- 2. 注册 ----------
        elif choice == '2':
            print('======== 用户注册 ========')
            print('1. 自己设置账号和密码')
            print('2. 系统随机生成账户和密码（推荐）')
            reg_choice = input('请输入你的选择: ').strip()

            if reg_choice == '1':
                new_username = input('请设置你的账户: ').strip()
                new_password = input('请设置你的密码: ').strip()

            elif reg_choice == '2':
                while True:
                    uname, pwd = system.get_random_account()
                    print(f'\n本次随机的账户密码:')
                    print(f'账户: {uname}')
                    print(f'密码: {pwd}')
                    print('1. 确定使用')
                    print('2. 换一组')
                    print('3. 取消注册')
                    select = input('请输入你的选择: ').strip()

                    if select == '1':
                        new_username, new_password = uname, pwd
                        break
                    elif select == '2':
                        continue
                    elif select == '3':
                        new_username, new_password = None, None
                        break
                    else:
                        print('输入错误，请输入 1/2/3！')

                if new_username is None:
                    continue
            else:
                print('输入错误！')
                continue

            success, msg = system.register(new_username, new_password)
            print(msg)

        # ---------- 3. 管理员查询 ----------
        elif choice == '3':
            key = input('请输入专属密钥: ').strip()
            if not system.check_admin_key(key):
                print('密钥错误，无法查看！')
                continue

            print('1. 查看管理员账户信息')
            print('2. 查看所有已注册过的用户信息')
            sub_choice = input('请输入你的选择: ').strip()

            if sub_choice == '1':
                admin_data = system.get_admin_info()
                if admin_data:
                    print('管理员账户信息:')
                    print(f'管理员账户: {admin_data[0]}')
                    print(f'管理员密码: {admin_data[1]}')
                else:
                    print('暂无管理员信息')

            elif sub_choice == '2':
                users = system.get_all_users()
                print('数据库里所有用户:')
                for user in users:
                    print(f'ID: {user[0]}, 用户名: {user[1]},密码：{user[2]}')
            else:
                print('输入错误！')

        # ---------- 4. 退出 ----------
        elif choice == '4':
            system.close()
            print("再见！")
            break

        else:
            print('输入错误，请输入 1/2/3/4！')

if __name__ == '__main__':
    main()

