from flask import render_template, url_for
from QLPMT import app, login
from flask_login import login_user
from twilio.rest import Client
import cloudinary.uploader
import math
import key
client = Client(key.account_sid, key.auth_token)

@app.route("/")
def TrangChu():
    quantity = utils.count_bacsi()
    page = request.args.get('page',1)
    bacsi = utils.load_bacsi(page=int(page))
    return render_template("TrangChu.html",bacsi=bacsi,pages=math.ceil(quantity/app.config['PAGESIZE']))

# @app.route('/admin-login',methods=['post'])
# def admin_login():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     admin = utils.check_login(username=username,password=password)
#     if admin:
#         login_user(user=admin)
#
#     return redirect('/admin')

@app.route('/admin-login',methods=['post'])
def admin_login():
    war = ""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        role = utils.get_role(username=username, password=password)
        admin = utils.check_login(username=username, password=password, role=role)
        if admin:
            login_user(user=admin)
    except Exception as ex:
        war = 'Không tồn tại người dùng'
        return render_template('admin.html',war=war)

    return redirect('/admin')

@login.user_loader
def load_nguoidung(user_id):
    return utils.get_nguoidung_id(user_id=user_id)

@app.route('/user-signin', methods=['get', 'post'])
def user_signin():
    warning_err = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            role_user = utils.get_role(username=username, password=password)
            if str(role_user) == 'UserRole.BenhNhan':
                user = utils.check_login(username, password)
            elif str(role_user) == 'UserRole.YTa':
                user = utils.check_login(username, password, role_user)
            else:
                user = utils.check_login(username, password)
            if user:
                login_user(user=user)
                return redirect(url_for('TrangChu'))
            else:
                warning_err = 'Thông tin đăng nhập không chính xác !!!'
        except Exception as ex:
            warning_err = "Không tồn tại người dùng"

    return render_template('login.html',warning_err=warning_err)

@app.route('/user-signout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.route('/register', methods=['get','post'])
def user_register():
    err_register = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        gender = request.form.get('gender')
        address = request.form.get('address')
        birthday = request.form.get('birthday')
        SDT = request.form.get('SDT')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, gender=gender, address=address, birthday=birthday, avatar=avatar_path, SDT=SDT)
                return redirect(url_for('user_signin'))
            else:
                err_register = "Mật khẩu không khớp"
        except Exception as ex:
            err_register = "Trùng tài khoản hoặc sai thông tin"

    return render_template('dangki.html',err_register=err_register)

@app.route("/dangkilichkham",methods=['get','post'])
def dangkilichkham():
    quantity = utils.count_bacsi()
    page = request.args.get('page', 1)
    bacsi = utils.load_bacsi(page=int(page))
    ngaykham = request.form.get('ngaykham')
    trieuchung = request.form.get('trieuchung')
    sdt = request.form.get('sdt')
    name = request.form.get('name')
    erro = ''
    if current_user.is_authenticated:
        role_user = current_user.user_role
        if str(role_user) == 'UserRole.BenhNhan' or str(role_user) == 'UserRole.YTa':
            user = utils.getuser(name, sdt)
            try:
                id_user = user.id
                role = user.user_role
                if id_user:
                    if str(role) == 'UserRole.BenhNhan':

                        songaykham = utils.count_lichkham(ngayKham=ngaykham)
                        if songaykham < int(utils.get_soLuongKham()):
                            utils.add_dangkikham(id_user=int(id_user), ngayKham=ngaykham, trieuchung=trieuchung)
                            erro = 'ThanhCong'
                            render_template('TrangChu.html', pages=math.ceil(quantity / app.config['PAGESIZE']), bacsi=bacsi,
                                            erro=erro)
                        else:
                            erro = 'DaDuNguoi'
            except Exception as ex:
                erro = 'TKKTT'
        elif str(role_user) == 'UserRole.BenhNhan':
            link = 'dangkilichkhamyta'
    else:
        return redirect(url_for('user_signin'))

    return render_template('TrangChu.html', pages=math.ceil(quantity / app.config['PAGESIZE']), bacsi=bacsi, erro=erro)

@app.route("/dangkilichkham-yta",methods=['get','post'])
def dangkilichkhamyta():
    errregister = ""
    erro = ""
    if request.method.__eq__('POST'):
        if current_user.is_authenticated:
            role_user = current_user.user_role
            if str(role_user) == 'UserRole.YTa':
                name = request.form.get('name')
                username = request.form.get('username')
                password = request.form.get('password')
                confirm = request.form.get('confirm')
                email = request.form.get('email')
                gender = request.form.get('gender')
                address = request.form.get('address')
                birthday = request.form.get('birthday')
                SDT = request.form.get('SDT')
                ngaykham = request.form.get('ngaykham')
                trieuchung = request.form.get('trieuchung')
                avatar_path = None
                sdt = '+84' + str(SDT)
                try:
                    if password.strip().__eq__(confirm.strip()):
                        avatar = request.files.get('avatar')
                        u = utils.check_login(username, password)
                        if not u:
                            if avatar:
                                res = cloudinary.uploader.upload(avatar)
                                avatar_path = res['secure_url']
                            utils.add_user(name=name, username=username, password=password, email=email, gender=gender,
                                           address=address, birthday=birthday, avatar=avatar_path, SDT=SDT)
                            us = utils.loaduser(username=username)
                            iduser = us.id
                        else:
                            us = utils.loaduser(username=username)
                            iduser = us.id
                        if iduser:
                            songaykham = utils.count_lichkham(ngayKham=ngaykham)
                            if songaykham < int(utils.get_soLuongKham()):
                                utils.add_dangkikham(id_user=int(iduser), ngayKham=ngaykham, trieuchung=trieuchung)
                                erro = 'ThanhCong'
                            else:
                                erro = 'DaDuNguoi'
                    else:
                        errregister = "Mật khẩu không khớp"
                except Exception as ex:
                    errregister = "Trùng tài khoản hoặc sai thông tin"
            else:
                errregister = 'Chỉ y tá được sử dụng'
        else:
            redirect(url_for('user_signin'))
    return render_template('dangkilichkham-yta.html', errregister=errregister,erro=erro)



if __name__ == '__main__':
    from QLPMT.admin import *

    app.run(debug=True)

