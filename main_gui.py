import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import math

from modules.sheet_metal import SheetMetalModule
from modules.trusses import TrussModule
from modules.machine_3d import Machine3DModule
from modules.gears_gearbox import GearsAndGearboxModule
from modules.unit_converter import UnitAndPhysicsModule
from modules.electronics import ElectronicsModule

class EngineeringSuiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("المنظومة الهندسية الشاملة - مع المعاينة البصرية 2D")
        self.root.geometry("1220x740")
        self.root.configure(bg="#0d1b2a")

        self.db_modules = {
            "sheet": SheetMetalModule(),
            "truss": TrussModule(),
            "gearbox": GearsAndGearboxModule(),
            "cad3d": Machine3DModule(),
            "units": UnitAndPhysicsModule(),
            "elec": ElectronicsModule()
        }

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0d1b2a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1b263b", foreground="#00f5d4", padding=[10, 5], font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#415a77")], foreground=[("selected", "#ffd166")])
        style.configure("TFrame", background="#1b263b")
        style.configure("TLabel", background="#1b263b", foreground="#e0e1dd", font=("Arial", 10))
        style.configure("TButton", background="#00bbf9", foreground="#000000", font=("Arial", 10, "bold"), padding=6)

    def create_widgets(self):
        header = tk.Label(self.root, text="نظام الهندسة والفيزياء وتصميم الماكينات والجيربوكس (معاينة بصرية 2D)", bg="#0d1b2a", fg="#ffd166", font=("Arial", 15, "bold"), pady=8)
        header.pack(fill="x")

        # تقسيم الشاشة: اليسار للإدخال والنتائج، واليمين لنافذة المعاينة البصرية
        main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#0d1b2a", sashwidth=6)
        main_pane.pack(expand=True, fill="both", padx=10, pady=5)

        left_frame = tk.Frame(main_pane, bg="#0d1b2a")
        right_frame = tk.Frame(main_pane, bg="#09121c", bd=2, relief="groove")
        main_pane.add(left_frame, width=720)
        main_pane.add(right_frame, width=480)

        # إعداد نافذة المعاينة البصرية في الجانب الأيمن
        vis_title = tk.Label(right_frame, text="نافذة المعاينة الهندسية ثنائية الأبعاد (2D CAD Preview)", bg="#1b263b", fg="#00f5d4", font=("Arial", 11, "bold"), pady=6)
        vis_title.pack(fill="x")

        self.canvas = tk.Canvas(right_frame, bg="#050b14", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=5, pady=5)
        self.draw_grid()

        # التبويبات وصندوق النتائج في الجانب الأيسر
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(expand=True, fill="both")

        self.build_sheet_tab()
        self.build_truss_tab()
        self.build_gearbox_tab()
        self.build_3d_tab()
        self.build_units_tab()
        self.build_elec_tab()

        res_label = tk.Label(left_frame, text="مخرجات الحسابات ومسارات الملفات (DXF / STEP):", bg="#0d1b2a", fg="#00f5d4", font=("Arial", 10, "bold"))
        res_label.pack(anchor="e", pady=(5, 0))

        self.output_box = scrolledtext.ScrolledText(left_frame, height=11, bg="#09121c", fg="#00ff88", font=("Consolas", 10))
        self.output_box.pack(fill="x", pady=(2, 5))
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(0, 800, 25):
            self.canvas.create_line([(i, 0), (i, 800)], fill="#102035")
            self.canvas.create_line([(0, i), (800, i)], fill="#102035")

    def show_result(self, data):
        self.output_box.delete("1.0", tk.END)
        formatted = json.dumps(data, ensure_ascii=False, indent=4)
        self.output_box.insert(tk.END, formatted)

    def preview_cone(self, res):
        self.draw_grid()
        if "خطأ" in res:
            return
        R1 = res["نصف_قطر_البرجل_الكبير_R1"]
        R2 = res["نصف_قطر_البرجل_الصغير_R2"]
        angle = res["زاوية_التقطيع_بالدرجات"]

        cx, cy = 230, 320
        scale = 180.0 / R1
        r1_s, r2_s = R1 * scale, R2 * scale

        # رسم القوسين الخارجي والداخلي للمسلوب المفرود
        self.canvas.create_arc(cx - r1_s, cy - r1_s, cx + r1_s, cy + r1_s, start=0, extent=angle, style=tk.ARC, outline="#00f5d4", width=2)
        self.canvas.create_arc(cx - r2_s, cy - r2_s, cx + r2_s, cy + r2_s, start=0, extent=angle, style=tk.ARC, outline="#ffd166", width=2)

        rad = math.radians(angle)
        self.canvas.create_line(cx + r2_s, cy, cx + r1_s, cy, fill="#ff006e", width=2)
        self.canvas.create_line(cx + r2_s * math.cos(rad), cy - r2_s * math.sin(rad), cx + r1_s * math.cos(rad), cy - r1_s * math.sin(rad), fill="#ff006e", width=2)
        self.canvas.create_text(230, 30, text=f"تفريد المسلوب | الزاوية: {angle}°", fill="#ffffff", font=("Arial", 11, "bold"))

    def preview_truss(self, span, ch, sh, panels):
        self.draw_grid()
        if panels % 2 != 0:
            panels += 1
        scale_x = 400.0 / span
        scale_y = 220.0 / max(ch, sh, 1)
        ox, oy = 35, 360

        half_span = span / 2.0
        panel_w = span / panels
        rise = ch - sh

        # الوتر السفلي والعلوي
        self.canvas.create_line(ox, oy, ox + span * scale_x, oy, fill="#00f5d4", width=3)
        self.canvas.create_line(ox, oy - sh * scale_y, ox + half_span * scale_x, oy - ch * scale_y, fill="#ffd166", width=3)
        self.canvas.create_line(ox + half_span * scale_x, oy - ch * scale_y, ox + span * scale_x, oy - sh * scale_y, fill="#ffd166", width=3)

        for i in range(panels + 1):
            x = i * panel_w
            y_top = sh + (rise * (x / half_span)) if x <= half_span else sh + (rise * ((span - x) / half_span))
            self.canvas.create_line(ox + x * scale_x, oy, ox + x * scale_x, oy - y_top * scale_y, fill="#00bbf9", width=2)
            if i < panels:
                xn = (i + 1) * panel_w
                yn = sh + (rise * (xn / half_span)) if xn <= half_span else sh + (rise * ((span - xn) / half_span))
                if xn <= half_span:
                    self.canvas.create_line(ox + x * scale_x, oy, ox + xn * scale_x, oy - yn * scale_y, fill="#ff006e", width=1.5)
                else:
                    self.canvas.create_line(ox + x * scale_x, oy - y_top * scale_y, ox + xn * scale_x, oy, fill="#ff006e", width=1.5)

        self.canvas.create_text(230, 30, text=f"مخطط الجمالون | البحر: {span}م | الباكيات: {panels}", fill="#ffffff", font=("Arial", 11, "bold"))

    def preview_gearbox(self, res):
        self.draw_grid()
        stages = res.get("تفاصيل_المراحل", [])
        if not stages:
            return
        x_pos = 65
        cy = 240
        max_d = max([max(s["قطر_القائد_الخارجي_مم"], s["قطر_المنقاد_الخارجي_مم"]) for s in stages])
        scale = 95.0 / max(max_d, 1)

        for s in stages:
            r1 = (s["قطر_القائد_الخارجي_مم"] / 2.0) * scale
            r2 = (s["قطر_المنقاد_الخارجي_مم"] / 2.0) * scale
            self.canvas.create_oval(x_pos - r1, cy - r1, x_pos + r1, cy + r1, outline="#00f5d4", width=2)
            x_pos += r1 + r2
            self.canvas.create_oval(x_pos - r2, cy - r2, x_pos + r2, cy + r2, outline="#ffd166", width=2)
            self.canvas.create_text(x_pos, cy + r2 + 18, text=f"{s['السرعة_الفعلية_الناتجة']} RPM\n({s['الاتجاه']})", fill="#00ff88", font=("Arial", 8))
            x_pos += r2 + 25

        self.canvas.create_text(230, 30, text="تخطيط تروس الجيربوكس متعدد المراحل", fill="#ffffff", font=("Arial", 11, "bold"))
    def build_sheet_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="1. الصاج والمسلوب")

        ttk.Label(tab, text="تفريد المسلوب (Frustum) وتصدير أوتوكاد DXF:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, pady=8, padx=10, sticky="w")
        ttk.Label(tab, text="القطر الكبير (مم):").grid(row=1, column=0, padx=5, pady=5)
        e_d1 = ttk.Entry(tab, width=12); e_d1.insert(0, "1000"); e_d1.grid(row=1, column=1)

        ttk.Label(tab, text="القطر الصغير (مم):").grid(row=1, column=2, padx=5, pady=5)
        e_d2 = ttk.Entry(tab, width=12); e_d2.insert(0, "400"); e_d2.grid(row=1, column=3)

        ttk.Label(tab, text="الارتفاع (مم):").grid(row=2, column=0, padx=5, pady=5)
        e_h = ttk.Entry(tab, width=12); e_h.insert(0, "800"); e_h.grid(row=2, column=1)

        def run_cone():
            res = self.db_modules["sheet"].calculate_and_export_cone(float(e_d1.get()), float(e_d2.get()), float(e_h.get()))
            self.show_result(res)
            self.preview_cone(res)

        ttk.Button(tab, text="احسب وارسم وصدر DXF", command=run_cone).grid(row=2, column=2, columnspan=2, pady=8)

        ttk.Label(tab, text="حساب الخزان (التكعيب):", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=4, pady=8, padx=10, sticky="w")
        ttk.Label(tab, text="الطول (م):").grid(row=4, column=0); e_tl = ttk.Entry(tab, width=12); e_tl.insert(0, "3"); e_tl.grid(row=4, column=1)
        ttk.Label(tab, text="العرض (م):").grid(row=4, column=2); e_tw = ttk.Entry(tab, width=12); e_tw.insert(0, "2"); e_tw.grid(row=4, column=3)
        ttk.Label(tab, text="الارتفاع (م):").grid(row=5, column=0); e_th = ttk.Entry(tab, width=12); e_th.insert(0, "1.5"); e_th.grid(row=5, column=1)
        ttk.Button(tab, text="احسب تكعيب الخزان", command=lambda: self.show_result(
            self.db_modules["sheet"].calculate_tank(float(e_tl.get()), float(e_tw.get()), float(e_th.get()))
        )).grid(row=5, column=2, columnspan=2, pady=5)

    def build_truss_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="2. الجمالونات")

        ttk.Label(tab, text="بحر الجمالون (م):").grid(row=0, column=0, padx=8, pady=10)
        e_span = ttk.Entry(tab, width=12); e_span.insert(0, "12"); e_span.grid(row=0, column=1)

        ttk.Label(tab, text="ارتفاع المنتصف (م):").grid(row=0, column=2, padx=8)
        e_ch = ttk.Entry(tab, width=12); e_ch.insert(0, "2.5"); e_ch.grid(row=0, column=3)

        ttk.Label(tab, text="ارتفاع الأطراف (م):").grid(row=1, column=0, padx=8, pady=10)
        e_sh = ttk.Entry(tab, width=12); e_sh.insert(0, "1.0"); e_sh.grid(row=1, column=1)

        ttk.Label(tab, text="عدد الباكيات:").grid(row=1, column=2, padx=8)
        e_pan = ttk.Entry(tab, width=12); e_pan.insert(0, "8"); e_pan.grid(row=1, column=3)

        def run_truss():
            sp, ch, sh, pn = float(e_span.get()), float(e_ch.get()), float(e_sh.get()), int(e_pan.get())
            res = self.db_modules["truss"].design_gable_truss(sp, ch, sh, pn)
            self.show_result(res)
            self.preview_truss(sp, ch, sh, pn)

        ttk.Button(tab, text="تصميم ومعاينة الجمالون DXF", command=run_truss).grid(row=2, column=0, columnspan=4, pady=12)

    def build_gearbox_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="3. الجيربوكس والتروس")

        ttk.Label(tab, text="حساب الطنابير والسيور:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)
        ttk.Label(tab, text="قطر 1 (مم):").grid(row=1, column=0); e_p1 = ttk.Entry(tab, width=8); e_p1.insert(0, "100"); e_p1.grid(row=1, column=1)
        ttk.Label(tab, text="RPM:").grid(row=1, column=2); e_prpm = ttk.Entry(tab, width=8); e_prpm.insert(0, "1400"); e_prpm.grid(row=1, column=3)
        ttk.Label(tab, text="قطر 2 (مم):").grid(row=1, column=4); e_p2 = ttk.Entry(tab, width=8); e_p2.insert(0, "300"); e_p2.grid(row=1, column=5)
        ttk.Button(tab, text="احسب", command=lambda: self.show_result(
            self.db_modules["gearbox"].calculate_pulley_drive(float(e_p1.get()), float(e_prpm.get()), float(e_p2.get()))
        )).grid(row=1, column=6, padx=4)

        ttk.Label(tab, text="تصميم جيربوكس متعدد التروس:", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=6, sticky="w", padx=10, pady=(12, 4))
        ttk.Label(tab, text="سرعة الدخول:").grid(row=3, column=0); e_in_rpm = ttk.Entry(tab, width=8); e_in_rpm.insert(0, "1500"); e_in_rpm.grid(row=3, column=1)
        ttk.Label(tab, text="الاتجاه:").grid(row=3, column=2); e_in_dir = ttk.Entry(tab, width=8); e_in_dir.insert(0, "CW"); e_in_dir.grid(row=3, column=3)
        ttk.Label(tab, text="الموديول:").grid(row=3, column=4); e_mod = ttk.Entry(tab, width=8); e_mod.insert(0, "3.0"); e_mod.grid(row=3, column=5)

        ttk.Label(tab, text="المراحل (السرعة,الاتجاه مفصولة بـ ;):").grid(row=4, column=0, columnspan=6, sticky="w", padx=10, pady=4)
        e_stages = ttk.Entry(tab, width=52)
        e_stages.insert(0, "500,CCW ; 125,CW ; 40,CCW")
        e_stages.grid(row=5, column=0, columnspan=5, padx=10)

        def run_gb():
            raw = e_stages.get().split(";")
            stages = []
            for item in raw:
                parts = item.strip().split(",")
                if len(parts) == 2:
                    stages.append({"rpm": float(parts[0]), "dir": parts[1].strip()})
            res = self.db_modules["gearbox"].design_custom_gearbox(float(e_in_rpm.get()), e_in_dir.get(), stages, float(e_mod.get()))
            self.show_result(res)
            self.preview_gearbox(res)

        ttk.Button(tab, text="صمم وارسم", command=run_gb).grid(row=5, column=5, columnspan=2)
    def build_3d_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="4. الماكينات 3D")

        ttk.Label(tab, text="بناء ترس ثلاثي الأبعاد للتشغيل على CNC (ملف STEP):", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)
        ttk.Label(tab, text="عدد الأسنان:").grid(row=1, column=0); e_gz = ttk.Entry(tab, width=12); e_gz.insert(0, "24"); e_gz.grid(row=1, column=1)
        ttk.Label(tab, text="الموديول:").grid(row=1, column=2); e_gm = ttk.Entry(tab, width=12); e_gm.insert(0, "3.0"); e_gm.grid(row=1, column=3)
        ttk.Label(tab, text="سمك الترس (مم):").grid(row=2, column=0); e_gt = ttk.Entry(tab, width=12); e_gt.insert(0, "25"); e_gt.grid(row=2, column=1)
        ttk.Label(tab, text="قطر الثقب (مم):").grid(row=2, column=2); e_gb = ttk.Entry(tab, width=12); e_gb.insert(0, "30"); e_gb.grid(row=2, column=3)

        ttk.Button(tab, text="توليد ترس 3D STEP", command=lambda: self.show_result(
            self.db_modules["cad3d"].build_3d_gear_assembly(int(e_gz.get()), float(e_gm.get()), float(e_gt.get()), float(e_gb.get()))
        )).grid(row=3, column=0, columnspan=4, pady=15)

    def build_units_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="5. الوحدات والفيزياء")

        ttk.Label(tab, text="القسم (length/area/volume/mass):").grid(row=0, column=0, padx=5, pady=8)
        e_cat = ttk.Entry(tab, width=12); e_cat.insert(0, "area"); e_cat.grid(row=0, column=1)

        ttk.Label(tab, text="القيمة:").grid(row=0, column=2); e_val = ttk.Entry(tab, width=12); e_val.insert(0, "1"); e_val.grid(row=0, column=3)
        ttk.Label(tab, text="من وحدة (feddan, qirat, sahm, weiba, kela):").grid(row=1, column=0, columnspan=2)
        e_u1 = ttk.Entry(tab, width=12); e_u1.insert(0, "feddan"); e_u1.grid(row=1, column=2)

        ttk.Label(tab, text="إلى وحدة (sqm, liter, m, cm, kg):").grid(row=2, column=0, columnspan=2)
        e_u2 = ttk.Entry(tab, width=12); e_u2.insert(0, "sqm"); e_u2.grid(row=2, column=2)

        ttk.Button(tab, text="تحويل الوحدة", command=lambda: self.show_result(
            self.db_modules["units"].convert(e_cat.get().strip(), float(e_val.get()), e_u1.get().strip(), e_u2.get().strip())
        )).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(tab, text="عرض ثوابت الفيزياء والإلكترون", command=lambda: self.show_result(
            self.db_modules["units"].get_physics_constants()
        )).grid(row=3, column=2, columnspan=2, pady=10)

    def build_elec_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="6. الإلكترونيات")

        ttk.Label(tab, text="قطر الكويل (مم):").grid(row=0, column=0); e_cd = ttk.Entry(tab, width=12); e_cd.insert(0, "10"); e_cd.grid(row=0, column=1)
        ttk.Label(tab, text="طول الكويل (مم):").grid(row=0, column=2); e_cl = ttk.Entry(tab, width=12); e_cl.insert(0, "20"); e_cl.grid(row=0, column=3)
        ttk.Label(tab, text="عدد اللفات:").grid(row=1, column=0); e_cn = ttk.Entry(tab, width=12); e_cn.insert(0, "15"); e_cn.grid(row=1, column=1)

        ttk.Button(tab, text="احسب محاثة الكويل", command=lambda: self.show_result(
            self.db_modules["elec"].calculate_coil_inductance(float(e_cd.get()), float(e_cl.get()), int(e_cn.get()))
        )).grid(row=1, column=2, columnspan=2, pady=10)

        ttk.Button(tab, text="رسم دائرة إرسال (TX)", command=lambda: self.show_result(
            self.db_modules["elec"].draw_rf_circuit("transmitter", "tx_circuit.png")
        )).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(tab, text="رسم دائرة استقبال (RX)", command=lambda: self.show_result(
            self.db_modules["elec"].draw_rf_circuit("receiver", "rx_circuit.png")
        )).grid(row=2, column=2, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineeringSuiteGUI(root)
    root.mainloop()
