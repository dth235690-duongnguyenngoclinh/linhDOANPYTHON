import tkinter as tk
from tkinter import messagebox
from database import get_connection

# các form con
from form_XeMay import open_xe_form
from form_NhanVien import open_nv_form
from form_KhachHang import open_kh_form
from form_HoaDon import open_hd_form
from form_CTHoaDon import open_cthd_form

# ----------------- KẾT NỐI DATABASE -----------------
conn = get_connection()
if not conn:
    tk.messagebox.showerror("Lỗi", "Không kết nối được MySQL. Kiểm tra database.py")
    raise SystemExit("Không kết nối DB")

# ----------------- MENU CHÍNH -----------------
root = tk.Tk()
root.title("Quản Lý Cửa Hàng Xe Máy")
root.geometry("500x500")

tk.Label(root, text="GIAO DIỆN CHÍNH", font=("Arial", 20, "bold")).pack(pady=20)

tk.Button(root, text="Quản lý Xe máy", width=28, height=2,
          command=lambda: open_xe_form(root, conn)).pack(pady=6)

tk.Button(root, text="Quản lý Nhân viên", width=28, height=2,
          command=lambda: open_nv_form(root, conn)).pack(pady=6)

tk.Button(root, text="Quản lý Khách hàng", width=28, height=2,
          command=lambda: open_kh_form(root, conn)).pack(pady=6)

tk.Button(root, text="Quản lý Hóa đơn", width=28, height=2,
          command=lambda: open_hd_form(root, conn)).pack(pady=6)

tk.Button(root, text="Quản lý Chi tiết HĐ", width=28, height=2,
          command=lambda: open_cthd_form(root, conn)).pack(pady=6)

tk.Button(root, text="Thoát", width=28, height=2, command=lambda: (conn.close(), root.quit()), ).pack(pady=18)

root.mainloop()
