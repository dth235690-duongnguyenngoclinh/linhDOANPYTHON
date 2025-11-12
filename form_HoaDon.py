import tkinter as tk
from tkinter import ttk, messagebox
from form_KhachHang import open_kh_form   # ✅ thêm dòng này để mở form Khách hàng thật

def open_hd_form(root, conn):
    cursor = conn.cursor()
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Quản lý Hóa đơn")
    win.geometry("1150x700")

    # === DANH SÁCH TẠM ===
    temp_data = []

    # === TIÊU ĐỀ ===
    tk.Label(win, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 19, "bold"), fg="#003399").pack(pady=10)

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

    # === KHUNG DANH SÁCH HÓA ĐƠN ===
    frame_dshd = tk.LabelFrame(win, text="Danh sách hóa đơn", padx=10, pady=10, font=("Arial", 11, "bold"), fg="#003366")
    frame_dshd.pack(padx=10, pady=10, fill="both", expand=True)

    scroll = tk.Scrollbar(frame_dshd)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ["MaHD", "NgayBan", "MaKH", "MaNV", "TongTien", "GhiChu", "CreatedAt"]
    tree = ttk.Treeview(frame_dshd, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)

    # === FORM NHẬP DỮ LIỆU ===
    form = tk.LabelFrame(win, text="Thông tin hóa đơn", padx=10, pady=10, font=("Arial", 10, "bold"))
    form.pack(pady=10, padx=10, fill="x")

    entries = {}
    left_fields = ["MaHD", "NgayBan", "MaNV"]
    right_fields = ["TongTien", "GhiChu"]

    for i, c in enumerate(left_fields):
        tk.Label(form, text=c + ":", font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=6, pady=4)
        e = tk.Entry(form, width=30)
        e.grid(row=i, column=1, padx=6, pady=4)
        entries[c] = e

    entries["MaHD"].config(state="readonly")  # Mã tự động

    # === COMBOBOX KHÁCH HÀNG ===
    tk.Label(form, text="Khách hàng:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=6, pady=4)
    kh_var = tk.StringVar()
    cb_kh = ttk.Combobox(form, textvariable=kh_var, width=33)
    cb_kh.grid(row=3, column=1, padx=6, pady=4)
    entries["MaKH"] = cb_kh

    # Ô tìm khách
    tk.Entry(form, width=25, font=("Arial", 10), fg="#555").grid(row=3, column=2, padx=6, pady=4)
    tk.Button(form, text="🔍 Tìm khách", width=12, bg="#2196F3", fg="white",
              command=lambda: search_customer()).grid(row=3, column=3, padx=5)

    # ✅ Nút thêm khách thật (đã sửa)
    tk.Button(form, text="➕ Thêm khách", width=12, bg="#4CAF50", fg="white",
              command=lambda: open_kh_form(win, conn)).grid(row=3, column=4, padx=5)

    for i, c in enumerate(right_fields):
        tk.Label(form, text=c + ":", font=("Arial", 10)).grid(row=i+4, column=0, sticky="w", padx=6, pady=4)
        e = tk.Entry(form, width=30)
        e.grid(row=i+4, column=1, padx=6, pady=4)
        entries[c] = e

    # === SINH MÃ LIỀN MẠCH ===
    def next_mahd():
        try:
            cursor.execute("SELECT MaHD FROM HoaDon ORDER BY MaHD ASC")
            db_ids = [row[0] for row in cursor.fetchall()]
            used_ids = set(db_ids + [int(x["MaHD"]) for x in temp_data])
            next_id = 1
            while next_id in used_ids:
                next_id += 1
            entries["MaHD"].config(state="normal")
            entries["MaHD"].delete(0, tk.END)
            entries["MaHD"].insert(0, str(next_id))
            entries["MaHD"].config(state="readonly")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tạo mã mới: {e}")

    # === NẠP DANH SÁCH KHÁCH HÀNG ===
    def load_customers():
        try:
            cursor.execute("SELECT MaKH, TenKH, SDT FROM KhachHang ORDER BY MaKH ASC")
            rows = cursor.fetchall()
            cb_kh['values'] = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải khách hàng: {e}")

    # === TÌM KHÁCH ===
    def search_customer():
        keyword = kh_var.get().strip()
        if not keyword:
            messagebox.showinfo("Thông báo", "Nhập tên hoặc số điện thoại khách để tìm.")
            return
        cursor.execute("""
            SELECT MaKH, TenKH, SDT FROM KhachHang
            WHERE TenKH LIKE %s OR SDT LIKE %s OR MaKH LIKE %s
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        if not rows:
            messagebox.showinfo("Kết quả", "Không tìm thấy khách hàng phù hợp.")
        else:
            cb_kh['values'] = [f"{r[0]} - {r[1]} ({r[2]})" for r in rows]
            cb_kh.current(0)

    # === XÓA FORM ===
    def clear_form():
        for c in entries:
            entries[c].config(state="normal")
            if hasattr(entries[c], "delete"):
                entries[c].delete(0, tk.END)
            if c == "MaHD":
                entries[c].config(state="readonly")
        next_mahd()

    # === LOAD DỮ LIỆU ===
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search and search.strip():
                text = search.strip()
                if ":" in text:
                    field, value = text.split(":", 1)
                    field, value = field.strip(), value.strip()
                    cursor.execute(f"SELECT * FROM HoaDon WHERE {field} LIKE %s", (f"%{value}%",))
                else:
                    like = f"%{text}%"
                    cursor.execute("""
                        SELECT * FROM HoaDon
                        WHERE MaHD LIKE %s OR NgayBan LIKE %s OR MaKH LIKE %s
                        OR MaNV LIKE %s OR TongTien LIKE %s OR GhiChu LIKE %s OR CreatedAt LIKE %s
                    """, (like, like, like, like, like, like, like))
            else:
                cursor.execute("SELECT * FROM HoaDon ORDER BY MaHD ASC")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            next_mahd()
            load_customers()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    # === THÊM TẠM ===
    def add_temp():
        vals = {c: entries[c].get().strip() for c in entries}
        if not vals["NgayBan"]:
            messagebox.showwarning("Chú ý", "Ngày bán không được để trống")
            return
        if not vals["MaKH"]:
            messagebox.showwarning("Chú ý", "Vui lòng chọn khách hàng")
            return
        # kiểm tra trùng mã
        for hd in temp_data:
            if hd["MaHD"] == vals["MaHD"]:
                messagebox.showwarning("Trùng mã", f"Mã {vals['MaHD']} đã có trong danh sách tạm!")
                return
        temp_data.append(vals)
        tree.insert("", tk.END, values=[vals.get(c, "") for c in columns])
        clear_form()

    # === LƯU DỮ LIỆU TẠM VÀO DB ===
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for hd in temp_data:
                cursor.execute("""
                    INSERT INTO HoaDon (MaHD, NgayBan, MaKH, MaNV, TongTien, GhiChu)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (hd["MaHD"], hd["NgayBan"], hd["MaKH"].split(" ")[0], hd["MaNV"], hd["TongTien"], hd["GhiChu"]))
            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả hóa đơn mới!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")

    # === XÓA CẢ TRONG DB LẪN TẠM ===
    def delete_all():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn bản ghi để xóa!")
            return
        mahd = str(tree.item(sel[0])['values'][0])
        if not mahd:
            return
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa hóa đơn MaHD = {mahd}?"):
            return

        temp_data[:] = [hd for hd in temp_data if hd["MaHD"] != mahd]
        try:
            cursor.execute("DELETE FROM HoaDon WHERE MaHD = %s", (mahd,))
            conn.commit()
        except Exception:
            pass

        tree.delete(sel[0])
        clear_form()
        messagebox.showinfo("Đã xóa", f"Hóa đơn {mahd} đã được xóa khỏi tất cả dữ liệu!")
        next_mahd()

    # === CHỌN TRONG TREEVIEW ===
    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])['values']
        for i, c in enumerate(columns):
            if c in entries:
                entries[c].config(state="normal")
                entries[c].delete(0, tk.END)
                entries[c].insert(0, vals[i])
                if c == "MaHD":
                    entries[c].config(state="readonly")

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

    load_data()
