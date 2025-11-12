import tkinter as tk
from tkinter import ttk, messagebox

def open_cthd_form(root, conn):
    cursor = conn.cursor()
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Quản lý Chi tiết Hóa đơn")
    win.geometry("1100x650")

    # === TIÊU ĐỀ ===
    tk.Label(win, text="QUẢN LÝ CHI TIẾT HÓA ĐƠN", font=("Arial", 19, "bold"), fg="#003399").pack(pady=10)

    # === DANH SÁCH TẠM ===
    temp_data = []


    # === THANH TÌM KIẾM ===
    search_frame = tk.Frame(win)
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5)
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=60, font=("Arial", 10)).grid(row=0, column=1, padx=5)
    tk.Button(search_frame, text="Tìm", bg="#2196F3", fg="white", width=10,
              command=lambda: load_data(search_var.get())).grid(row=0, column=2, padx=5)
    tk.Button(search_frame, text="Tải lại", bg="#9E9E9E", fg="white", width=10,
              command=lambda: (search_var.set(""), load_data())).grid(row=0, column=3, padx=5)

    # === KHUNG DANH SÁCH CHI TIẾT HÓA ĐƠN ===
    frame_ds = tk.LabelFrame(win, text="Danh sách chi tiết hóa đơn", padx=10, pady=10, font=("Arial", 11, "bold"), fg="#003366")
    frame_ds.pack(padx=10, pady=10, fill="both", expand=True)

    scroll = tk.Scrollbar(frame_ds)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ["MaHD", "MaXe", "SoLuong", "DonGia", "ThanhTien"]
    tree = ttk.Treeview(frame_ds, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=200)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)

    # === FORM NHẬP DỮ LIỆU ===
    form = tk.LabelFrame(win, text="Thông tin chi tiết hóa đơn", padx=10, pady=10, font=("Arial", 10, "bold"))
    form.pack(pady=10, padx=10, fill="x")

    entries = {}
    fields = ["MaHD", "MaXe", "SoLuong", "DonGia", "ThanhTien"]

    for i, c in enumerate(fields):
        tk.Label(form, text=c + ":", font=("Arial", 10)).grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=6, pady=4)
        e = tk.Entry(form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[c] = e

    # === CLEAR FORM ===
    def clear_form():
        for c in entries:
            entries[c].delete(0, tk.END)

    # === LOAD DỮ LIỆU ===
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search and search.strip():
                like = f"%{search.strip()}%"
                cursor.execute("""
                    SELECT MaHD, MaXe, SoLuong, DonGia, ThanhTien
                    FROM CTHoaDon
                    WHERE MaHD LIKE %s OR MaXe LIKE %s
                """, (like, like))
            else:
                cursor.execute("SELECT MaHD, MaXe, SoLuong, DonGia, ThanhTien FROM CTHoaDon ORDER BY MaHD ASC")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")

    # === THÊM TẠM ===
    def add_temp():
        vals = {c: entries[c].get().strip() for c in entries}
        if not vals["MaHD"] or not vals["MaXe"]:
            messagebox.showwarning("Chú ý", "Vui lòng nhập đầy đủ Mã HĐ và Mã Xe!")
            return
        for ct in temp_data:
            if ct["MaHD"] == vals["MaHD"] and ct["MaXe"] == vals["MaXe"]:
                messagebox.showwarning("Trùng dữ liệu", f"Chi tiết HĐ {vals['MaHD']} - {vals['MaXe']} đã có!")
                return
        try:
            sl = float(vals["SoLuong"]) if vals["SoLuong"] else 0
            dg = float(vals["DonGia"]) if vals["DonGia"] else 0
            vals["ThanhTien"] = sl * dg
        except:
            messagebox.showerror("Lỗi", "Số lượng hoặc đơn giá không hợp lệ!")
            return
        temp_data.append(vals)
        tree.insert("", tk.END, values=[vals.get(c, "") for c in columns])
        clear_form()

    # === LƯU VÀO CSDL ===
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for ct in temp_data:
                cursor.execute("""
                    INSERT INTO CTHoaDon (MaHD, MaXe, SoLuong, DonGia, ThanhTien)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ct["MaHD"], ct["MaXe"], ct["SoLuong"], ct["DonGia"], ct["ThanhTien"]))
            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả chi tiết hóa đơn vào cơ sở dữ liệu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")

    # === XÓA ===
    def delete_all():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn bản ghi để xóa!")
            return
        vals = tree.item(sel[0])['values']
        mahd, maxe = vals[0], vals[1]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa MaHD = {mahd}, MaXe = {maxe}?"):
            return
        temp_data[:] = [ct for ct in temp_data if not (ct["MaHD"] == mahd and ct["MaXe"] == maxe)]
        try:
            cursor.execute("DELETE FROM CTHoaDon WHERE MaHD = %s AND MaXe = %s", (mahd, maxe))
            conn.commit()
        except Exception:
            pass
        tree.delete(sel[0])
        clear_form()
        messagebox.showinfo("Đã xóa", f"Chi tiết hóa đơn {mahd} - {maxe} đã được xóa!")

    # === CHỌN TRONG DANH SÁCH ===
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])['values']
        for i, c in enumerate(columns):
            entries[c].delete(0, tk.END)
            entries[c].insert(0, vals[i])

    tree.bind("<<TreeviewSelect>>", on_select)

    # === NÚT CHỨC NĂNG ===
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Thêm tạm", width=12, command=add_temp, bg="#2196F3", fg="white").grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="Lưu", width=12, command=save_all, bg="#4CAF50", fg="white").grid(row=0, column=1, padx=6)
    tk.Button(btn_frame, text="Xóa", width=12, command=delete_all, bg="#f44336", fg="white").grid(row=0, column=2, padx=6)
    tk.Button(btn_frame, text="Hủy", width=12, command=clear_form, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=6)
    tk.Button(btn_frame, text="Quay lại", width=12,
              command=lambda: (win.destroy(), root.deiconify()), bg="#2196F3", fg="white").grid(row=0, column=4, padx=6)

    # === LOAD BAN ĐẦU ===
    load_data()
