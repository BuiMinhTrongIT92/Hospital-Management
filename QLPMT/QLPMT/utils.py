from QLPMT.models import User,KhamBenh,PhieuKham,UserRole,QuyDinh,Thuoc,PhieuKhamThuoc,LoaiThuoc
import hashlib
from QLPMT import db,app
from sqlalchemy import func
from sqlalchemy.sql import extract
from datetime import datetime
import hashlib

def get_nguoidung_id(user_id):
    return User.query.get(user_id)

def check_login(username,password,role=UserRole.BenhNhan):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.taiKhoan.__eq__(username.strip()),User.matKhau.__eq__(password),User.user_role.__eq__(role),User.active.__eq__(1)).first()

def get_role(username,password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        getrole =  User.query.filter(User.taiKhoan.__eq__(username.strip()),User.matKhau.__eq__(password),User.active.__eq__(1)).first()
    return getrole.user_role

def doanhthhu_stats(month,year):
    bd = db.session.query(func.sum(PhieuKham.tongTien)).join(KhamBenh,
                                                             KhamBenh.idKhamBenh.__eq__(
                                                                 PhieuKham.idKhamBenh)).filter(PhieuKham.daThanhToan == '1').filter(
        extract('year', KhamBenh.ngayKham) == year).filter(
        extract('month', KhamBenh.ngayKham) == month).add_columns(func.sum(PhieuKham.tongTien)).first()

    quydinh = QuyDinh.query.filter().first()
    tienkham = quydinh.tienKham
    return db.session.query(KhamBenh.ngayKham, func.sum(PhieuKham.tongTien + tienkham),
                                func.count(func.distinct(KhamBenh.idNguoiDung)),(func.sum(PhieuKham.tongTien)/bd[0])).join(KhamBenh,
                                                                        KhamBenh.idKhamBenh.__eq__(
                                                                            PhieuKham.idKhamBenh)).filter(KhamBenh.daKham == '1').filter(PhieuKham.daThanhToan == '1').filter(
            extract('year', KhamBenh.ngayKham) == year).filter(
            extract('month', KhamBenh.ngayKham) == month).group_by(extract('day', KhamBenh.ngayKham)).all()

# Thêm
def thuoc_stats(kw=None, from_date=None, to_date=None, year=None, month=None):

    p = db.session.query(Thuoc.idThuoc, Thuoc.tenThuoc, LoaiThuoc.tenDonVi,
                            func.sum(PhieuKhamThuoc.soluong),
                            func.count(Thuoc.idThuoc))\
        .join(PhieuKhamThuoc, PhieuKhamThuoc.idThuoc.__eq__(Thuoc.idThuoc), isouter=True)\
        .join(LoaiThuoc, LoaiThuoc.id.__eq__(Thuoc.donVi))\
        .join(KhamBenh, KhamBenh.idKhamBenh.__eq__(PhieuKhamThuoc.idPhieuKham))\
        .filter(extract('month', KhamBenh.ngayKham) == month)\
        .filter(extract('year', KhamBenh.ngayKham) == year)\
        .group_by(Thuoc.idThuoc, Thuoc.tenThuoc, LoaiThuoc.tenDonVi)

    if from_date:
        p = p.filter(KhamBenh.ngayKham.__ge__(from_date))

    if to_date:
        p = p.filter(KhamBenh.ngayKham.__le__(to_date))

    return p.all()

def add_user(name,username,password,SDT,role=UserRole.BenhNhan, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(tenNguoiDung=name,
                taiKhoan=username,
                matKhau=password,
                gioiTinh=kwargs.get('gender'),
                namSinh=kwargs.get('birthday'),
                avatar=kwargs.get('avatar'),
                email=kwargs.get('email'),
                diaChi=kwargs.get('address'),
                user_role=role,
                SDT=SDT)
    db.session.add(user)
    db.session.commit()

def load_bacsi(page=1):
    Users = User.query.filter(User.active == True,User.user_role.__eq__("BacSi"))
    pagesize = app.config["PAGESIZE"]
    start = (page - 1) * pagesize
    end = start + pagesize
    return Users.slice(start, end).all()

def count_bacsi():
    Users = User.query.filter(User.active == True, User.user_role.__eq__("BacSi"))
    return Users.count()

def loaduser(username):
    uu = User.query.filter(User.active == True, User.taiKhoan.__eq__(username)).first()
    return uu

def count_lichkham(ngayKham):
    countlichkham = KhamBenh.query.filter(KhamBenh.ngayKham.__eq__(ngayKham)).count()
    return int(countlichkham)

def add_dangkikham(id_user,ngayKham,trieuchung):
    kham = KhamBenh(ngayKham=ngayKham,idNguoiDung=id_user)
    db.session.add(kham)
    db.session.commit()
    phieukham = PhieuKham(trieuChung=trieuchung,idKhamBenh=kham.idKhamBenh)
    db.session.add(phieukham)
    db.session.commit()

def eq_user(username):
    eq_user = User.query.filter(User.taiKhoan.__eq__(username)).first()
    return eq_user.taiKhoan

def getuser(username,sdt):
    uu = User.query.filter(User.tenNguoiDung.__eq__(username),User.SDT.__eq__(sdt)).first()
    return uu

def kham_benh(date):
    dskhambenh = db.session.query(KhamBenh.idKhamBenh, KhamBenh.ngayKham,
                                      User.tenNguoiDung,User.SDT).join(KhamBenh, KhamBenh.idNguoiDung.__eq__(User.id)).filter(KhamBenh.ngayKham.__eq__(date)).all()
    return dskhambenh

def get_soLuongKham():
    quydinh= QuyDinh.query.filter().first()
    return quydinh.slKham

def get_thongtinkhambenh(idkhambenh):
    khambenh = KhamBenh.query.filter(KhamBenh.idKhamBenh.__eq__(idkhambenh)).first()
    user = User.query.filter(User.id.__eq__(khambenh.idNguoiDung)).first()
    phieukham =PhieuKham.query.filter(PhieuKham.idKhamBenh.__eq__(idkhambenh)).first()

    thongtin =[user.tenNguoiDung, khambenh.ngayKham, phieukham.trieuChung, phieukham.duDoanBenh]
    return thongtin

def get_phieukham_thuoc(idkhambenh):
    phieukham = PhieuKham.query.filter(PhieuKham.idKhamBenh.__eq__(idkhambenh)).first()
    phieukham_thuoc_donvi = db.session.query(PhieuKhamThuoc.idPhieuKham, Thuoc.tenThuoc, LoaiThuoc.tenDonVi,PhieuKhamThuoc.soluong
                                   ,Thuoc.cachDung).join(Thuoc, Thuoc.idThuoc.__eq__(PhieuKhamThuoc.idThuoc))\
        .join(LoaiThuoc,LoaiThuoc.id.__eq__(Thuoc.donVi)).filter(PhieuKhamThuoc.idPhieuKham.__eq__(phieukham.idPhieuKham)).all()
    return phieukham_thuoc_donvi

def get_hoadon(idphieukham):
    phieukham = PhieuKham.query.filter(PhieuKham.idKhamBenh.__eq__(idphieukham)).first()

    tongtien =phieukham.tongTien
    tienthuoc= get_tienthuoc(idphieukham)

    tienkham =tongtien-tienthuoc
    tien=[tienkham,tienthuoc,tongtien]
    return tien

def get_tienthuoc(idphieukham):
    phieukham = PhieuKham.query.filter(PhieuKham.idKhamBenh.__eq__(idphieukham)).first()
    phieukham_thuoc = db.session.query(Thuoc.gia, PhieuKhamThuoc.soluong).join(Thuoc, Thuoc.idThuoc.__eq__(PhieuKhamThuoc.idThuoc))\
                                    .filter(PhieuKhamThuoc.idPhieuKham.__eq__(phieukham.idPhieuKham)).all()
    tienthuoc = 0
    for tien in phieukham_thuoc:
        tienthuoc += tien[0] * tien[1]
    return tienthuoc


def set_tongtien(idphieukham):
    quydinh = QuyDinh.query.filter().first()
    tienkham = quydinh.tienKham
    db.session.query(PhieuKham).filter(PhieuKham.idPhieuKham.__eq__(idphieukham)).update({"tongTien":(get_tienthuoc(idphieukham)+tienkham)})
    db.session.commit()

def set_dathanhtoan(idphieukham):
    db.session.query(PhieuKham).filter(PhieuKham.idPhieuKham.__eq__(idphieukham)).update({"daThanhToan": (1)})
    db.session.commit()

def get_dathanhtoan(idphieukham):
    phieukham= PhieuKham.query.filter(PhieuKham.idPhieuKham.__eq__(idphieukham)).first()
    return phieukham.daThanhToan

def total(month,year):
    data = doanhthhu_stats(month,year)
    totall = 0
    for i in data:
        totall = totall + i[1]

    return "{:,.1f}".format(totall)
def get_soLuongKham():
    quydinh= QuyDinh.query.filter().first()
    return quydinh.slKham

def get_dsthuoc():
    dsthuoc = Thuoc.query.filter().all()
    return dsthuoc


def get_ipk():
    return PhieuKham.query.filter().all()

def get_table(idPhieuKham):
    return db.session.query(PhieuKhamThuoc.idPKT,PhieuKhamThuoc.soluong,Thuoc.tenThuoc,PhieuKhamThuoc.idPhieuKham).join(PhieuKhamThuoc, PhieuKhamThuoc.idThuoc.__eq__(Thuoc.idThuoc)).filter(PhieuKhamThuoc.idPhieuKham.__eq__(idPhieuKham)).all()

def add_pkt(idPhieuKham,tenThuoc,sluong):
    idThuoc = Thuoc.query.filter(Thuoc.tenThuoc.__eq__(tenThuoc)).first();
    getpkt = PhieuKhamThuoc(idPhieuKham=idPhieuKham,idThuoc=idThuoc.idThuoc,soluong=sluong)
    db.session.add(getpkt)
    db.session.commit();

def del_pkt(idpkt):
    db.session.query(PhieuKhamThuoc).filter(PhieuKhamThuoc.idPKT.__eq__(idpkt)).delete()
    db.session.commit()

def idget(idpkt):
    eq_user = PhieuKhamThuoc.query.filter(PhieuKhamThuoc.idPKT.__eq__(str(idpkt))).first()
    return eq_user.idPhieuKham