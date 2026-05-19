import sqlite3
import random
import string
conn =sqlite3.connect('user_data.db')       #创建一个文件，存储账户和密码到表中
cur = conn.cursor()                           #增删改查表中的数据
cur.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL)
    ''')





def get_random_account():                               #自动生成账户密码用法（可自选）
    user_name = "admin_"+''.join(random.sample(string.ascii_lowercase, 4))
    password = ''.join(random.sample(string.digits, 6))
    return user_name, password

def init_admin():                                       #创建管理员账号

    cur.execute("SELECT * FROM user WHERE id = 1")                  #在表中寻找，看管理员账号是否存在

    if not cur.fetchone():                                          #若不存在，则生成管理员账号
        uname, pwd = get_random_account()
        cur.execute("INSERT INTO user (username, password) VALUES (?, ?)", (uname, pwd))
        conn.commit()
        print('已自动生成管理员账号')
        print(f'账号:{uname}')
        print(f'密码:{pwd}')

#查看管理员账户信息
def show_admin_account():
    print('\n========账户查询(专属管理员)========')
    key_pwd = input('请输入专属密钥:').strip()
    if key_pwd != 'admin666666':
        print('密钥错误，无法查看！')
        return
    else:
        print('1.查看管理员账户信息')
        print('2.查看所有已注册过的用户信息')
        choice = input('请输入你的选择:').strip()
        if choice == '1':
            cur.execute("SELECT username,password FROM user WHERE id = 1")
            admin_data = cur.fetchone()
            if admin_data:
                print('管理员账户信息')
                print(f'管理员账户:{admin_data[0]}')
                print(f'管理员密码:{admin_data[1]}')
            else:
                print('暂无管理员信息')
        if choice == '2':
            cur.execute("SELECT * FROM user")
            all_users = cur.fetchall()
            print('数据库里所有用户:')
            for user in all_users:
                print(user)

def sign_up():                                                      #用户注册新账户
    print('========用户注册========')
    #选择你注册的方式：
    print('1.自己设置账号和密码')
    print('2.系统随机生成账户和密码（推荐！）')
    choice = input('请输入你的选择').strip()

    if choice == '1':
        new_username = input('请设置你的账户：').strip()
        new_password = input('请设置你的密码：').strip()

        if new_username == "" or new_password == "":  # 检查账户密码不为空
            print('账号或者密码不能为空哦！')
            return
    elif choice == '2':
        #进入可无限循环的，随机挑选账户环节
        while True:
            new_username, new_password = get_random_account()
            print('\n本次随机的账户密码:')
            print(f'账户:{new_username}')
            print(f'密码:{new_password}')
            print('*你是否选择将其作为你的账户密码？')
            print('1.确定使用这个账户密码')
            print('2.换一组(重新随机)')
            print('3.不了，取消注册，返回上一级')
            select = input('请输入你的选择:').strip()
            if select == '1':
                #结束循环
                break
            elif select == '2':
                print('正在重新生成中')
                #立马结束这一次循环，继续下一次循环
                continue
            elif select == '3':
                print('已取消注册，正在返回主菜单')
                return
            else:
                print('输入错误，请输入1/2/3！')
                continue

    else:
        print('输入错误！请输入1/2！')





    cur.execute("SELECT * FROM user WHERE username = ?", (new_username,))        #在存储表中，查找账户是否存在
    res = cur.fetchone()

    if res:                                                                            #若存在，则提醒换一个
        print('该账户已经被注册过了，换一个试试吧~')
        return

    else:                                                                               #若不存在，则将数据储存，注册成功
        cur.execute("INSERT INTO user (username, password) VALUES (?, ?)", (new_username, new_password))
        conn.commit()
        print('注册成功！现在你可以用这个账户登录啦！')


def login():                                                            #登录界面

    print("========系统登录========")
    username = input("请输入账号：").strip()
    password = input("请输入密码：").strip()

    cur.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))     #在表中寻找是否账号存在
    res = cur.fetchone()

    if res:
        print('登录成功，欢迎进入系统！')
    else:
        print('账号或密码错误，登录失败')

def main_menu():
    while True:
        print('\n========简易用户登录系统========')
        print('1.用户登录')
        print('2.用户注册')
        print('3.账户查询（管理员专属）')
        print('4.退出系统')
        choice = input('请输入你的选择：').strip()
        if choice == '1':
            login()
        elif choice == '2':
            sign_up()
        elif choice == '3':
            show_admin_account()
        elif choice == '4':
            break
        else:
            print('输入错误，请输入1/2/3/4！')


if __name__ == '__main__':
    init_admin()
    main_menu()
    conn.close()
