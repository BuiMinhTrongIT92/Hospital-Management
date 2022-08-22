from QLPMT import app, db
from flask_admin import Admin,BaseView,expose
from QLPMT.models import Thuoc,User,KhamBenh,PhieuKham,UserRole,LoaiThuoc,QuyDinh
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user,current_user
from flask import redirect,request
from datetime import datetime
import utils
from twilio.rest import Client
import key
client = Client(key.account_sid, key.auth_token)

admin = Admin(app=app, name="An Khang ", template_mode='bootstrap4')

class CustomModel(ModelView):
    can_view_details = True
    form_excluded_columns = ['thuoc']

class DanhMucThuocView(CustomModel):

    # column_labels = {
    #     'tenDonVi': 'Đơn vị'
    # }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NguoiQuanTri

class AdminAuthenicated(CustomModel):
    can_export = True

    column_labels = {
        # Bảng Người dùng
        'tenNguoiDung': 'Tên người dùng',
        'taiKhoan': 'Tài khoản',
        'matKhau': 'Mật khẩu',
        'gioiTinh': 'Giới tính',
        'namSinh': 'Năm sinh',
        'active': 'Hoạt động',
        'avatar': 'Ảnh đại diện',
        'email': 'Email',
        'diaChi': 'Địa chỉ',
        'ngayTao': 'Ngày tạo',
        'SDT': 'Số điện thoại',
        'user_role': 'Quyền sử dụng',
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NguoiQuanTri

class BacSiThuNgan(CustomModel):
    column_labels = {
        # Bảng Phiếu khám
        'trieuChung': 'Triệu chứng',
        'duDoanBenh': 'Dự đoán bệnh',
        'tongTien': 'Tổng tiền',
        'daThanhToan': 'Đã thanh toán',
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.BacSi

class YTaThuNganBSQT(CustomModel):
    column_labels = {
        # Bảng Khám bệnh
        'ngayKham': 'Ngày khám',
        'daKham': 'Đã khám',
        'khambenh': 'Tên bệnh nhân'
    }

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.user_role == UserRole.YTa or current_user.user_role == UserRole.BacSi)

# class SenDSMS(BaseView):
#     @expose("/")
#     def index(self):
#         ds = None
#         date = request.args.get('date')
#         if not date:
#             date = datetime.now()
#         dskham = utils.kham_benh(date=date)
#         ds = dskham
#         send = request.args.get('send')
#         if send:
#             for getsdt in ds:
#                 message = client.messages.create(
#                     to='+84'+str(getsdt[4]),
#                     from_=key.twilio_number,
#                     body='Ngày khám: ' + str(getsdt[1]) + ' Bệnh nhân: ' + getsdt[3] + ' Tại phòng khám An Khang')
#                 print(message.body)
#         return self.render('/admin/sendSMS.html',dskham=dskham)
#
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role == UserRole.YTa

class SenDSMS(BaseView):
    @expose("/")
    def index(self):
        date = request.args.get('date')
        if not date:
            date = datetime.now()
        dskham = utils.kham_benh(date=date)
        ds = dskham
        sen = request.args.get('sen')
        if date and sen:
            for getsdt in ds:
                message = client.messages.create(
                    to='+84' + str(getsdt[3]),
                    from_=key.twilio_number,
                    body='Ngày khám: ' + str(getsdt[1]) + ' Bệnh nhân: ' + getsdt[2] + ' Tại phòng khám An Khang')
                print(message.body)

        return self.render('/admin/sendSMS.html', dskham=dskham, date=date)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.YTa


class phieukhambenh(BaseView):
    @expose("/")
    def index(self):
        idphieukham = request.args.get('idphieukham')
        hoadon = request.args.get('hoadon')

        try:
            if not idphieukham:
                idphieukham=1
            thongtinkhambenh= utils.get_thongtinkhambenh(idphieukham)
            dsthuoc = utils.get_phieukham_thuoc(idphieukham)

        except:
            return redirect('/admin/phieukhambenh')

        if idphieukham and hoadon:
            if utils.get_dathanhtoan(idphieukham)==0:
                utils.set_tongtien(idphieukham)
                utils.set_dathanhtoan(idphieukham)
                tien = utils.get_hoadon(idphieukham)

                return self.render('/admin/phieukhambenh.html', thongtinkhambenh=thongtinkhambenh, dsthuoc=dsthuoc,
                                   idphieukham=idphieukham, tien=tien)

            tien =utils.get_hoadon(idphieukham)
            return self.render('/admin/phieukhambenh.html', thongtinkhambenh=thongtinkhambenh, dsthuoc=dsthuoc,
                               idphieukham=idphieukham,tien=tien)

        return self.render('/admin/phieukhambenh.html',thongtinkhambenh=thongtinkhambenh,dsthuoc=dsthuoc,
                               idphieukham=idphieukham,tien=[0,0,0])


    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NhanVienThuNgan

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose("/")
    def index(self):
        mon = request.args.get('dat')
        if mon:
            mon = datetime.strptime(mon,'%Y-%m-%d')
            year = mon.year
            month = mon.month
        else:
            year = datetime.now().year
            month = datetime.now().month
        dt = utils.total(month=month, year=year)
        return self.render('/admin/stats.html', month_stats=utils.doanhthhu_stats(month=month, year=year),month=month,dt=dt)

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.user_role == UserRole.NguoiQuanTri or current_user.user_role == UserRole.NhanVienThuNgan)

class ThuocStatsView(BaseView):
    @expose("/")
    def index(self):
        month = request.args.get('month', datetime.now().month)
        year = request.args.get('year', datetime.now().year)

        return self.render('/admin/thuoc_stats.html', thuoc_month_stats=utils.thuoc_stats(year=year, month=month),month=month,year=year)

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.user_role == UserRole.NguoiQuanTri or current_user.user_role == UserRole.NhanVienThuNgan)

class QuyDinhView(ModelView):
    can_export = True
    can_create = False
    can_delete = False

    column_labels = {
        # Bảng Quy định
        'slKham': 'Số lượng khám',
        'loaiThuoc': 'Loại thuốc',
        'tienKham': 'Tiền khám',
        'soLoaiDonVi': 'Số loại đơn vị thuốc',
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NguoiQuanTri

class ThuocView(ModelView):
    can_export = True
    column_searchable_list = ['tenThuoc', 'cachDung']
    column_filters = ['tenThuoc', 'gia']
    column_exclude_list = ['image']
    column_labels = {
        # Bảng Thuốc
        'tenThuoc': 'Tên thuốc',
        'cachDung': 'Cách dùng',
        'gia': 'Giá',
        'loaithuoc': 'Tên đơn vị',
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NguoiQuanTri

class LoaiThuocView(ModelView):
    can_export = True
    can_create = False
    can_delete = False

    column_labels = {
        # Bảng Loại thuốc
        'tenDonVi': 'Tên đơn vị',
    }

class PKThuoc(BaseView):
    @expose("/")
    def index(self):
        table = []
        get_id = utils.get_ipk()
        dsthuoc = utils.get_dsthuoc()
        sl = request.args.get('sl')
        loaithuoc = request.args.get('loaithuoc')
        idpk = request.args.get('phieukham')
        xem = request.args.get('Xem')
        sr = None
        delid = request.args.get('deleteid')
        delete = request.args.get('xoa')
        table = utils.get_table(idPhieuKham=1)
        if sl and loaithuoc and idpk and not xem:
            utils.add_pkt(idpk,loaithuoc,sl)
            table = utils.get_table(idpk)
        elif xem == 'Xem':
            table = utils.get_table(idpk)
            sl = None;
            idpk = None;
            loaithuoc = None;
        elif delete.__eq__('Xóa') and delid:
            iddd = utils.idget(delid)
            utils.del_pkt(delid)
            table = utils.get_table(iddd)
        return self.render('/admin/pkthuoc.html',dsthuoc=dsthuoc,geti=get_id,table=table)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.BacSi

admin.add_view(BacSiThuNgan(PhieuKham,db.session,name="Phiếu khám"))
admin.add_view(YTaThuNganBSQT(KhamBenh,db.session,name="Khám bệnh"))
admin.add_view(AdminAuthenicated(User,db.session,name="Người dùng"))
admin.add_view(AdminAuthenicated(LoaiThuoc,db.session,name="Loại thuốc"))
admin.add_view(ThuocView(Thuoc, db.session,name="Thuốc"))
admin.add_view(QuyDinhView(QuyDinh,db.session,name="Quy định"))
admin.add_view(SenDSMS(name="Gửi SMS"))
admin.add_view(phieukhambenh(name="Phiếu khám kệnh"))
admin.add_view(PKThuoc(name="Thêm thuốc cho phiếu khám"))
admin.add_view(StatsView(name="Thống kê báo cáo doanh thu"))
admin.add_view(ThuocStatsView(name="Báo các sử dụng thuốc"))
admin.add_view(LogoutView(name="Đăng xuất"))



