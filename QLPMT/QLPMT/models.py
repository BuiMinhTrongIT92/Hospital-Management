from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from QLPMT import app, db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

class UserRole(UserEnum):
    NguoiQuanTri = 1
    BacSi = 2
    YTa = 3
    BenhNhan = 4
    NhanVienThuNgan = 5
class Sex(UserEnum):
    Nam = 1
    Nu = 2
    Khac = 3

class User(db.Model,UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenNguoiDung = Column(String(50), nullable=False)
    taiKhoan = Column(String(50), nullable=False, unique=True)
    matKhau = Column(String(50), nullable=False)
    gioiTinh = Column(Enum(Sex), default=Sex.Nam)
    namSinh = Column(DateTime)
    active = Column(Boolean, default=True)
    avatar = Column(String(200))
    email = Column(String(50))
    diaChi = Column(String(500))
    ngayTao = Column(DateTime, default=datetime.now())
    SDT = Column(Integer, nullable=False,unique=True)
    user_role = Column(Enum(UserRole))
    khambenh = relationship('KhamBenh', backref='khambenh', lazy=True)
    def __str__(self):
        return self.tenNguoiDung

class NguoiQuanTri(User):
    __tablename__ = 'nguoiquantri'

    def __str__(self):
        return self.chucVu

class BacSi(User):
    __tablename__ = 'bacsi'

    def __str__(self):
        return self.chucVu

class YTa(User):
    __tablename__ = 'yta'

    def __str__(self):
        return self.chucVu

class BenhNhan(User):
    __tablename__ = 'benhnhan'

    def __str__(self):
        return self.chucVu

class NhanVienThuNgan(User):
    __tablename__ = 'nhanvienthungan'

    def __str__(self):
        return self.chucVu

class PhieuKham(db.Model):
    __tablename__ = 'phieukham'
    idPhieuKham = Column(Integer, primary_key=True, autoincrement=True)
    trieuChung = Column(String(500))
    duDoanBenh = Column(String(500))
    tongTien = Column(Integer, default=0)
    daThanhToan = Column(Boolean, default=False)
    idKhamBenh = Column(Integer, ForeignKey('khambenh.idKhamBenh'),unique=True,nullable=False)

class QuyDinh(db.Model):
    __tablename__ = 'quydinh'
    id = Column(Integer, primary_key=True, autoincrement=True)
    slKham = Column(Integer, default=30 )
    loaiThuoc = Column(Integer, default=30)
    tienKham = Column(Integer,default=100000)
    soLoaiDonVi = Column(Integer,default=2)


class LoaiThuoc(db.Model):
    __tablename__ = 'loaithuoc'
    id = Column(Integer,primary_key=True, autoincrement=True)
    tenDonVi = Column(String(50),nullable=False)
    idQuyDinh=Column(Integer,ForeignKey('quydinh.id'),nullable=True,default=1)

    thuoc = relationship('Thuoc', backref='loaithuoc', lazy=False)

    def __str__(self):
        return self.tenDonVi


class KhamBenh(db.Model):
    __tablename__ = 'khambenh'
    idKhamBenh = Column(Integer, primary_key=True, autoincrement=True)
    ngayKham = Column(DateTime, default=datetime.now())
    daKham = Column(Boolean, default=False)
    idNguoiDung = Column(Integer, ForeignKey(User.id), nullable=False)
    # idDSKham = Column(Integer, ForeignKey('danhsachkham.idDSKham'), nullable=False)

# class DanhMucThuoc(db.Model):
#     __tablename__ = 'danhmucthuoc'
#
#     idDanhMuc = Column(Integer, primary_key=True, autoincrement=True)
#     tenDonVi = Column(String(50), nullable=False)
#     thuoc = relationship('Thuoc', backref='danhmucthuoc', lazy=False)
#
#     def __str__(self):
#         return self.tenDonVi

class Thuoc(db.Model):
    #__abstract__ = True
    idThuoc = Column(Integer, primary_key=True, autoincrement=True)
    tenThuoc = Column(String(50), nullable=False)
    cachDung = Column(String(500))
    gia = Column(Integer)
    donVi = Column(Integer,ForeignKey('loaithuoc.id'),nullable=False)

    # idDanhMuc = Column(Integer, ForeignKey('danhmucthuoc.idDanhMuc'), nullable=False)
    phieuKham = relationship('PhieuKham', secondary='phieukham_thuoc', lazy='subquery')
    #backref = backref('thuoc', lazy=True)



class PhieuKhamThuoc(db.Model):
    __tablename__ = 'phieukham_thuoc'
    idPKT = Column(Integer, primary_key=True, autoincrement=True)
    soluong = Column(Integer)
    idThuoc = Column(Integer, ForeignKey('thuoc.idThuoc'), primary_key=True)
    idPhieuKham = Column(Integer, ForeignKey('phieukham.idPhieuKham'), primary_key=True)




if __name__ == '__main__':
    db.create_all()

    quydinh = QuyDinh()
    db.session.add(quydinh)
    db.session.commit()

    loaithuoc1 = LoaiThuoc(tenDonVi='Vien',idQuyDinh=1)
    loaithuoc2 = LoaiThuoc(tenDonVi='Chai', idQuyDinh=1)
    db.session.add(loaithuoc1)
    db.session.add(loaithuoc2)

    db.session.commit()





