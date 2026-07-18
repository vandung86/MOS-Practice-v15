import tkinter as tk
from tkinter import messagebox, Menu
import time, threading, os, sys
import requests # Cần cài đặt: pip install requests

try:
    import win32gui, win32con, win32com.client, pygetwindow as gw
except ImportError:
    pass

class MOSPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MOS Practice Bar")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # CẤU HÌNH CLOUD (Thay link của bạn vào đây)
        self.BASE_CLOUD_URL = "https://github.com/vandung86/MOS2019.git"
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.app_height = 200
        self.position_mode = "bottom"
        self.MOS_COLOR = "#062852" 
        
        self.projects_data = self.load_questions()
        self.task_statuses = {} 
        self.current_project_idx = 0
        self.current_task_idx = 0
        self.elapsed_seconds = 0
        
        self.update_window_geometry()
        self.root.configure(bg="#F8FAFC")
        self.setup_ui()
        self.start_timer()
        self.open_word_file_for_project(0)

    # --- HÀM HỖ TRỢ ---
    def get_base_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    # --- TẢI FILE TỪ CLOUD ---
    def download_word_from_cloud(self, filename):
        local_path = os.path.join(self.get_base_path(), filename)
        if not os.path.exists(local_path):
            try:
                # Tải file từ Cloud
                url = self.BASE_CLOUD_URL + filename
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
            except:
                pass
        return local_path

    def close_word_without_saving(self, keyword=None):
        try:
            app = win32com.client.GetActiveObject("Word.Application")
            for doc in list(app.Documents):
                if keyword is None or (doc.Name and keyword.lower() in doc.Name.lower()):
                    doc.Close(SaveChanges=0)
            if app.Documents.Count == 0: app.Quit()
        except: pass

    def close_application(self):
        self.close_word_without_saving()
        self.root.destroy()
        sys.exit()

    def mark_task(self, status):
        key = (self.current_project_idx, self.current_task_idx)
        self.task_statuses[key] = status
        self.update_display()

    # --- SETUP UI ---
    def setup_ui(self):
        top_bar = tk.Frame(self.root, bg=self.MOS_COLOR, height=45)
        top_bar.pack(fill="x", side="top")
        
        # BRANDING
        brand_frame = tk.Frame(top_bar, bg=self.MOS_COLOR)
        brand_frame.pack(side="left", padx=10)
        try:
            logo_path = os.path.join(self.get_base_path(), "logo.png")
            if os.path.exists(logo_path):
                self.logo_img = tk.PhotoImage(file=logo_path)
                tk.Label(brand_frame, image=self.logo_img, bg=self.MOS_COLOR).pack(side="left")
        except: pass
        tk.Label(brand_frame, text="MyBrand", bg=self.MOS_COLOR, fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)

        # CONTROLS
        left = tk.Frame(top_bar, bg=self.MOS_COLOR)
        left.pack(side="left", padx=10)
        
        self.lbl_timer = tk.Label(left, text="⏱ 00:00", bg="#041b38", fg="white", font=("Segoe UI", 12, "bold"), padx=10)
        self.lbl_timer.pack(side="left", padx=5)
        self.create_btn(left, "↕ Vị trí", self.toggle_position, "#041b38", padx=8).pack(side="left", padx=5)
        
        self.btn_select = tk.Menubutton(left, text="Select Project", bg="#041b38", fg="white", font=("Segoe UI", 9, "bold"), padx=8, pady=5, cursor="hand2")
        self.menu_proj = Menu(self.btn_select, tearoff=0)
        for i, p in enumerate(self.projects_data):
            self.menu_proj.add_command(label=p["name"], command=lambda idx=i: self.jump_to_project(idx))
        self.btn_select["menu"] = self.menu_proj
        self.btn_select.pack(side="left", padx=5)

        # Title (Canh giữa)
        self.title_cont = tk.Frame(top_bar, bg=self.MOS_COLOR)
        self.title_cont.pack(side="left", expand=True)
        self.lbl_title_prefix = tk.Label(self.title_cont, bg=self.MOS_COLOR, fg="#A0AEC0", font=("Segoe UI", 11))
        self.lbl_title_prefix.pack(side="left")
        self.lbl_title_name = tk.Label(self.title_cont, bg=self.MOS_COLOR, fg="#FFFFFF", font=("Segoe UI", 13, "bold"))
        self.lbl_title_name.pack(side="left")

        # Right Group
        right = tk.Frame(top_bar, bg=self.MOS_COLOR)
        right.pack(side="right", padx=10)
        self.create_btn(right, "Restart", self.restart_project, "#4A5568").pack(side="left", padx=5)
        self.create_btn(right, "Submit", self.submit_project, "#059669").pack(side="left", padx=5)
        self.create_btn(right, "✖", self.close_application, "#C53030").pack(side="left", padx=5)

        self.task_bar = tk.Frame(self.root, bg="#F8FAFC", height=40)
        self.task_bar.pack(fill="x")
        self.task_frame = tk.Frame(self.task_bar, bg="#F8FAFC")
        self.task_frame.pack(pady=5)
        
        # Khung văn bản (padx=300)
        self.instruction_container = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        self.instruction_container.pack(fill="x", padx=300, pady=8) 
        
        self.lbl_inst = tk.Label(self.instruction_container, bg="white", fg="#2D3748", 
                                 font=("Segoe UI", 12), wraplength=900, justify="center", padx=10, pady=10)
        self.lbl_inst.pack(fill="both", expand=True)
        
        # Footer
        footer = tk.Frame(self.root, bg="white", height=45)
        footer.pack(fill="x", side="bottom")
        btn_c = tk.Frame(footer, bg="white")
        btn_c.pack(pady=5)
        self.create_btn(btn_c, "✓ Mark Complete", lambda: self.mark_task("completed"), "#E2E8F0", "#4A5568", font=("Segoe UI", 8, "bold"), padx=12, pady=3).pack(side="left", padx=10)
        self.create_btn(btn_c, "⚐ Mark for Review", lambda: self.mark_task("review"), "#E2E8F0", "#4A5568", font=("Segoe UI", 8, "bold"), padx=12, pady=3).pack(side="left", padx=10)
        
        self.update_display()

    # --- LOGIC ---
    def update_display(self):
        for w in self.task_frame.winfo_children(): w.destroy()
        tasks = self.projects_data[self.current_project_idx]["tasks"]
        self.lbl_title_prefix.config(text=f"Project {self.current_project_idx + 1} of {len(self.projects_data)}: ")
        self.lbl_title_name.config(text=f"{self.projects_data[self.current_project_idx]['name']}")
        
        # Nút Prev
        self.create_btn(self.task_frame, "◀ Prev", self.prev_task, "#4A5568", font=("Segoe UI", 9), padx=10, pady=3).pack(side="left", padx=10)
        
        for i in range(len(tasks)):
            status = self.task_statuses.get((self.current_project_idx, i))
            icon = " ✔" if status == "completed" else (" ⚐" if status == "review" else "")
            if status == "completed": bg = "#48BB78"
            elif status == "review": bg = "#ED8936"
            else: bg = "#3182CE" if i == self.current_task_idx else "#E2E8F0"
            fg = "white" if bg != "#E2E8F0" else "#4A5568"
            tk.Button(self.task_frame, text=f"{i+1}{icon}", bg=bg, fg=fg, bd=0, padx=10, pady=3, 
                      command=lambda idx=i: self.select_task(idx)).pack(side="left", padx=3)
        
        # Nút Next
        self.create_btn(self.task_frame, "Next Task ▶", self.next_task, "#059669", font=("Segoe UI", 9), padx=10, pady=3).pack(side="left", padx=10)
        self.lbl_inst.config(text=tasks[self.current_task_idx])

    def create_btn(self, parent, text, cmd, bg, fg="white", font=("Segoe UI", 9, "bold"), padx=12, pady=5):
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg, font=font, bd=0, padx=padx, pady=pady, cursor="hand2")

    def toggle_position(self):
        self.position_mode = "top" if self.position_mode == "bottom" else "bottom"
        self.update_window_geometry()
        threading.Thread(target=self.autofit, args=(self.projects_data[self.current_project_idx]["name"],), daemon=True).start()

    def select_task(self, idx): self.current_task_idx = idx; self.update_display()
    def next_task(self): 
        if self.current_task_idx < len(self.projects_data[self.current_project_idx]["tasks"]) - 1: self.select_task(self.current_task_idx + 1)
    
    def prev_task(self):
        if self.current_task_idx > 0: self.select_task(self.current_task_idx - 1)
    
    def jump_to_project(self, idx):
        self.close_word_without_saving(self.projects_data[self.current_project_idx]["name"])
        self.current_project_idx = idx; self.current_task_idx = 0; self.update_display(); self.open_word_file_for_project(idx)
    
    def restart_project(self):
        if messagebox.askyesno("Restart", "Khởi động lại Project này (Không lưu)?"):
            self.close_word_without_saving(self.projects_data[self.current_project_idx]["name"])
            self.open_word_file_for_project(self.current_project_idx)
            
    def submit_project(self):
        if messagebox.askyesno("Submit", "Nộp bài và chuyển sang Project tiếp theo?"):
            self.close_word_without_saving(self.projects_data[self.current_project_idx]["name"])
            if self.current_project_idx < len(self.projects_data) - 1: self.jump_to_project(self.current_project_idx + 1)
            else: messagebox.showinfo("Hoàn thành", "Chúc mừng, bạn đã xong!")
    
    def load_questions(self):
        projects = []
        lines = []
        
        # 1. Thử tải từ Cloud
        try:
            print(f"Đang thử tải từ: {self.BASE_CLOUD_URL}questions.txt")
            response = requests.get(self.BASE_CLOUD_URL + "questions.txt", timeout=5)
            if response.status_code == 200:
                lines = response.text.splitlines()
                print("Tải từ Cloud thành công!")
            else:
                print(f"Lỗi Cloud: Status code {response.status_code}")
        except Exception as e:
            print(f"Không thể kết nối Cloud: {e}")
        
        # 2. Nếu không có dữ liệu từ Cloud, thử tải local
        if not lines:
            path = os.path.join(self.get_base_path(), "questions.txt")
            if os.path.exists(path):
                print(f"Đang đọc từ file local: {path}")
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            else:
                print("Không tìm thấy file questions.txt local.")

        # 3. Phân tích dữ liệu
        curr = None
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith("#"):
                curr = {"name": line.replace("#", "").strip(), "tasks": []}
                projects.append(curr)
            elif curr:
                curr["tasks"].append(line)
        
        # 4. TRÁNH LỖI CRASH: Nếu vẫn không có project nào, trả về project mặc định
        if not projects:
            print("CẢNH BÁO: Không tìm thấy dữ liệu Project hợp lệ!")
            return [{"name": "Error_No_Data", "tasks": ["Vui lòng kiểm tra file questions.txt", "Phải bắt đầu bằng dấu #"]}]
            
        return projects

    def update_window_geometry(self):
        y = (self.screen_height - self.app_height - 40) if self.position_mode == "bottom" else 0
        self.root.geometry(f"{self.screen_width}x{self.app_height}+0+{y}")
        self.root.update_idletasks()

    def open_word_file_for_project(self, idx):
        name = self.projects_data[idx]["name"]
        # Gọi hàm download trước khi mở
        path = self.download_word_from_cloud(f"{name}.docx")
        if os.path.exists(path):
            os.startfile(path)
            threading.Thread(target=self.autofit, args=(name,), daemon=True).start()
        
    def autofit(self, keyword):
        time.sleep(1.2)
        try:
            for window in gw.getAllWindows():
                if keyword.lower() in window.title.lower() or "word" in window.title.lower():
                    win32gui.ShowWindow(window._hWnd, win32con.SW_SHOWNORMAL)
                    y = 0 if self.position_mode == "bottom" else self.app_height
                    win32gui.SetWindowPos(window._hWnd, win32con.HWND_NOTOPMOST, 0, y, self.screen_width, self.screen_height - self.app_height - 45, win32con.SWP_SHOWWINDOW)
                    break
        except: pass

    def start_timer(self):
        def count():
            while True:
                time.sleep(1)
                self.elapsed_seconds += 1
                minutes = self.elapsed_seconds // 60
                seconds = self.elapsed_seconds % 60
                self.lbl_timer.config(text=f"⏱ {minutes:02d}:{seconds:02d}")
        threading.Thread(target=count, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MOSPracticeApp(root)
    root.mainloop()
