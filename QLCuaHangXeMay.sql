create database QLCuaHangXeMay
collate utf8mb4_unicode_ci
character set utf8mb4;

drop database if exists QLCuaHangXeMay;
use QLCuaHangXeMay;

CREATE TABLE XeMay (
    MaXe INT AUTO_INCREMENT PRIMARY KEY,
    TenXe VARCHAR(100) NOT NULL,
    HangXe VARCHAR(50),
    MauXe VARCHAR(50),
    GiaXe DECIMAL(15,2),
    SoLuong INT DEFAULT 0,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO XeMay (TenXe, HangXe, MauXe, GiaXe, SoLuong) VALUES
('Vision 2024', 'Honda', 'Đỏ', 34000000, 10),
('Sirius RC', 'Yamaha', 'Đen', 22000000, 15),
('Air Blade 160', 'Honda', 'Trắng', 52000000, 8),
('Exciter 155', 'Yamaha', 'Xanh', 47000000, 12);

CREATE TABLE NhanVien (
    MaNV INT AUTO_INCREMENT PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    GioiTinh ENUM('Nam','Nữ') DEFAULT 'Nam',
    NgaySinh DATE,
    SDT VARCHAR(20),
    DiaChi VARCHAR(255),
    ChucVu VARCHAR(100),
    Luong DECIMAL(15,2),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO NhanVien (HoTen, GioiTinh, NgaySinh, SDT, DiaChi, ChucVu, Luong) VALUES
('Nguyễn Văn A', 'Nam', '1999-05-12', '0912345678', 'An Giang', 'Quản lý', 15000000),
('Trần Thị B', 'Nữ', '2000-08-20', '0987654321', 'Cần Thơ', 'Nhân viên bán hàng', 9000000),
('Lê Hoàng Min', 'Nam', '2002-03-01', '0901112233', 'Long Xuyên', 'Kế toán', 10000000);

CREATE TABLE KhachHang (
    MaKH INT AUTO_INCREMENT PRIMARY KEY,
    TenKH VARCHAR(100) NOT NULL,
    DiaChi VARCHAR(255),
    SDT VARCHAR(20),
    Email VARCHAR(100),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO KhachHang (TenKH, DiaChi, SDT, Email) VALUES
('Phạm Văn Long', 'Long Xuyên', '0911222333', 'longpv@gmail.com'),
('Nguyễn Thị Mai', 'Châu Đốc', '0909888777', 'mainguyen@gmail.com'),
('Trần Hoàng Anh', 'Tân Châu', '0977665544', 'anhtran@gmail.com');

CREATE TABLE HoaDon (
    MaHD INT AUTO_INCREMENT PRIMARY KEY,
    NgayBan DATE NOT NULL,
    MaKH INT,
    MaNV INT,
    TongTien DECIMAL(18,2) NOT NULL DEFAULT 0,
    GhiChu TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_hd_kh FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_hd_nv FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO HoaDon (MaKH, MaNV, NgayBan, TongTien) VALUES
(1, 1, '2025-11-01', 34000000),
(2, 2, '2025-11-02', 52000000);

CREATE TABLE CTHoaDon (
    MaCT INT AUTO_INCREMENT PRIMARY KEY,
    MaHD INT,
    MaXe INT,
    SoLuong INT DEFAULT 1,
    DonGia DECIMAL(15,2),
    ThanhTien DECIMAL(15,2) GENERATED ALWAYS AS (SoLuong * DonGia) STORED,
    FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD) ON DELETE CASCADE,
    FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO CTHoaDon (MaHD, MaXe, SoLuong, DonGia) VALUES
(1, 1, 1, 34000000),
(2, 3, 1, 52000000);

SELECT * FROM NhanVien;
SELECT * FROM KhachHang;
SELECT * FROM XeMay;
SELECT * FROM HoaDon;
SELECT * FROM CTHoaDon;
DESCRIBE NhanVien;
describe HoaDon;


SELECT 
    hd.MaHD AS 'Mã Hóa Đơn',
    kh.TenKH AS 'Tên Khách Hàng',
    nv.HoTen AS 'Tên Nhân Viên',
    xm.TenXe AS 'Tên Xe',
    xm.HangXe AS 'Hãng Xe',
    xm.MauXe AS 'Màu Xe',
    cthd.SoLuong AS 'Số Lượng',
    cthd.DonGia AS 'Đơn Giá',
    cthd.ThanhTien AS 'Thành Tiền',
    hd.NgayBan AS 'Ngày Bán',
    hd.TongTien AS 'Tổng Tiền'
FROM HoaDon hd
JOIN KhachHang kh ON hd.MaKH = kh.MaKH
JOIN NhanVien nv ON hd.MaNV = nv.MaNV
JOIN CTHoaDon cthd ON hd.MaHD = cthd.MaHD
JOIN XeMay xm ON cthd.MaXe = xm.MaXe
ORDER BY hd.MaHD;



