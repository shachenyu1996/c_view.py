"""
还需要一个在游戏外（大厅·）的提示框
"""


"""
command 所需的标识头由调用者提供
"""

from tkinter import *
import tkinter.messagebox
import pickle
from PIL import ImageTk#因为ImageTk.PhotoImage支持的格式gif别的有问题 所以导入PIL模块处理

# 窗口
window = Tk()
window.title('狼人杀')
window.geometry('450x450')
# 画布放置图片
canvas = Canvas(window, height=450, width=450)
imagefile = ImageTk.PhotoImage(file='zh.jpg')#就是这里的格式
image = canvas.create_image(0, 0, anchor='nw', image=imagefile)
canvas.pack(side='top')
# 用户名密码
Label(window, text='用户名:').place(x=100, y=150)
Label(window, text='密码:').place(x=100, y=190)
# 用户名输入框
var_usr_name = StringVar()
entry_usr_name = Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
# 密码输入框
var_usr_pwd = StringVar()
entry_usr_pwd = Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


def log_in():
    """
    登录界面
    登录/注册界面能相互转换，有退出按钮
    
	收集用户账号和密码
	使用command发送
    recv接收回执信息
	
"""
    # 输入框获取用户名密码
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    if usr_name == '' or usr_pwd == '':
        tkinter.messagebox.showerror(message='用户名或密码为空')
    # 不在数据库中弹出是否注册的框
    else:
        is_signup = tkinter.messagebox.askyesno('欢迎', '用户名密码错误')
        if is_signup:
            sign_up()

def sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()

        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            tkinter.messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            tkinter.messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            tkinter.messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = np
            with open('usr_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('欢迎', '注册成功')
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_name = StringVar()
    Label(window_sign_up, text='用户名：').place(x=10, y=10)
    Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = StringVar()
    Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
    Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = StringVar()
    Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 确认注册按钮及位置
    bt_confirm_sign_up = Button(window_sign_up, text='确认注册',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=130)

def usr_sign_quit():
    window.destroy()

def hall_interface():
    """
    大厅界面
    
    需求说明：
    展现目前房间情况
    根据玩家点击进入或创建房间或刷新界面
    """
    lobby_window = Tk()  # 当调用的函数为create_room 或 join_room时，且其返回True(使用 is True 判断)则结束循环
    lobby_window.title("狼人杀")
    lobby_window.geometry("800x500")
    canvas_lobby = Canvas(lobby_window, height=500, width=800)
    imagefile_lobby = ImageTk.PhotoImage(file="timg.jpg")  # 背景
    # image = canvas_lobby.create_image(0, 0, anchor="nw", image=imagefile_lobby)
    canvas_lobby.pack(side="top")
    # 用户名的显示
    Label(lobby_window, text="用户名：%s" % (log_in.usr_name), font=("黑体", 16)).place(x=20, y=30)
    Button(lobby_window, text="创建房间", font=("黑体", 16), command=create_room).place(x=100, y=80)
    Button(lobby_window, text="加入房间", font=("黑体", 16), command=join_room).place(x=200, y=80)

def join_room():
    """
    加入房间界面
    展示房间信息
    如果有需要输入密码
    调用command、recv
		提交信息(room_id，密码（若无则空）)
		并等待接收相应结果
		需显示相应提示
    成功则 return True
    否则   return False
    """
    lobby_window = Tk()  # 当调用的函数为create_room 或 join_room时，且其返回True(使用 is True 判断)则结束循环
    lobby_window.title("加入房间")
    lobby_window.geometry("200x200")
    # 用户名密码
    Label(window, text='用户名:').place(x=100, y=150)
    var_usr_name = StringVar()
    entry_usr_name = Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)
    bt_login = Button(window, text='确定', command=room_interface())
    bt_login.place(x=140, y=230)

def create_room():
    """
    创建房间界面
    获取用户输入的房间名等信息
    调用command、recv
	提交信息
    并等待接收相应结果
    """

    join_window = Tk()
    join_window.title("狼人杀")
    join_window.geometry("450x450")
    Label(window, text='房间名字:').place(x=100, y=150)
    Label(window, text='密码:').place(x=100, y=190)
    # 房间名输入框
    var_usr_name = StringVar()
    entry_usr_name = Entry(window, textvariable=var_usr_name)
    entry_usr_name.place(x=160, y=150)
    # 密码输入框
    var_usr_pwd = StringVar()
    entry_usr_pwd = Entry(window, textvariable=var_usr_pwd, show='*')
    entry_usr_pwd.place(x=160, y=190)
    bt_login = Button(window, text='确定', command=room_interface())
    bt_login.place(x=140, y=230)


def room_interface():
    """
    游戏内界面
	初步分为三层：
		第一层：人物层，显示人员信息（状态，身份）等
		第二层：会话层，显示当前阶段（背景图片显示）及人物发言等
		第三层：输入层，用于获取用户输入信息（文字和语音）等
	整合三层拼接到一起
	"""
    room_info=Tk()
    room_info.title("房间名%s 房间Id%d"%(room_name,room_id))
    room_info.geometry("400x600")
    canvas_lobby = Canvas(room_info, height=500, width=800)
    imagefile_lobby = ImageTk.PhotoImage(file="timg.jpg")  # 背景
    image = canvas_lobby.create_image(0, 0, anchor="nw", image=imagefile_lobby)
    canvas_lobby.pack(side="top")


def people_screen(target, info, *args, **kwargs):
    """
	人物层
	显示人员信息（状态，身份）等
	每个人物都是独立的，减少每次更新人物信息的步骤数
	
	target:需更改的目标
	info::新的信息		dict(属性：值)
	args:视情况而定各自协定
	kwargs:视情况而定各自协定
	"""
    pass

def conversation_screen(data, *args, **kwargs):
    """
	会话层
	获取recv接收到的数据
	显示当前阶段（背景图片显示）及人物发言
	
	data:（dict：{消息源：消息内容}）
	args:视情况而定各自协定
	kwargs:视情况而定各自协定
	"""
    pass
	
def input_screen():
    """
	输入层
	收集用户输入信息
	包括语音和文本
	使用command发送
	
	要求
	当用户处于暂时不能发言却点击发送的情况时
	已键入的文本不会被清除
	
	处于不能发言的情况时语音按钮点击无效
	"""
    pass

def main():
# 登录 注册按钮
    bt_login = Button(window, text='登录', command=log_in)
    bt_login.place(x=140, y=230)
    bt_logup = Button(window, text='注册', command=sign_up)
    bt_logup.place(x=210, y=230)
    bt_logquit = Button(window, text='退出', command=usr_sign_quit)
    bt_logquit.place(x=280, y=230)
    # 主循环
    window.mainloop()

main()
















# def command(iden, data, *args, **kwargs):
#     """
# 	发送端
# 	向服务端发送用户指令
#
# 	iden:标识头（见s_transfer.py）
# 	data:内容
# 	args:视情况而定各自协定
# 	kwargs:视情况而定各自协定
# 	"""
#     pass

# def recv(iden, data, *args, **kwargs):
#     """
# 	接收端
# 	根据服务器返回的数据调用响应的函数，
# 	展示效果（变化）
#
# 	iden:标识头（未定）
# 	data:内容
# 	args:视情况而定各自协定
# 	kwargs:视情况而定各自协定
# 	"""

# def main(client):
# 	while True:
#         acc = log_in()
#         break if acc is not None
# 	client.acc = Account(*acc)
#     while True：						# 该层循环是为了保证每次游戏结束后回到大厅
#         hall_interface()
# 		game_interface()
#
#