import tkinter as tk
from tkinter import ttk, messagebox

def open_kh_form(root, conn, callback=None):
    cursor = conn.cursor()
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Quản lý Khách hàng")
    win.geometry("1200x700")
    win.configure(bg="#f2f2f2")

    # ======= TIÊU ĐỀ =======
    tk.Label(win, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 20, "bold"), fg="#003399", bg="#f2f2f2").pack(pady=10)

    # ======= THANH TÌM KIẾM =======
    search_frame = tk.Frame(win, bg="#f2f2f2")
    search_frame.pack(fill="x", padx=30, pady=5)
    tk.Label(search_frame, text="🔍 Tìm kiếm:", font=("Arial", 11), bg="#f2f2f2").pack(side="left")
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=50, font=("Arial", 11)).pack(side="left", padx=8)
    tk.Button(search_frame, text="Tìm", bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
              width=10, command=lambda: load_data(search_var.get())).pack(side="left", padx=5)
    tk.Button(search_frame, text="Tải lại", bg="#6c757d", fg="white", font=("Arial", 10, "bold"),
              width=10, command=lambda: (search_var.set(""), load_data())).pack(side="left", padx=5)

    # ======= DANH SÁCH KHÁCH HÀNG =======
    list_frame = tk.LabelFrame(win, text="Danh sách khách hàng", font=("Arial", 12, "bold"), bg="#ffffff")
    list_frame.pack(fill="both", expand=True, padx=30, pady=5)

    columns = ["MaKH", "TenKH", "DiaChi", "SDT", "Email", "CreatedAt"]
    tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=180 if c != "DiaChi" else 250)
    tree.pack(fill="both", expand=True, pady=5)

    scroll_y = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    scroll_y.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scroll_y.set)

    # ======= KHUNG NHẬP THÔNG TIN =======
    info_frame = tk.LabelFrame(win, text="Thông tin khách hàng", font=("Arial", 12, "bold"), bg="#ffffff")
    info_frame.pack(fill="x", padx=30, pady=5)

    fields = ["MaKH", "TenKH", "DiaChi", "SDT", "Email"]
    entries = {}

    # Chia bố cục 2 hàng, 3 cột
    positions = [
        ("MaKH", 0, 0), ("TenKH", 0, 2), ("DiaChi", 1, 0),
        ("SDT", 1, 2), ("Email", 2, 0)
    ]

    for field, r, c in positions:
        tk.Label(info_frame, text=field + ":", font=("Arial", 11), bg="#ffffff").grid(row=r, column=c, padx=10, pady=6, sticky="w")
        e = tk.Entry(info_frame, width=40)
        e.grid(row=r, column=c + 1, padx=10, pady=6, sticky="w")
        entries[field] = e

    # ======= FRAME NÚT CHỨC NĂNG =======
    btn_frame = tk.Frame(win, bg="#f2f2f2")
    btn_frame.pack(pady=10)

    btn_style = {"font": ("Arial", 10, "bold"), "width": 12, "fg": "white"}

    # === HÀM XỬ LÝ ===
    def clear_entries():
        for e in entries.values():
            e.delete(0, tk.END)
        search_var.set("")

    def load_data(search=None):
        tree.delete(*tree.get_children())
        try:
            if search and search.strip():
                like = f"%{search.strip()}%"
                cursor.execute("""
                    SELECT MaKH, TenKH, DiaChi, SDT, Email, CreatedAt
                    FROM KhachHang
                    WHERE MaKH LIKE %s OR TenKH LIKE %s OR DiaChi LIKE %s
                        OR SDT LIKE %s OR Email LIKE %s
                """, (like, like, like, like, like))
            else:
                cursor.execute("SELECT MaKH, TenKH, DiaChi, SDT, Email, CreatedAt FROM KhachHang")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=[str(v) if v is not None else "" for v in row])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tải dữ liệu: {e}")

    def add_temp():
        vals = [entries[c].get().strip() for c in fields]
        if not vals[0] or not vals[1]:
            messagebox.showwarning("Chú ý", "Vui lòng nhập đầy đủ Mã KH và Tên KH!")
            return
        for i in range(len(vals), len(columns)):
            vals.append("")
        tree.insert("", tk.END, values=vals)
        clear_entries()

    def save_data():
        try:
            cursor.execute("DELETE FROM KhachHang")
            for child in tree.get_children():
                vals = tree.item(child)["values"][:5]
                cursor.execute("""
                    INSERT INTO KhachHang (MaKH, TenKH, DiaChi, SDT, Email)
                    VALUES (%s, %s, %s, %s, %s)
                """, vals)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã lưu toàn bộ danh sách khách hàng!")
            load_data()
            if callback:
                callback()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")

    def delete_record():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn khách hàng cần xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Xóa khách hàng đã chọn?"):
            for s in sel:
                tree.delete(s)

    def on_select(event):
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0])["values"]
        for i, f in enumerate(fields):
            entries[f].delete(0, tk.END)
            if i < len(vals):
                entries[f].insert(0, vals[i])

    tree.bind("<<TreeviewSelect>>", on_select)

    # ======= CÁC NÚT =======
    tk.Button(btn_frame, text="Thêm tạm", bg="#2196F3", command=add_temp, **btn_style).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="Lưu", bg="#4CAF50", command=save_data, **btn_style).grid(row=0, column=1, padx=6)
    tk.Button(btn_frame, text="Xóa", bg="#F44336", command=delete_record, **btn_style).grid(row=0, column=2, padx=6)
    tk.Button(btn_frame, text="Hủy", bg="#6c757d", command=clear_entries, **btn_style).grid(row=0, column=3, padx=6)
    tk.Button(btn_frame, text="Quay lại", bg="#003399",
              command=lambda: (win.destroy(), root.deiconify(), callback() if callback else None),
              **btn_style).grid(row=0, column=4, padx=6)

    # ======= SỰ KIỆN ĐÓNG =======
    def on_close():
        win.destroy()
        root.deiconify()
        if callback:
            callback()

    win.protocol("WM_DELETE_WINDOW", on_close)
    load_data()
    
    #
