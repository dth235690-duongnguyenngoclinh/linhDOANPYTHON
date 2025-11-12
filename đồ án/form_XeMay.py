import tkinter as tk
from tkinter import ttk, messagebox

def open_xe_form(root, conn):
    cursor = conn.cursor()
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Quản lý Xe Máy")
    win.geometry("1100x650")

    # === TIÊU ĐỀ ===
    tk.Label(win, text="QUẢN LÝ XE MÁY", font=("Arial", 19, "bold"), fg="#003399").pack(pady=10)

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

    # === KHUNG DANH SÁCH XE ===
    frame_ds = tk.LabelFrame(win, text="Danh sách xe máy", padx=10, pady=10, font=("Arial", 11, "bold"), fg="#003366")
    frame_ds.pack(padx=10, pady=10, fill="both", expand=True)

    scroll = tk.Scrollbar(frame_ds)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    columns = ["MaXe", "TenXe", "HangXe", "MauXe", "GiaXe", "SoLuong", "CreatedAt"]
    tree = ttk.Treeview(frame_ds, columns=columns, show="headings", yscrollcommand=scroll.set, height=12)
    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=140)
    tree.pack(fill="both", expand=True)
    scroll.config(command=tree.yview)

    # === FORM NHẬP DỮ LIỆU ===
    form = tk.LabelFrame(win, text="Thông tin xe máy", padx=10, pady=10, font=("Arial", 10, "bold"))
    form.pack(pady=10, padx=10, fill="x")

    entries = {}
    fields = ["MaXe", "TenXe", "HangXe", "MauXe", "GiaXe", "SoLuong"]

    for i, c in enumerate(fields):
        tk.Label(form, text=c + ":", font=("Arial", 10)).grid(row=i // 3, column=(i % 3) * 2, sticky="w", padx=6, pady=4)
        e = tk.Entry(form, width=25)
        e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=6, pady=4)
        entries[c] = e

    entries["MaXe"].config(state="readonly")

    # === SINH MÃ LIỀN MẠCH ===
    def next_maxe():
        try:
            cursor.execute("SELECT MaXe FROM XeMay ORDER BY MaXe ASC")
            db_ids = [row[0] for row in cursor.fetchall()]
            used_ids = set(db_ids + [int(x["MaXe"]) for x in temp_data])
            next_id = 1
            while next_id in used_ids:
                next_id += 1
            entries["MaXe"].config(state="normal")
            entries["MaXe"].delete(0, tk.END)
            entries["MaXe"].insert(0, str(next_id))
            entries["MaXe"].config(state="readonly")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tạo mã mới: {e}")

    # === XÓA FORM ===
    def clear_form():
        for c in entries:
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
            if c == "MaXe":
                entries[c].config(state="readonly")
        next_maxe()

    # === LOAD DỮ LIỆU ===
    def load_data(search=None):
        tree.delete(*tree.get_children())
        temp_data.clear()
        try:
            if search and search.strip():
                like = f"%{search.strip()}%"
                cursor.execute("""
                    SELECT MaXe, TenXe, HangXe, MauXe, GiaXe, SoLuong, CreatedAt
                    FROM XeMay
                    WHERE CAST(MaXe AS CHAR) LIKE %s 
                        OR TenXe LIKE %s 
                        OR HangXe LIKE %s 
                        OR MauXe LIKE %s
                        OR CAST(GiaXe AS CHAR) LIKE %s
                        OR CAST(SoLuong AS CHAR) LIKE %s
                        OR CAST(CreatedAt AS CHAR) LIKE %s
                """, (like, like, like, like, like, like, like))
            else:
                cursor.execute("SELECT MaXe, TenXe, HangXe, MauXe, GiaXe, SoLuong, CreatedAt FROM XeMay ORDER BY MaXe ASC")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            next_maxe()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")

    # === THÊM TẠM ===
    def add_temp():
        vals = {c: entries[c].get().strip() for c in entries}
        if not vals["TenXe"]:
            messagebox.showwarning("Chú ý", "Tên xe không được để trống!")
            return
        for xe in temp_data:
            if xe["MaXe"] == vals["MaXe"]:
                messagebox.showwarning("Trùng mã", f"Mã {vals['MaXe']} đã có trong danh sách tạm!")
                return
        temp_data.append(vals)
        tree.insert("", tk.END, values=[vals.get(c, "") for c in columns])
        clear_form()

    # === LƯU TẤT CẢ DỮ LIỆU VÀO DB ===
    def save_all():
        if not temp_data:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để lưu.")
            return
        try:
            for xe in temp_data:
                cursor.execute("""
                    INSERT INTO XeMay (TenXe, HangXe, MauXe, GiaXe, SoLuong)
                    VALUES (%s, %s, %s, %s, %s)
                """, (xe["TenXe"], xe["HangXe"], xe["MauXe"], xe["GiaXe"], xe["SoLuong"]))
            conn.commit()
            temp_data.clear()
            load_data()
            messagebox.showinfo("Thành công", "Đã lưu tất cả xe mới vào cơ sở dữ liệu!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {e}")

    # === XÓA XE (CẢ TRONG DB LẪN TẠM) ===
    def delete_all():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn bản ghi để xóa!")
            return
        maxe = str(tree.item(sel[0])['values'][0])
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa xe MaXe = {maxe}?"):
            return
        temp_data[:] = [xe for xe in temp_data if xe["MaXe"] != maxe]
        try:
            cursor.execute("DELETE FROM XeMay WHERE MaXe = %s", (maxe,))
            conn.commit()
        except Exception:
            pass
        tree.delete(sel[0])
        clear_form()
        messagebox.showinfo("Đã xóa", f"Xe MaXe {maxe} đã được xóa!")
        next_maxe()

    # === CHỌN TRONG DANH SÁCH ===
    def on_select(event):
        sel = tree.selection()
        if not sel: return
        vals = tree.item(sel[0])['values']
        for i, c in enumerate(columns[:-1]):
            entries[c].config(state="normal")
            entries[c].delete(0, tk.END)
            entries[c].insert(0, vals[i])
            if c == "MaXe":
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
