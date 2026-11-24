import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json

from modules.sheet_metal import SheetMetalModule
from modules.trusses import TrussModule
from modules.machine_3d import Machine3DModule
from modules.gears_gearbox import GearsAndGearboxModule
from modules.unit_converter import UnitAndPhysicsModule
from modules.electronics import ElectronicsModule

class EngineeringSuiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("المنظومة الهندسية الشاملة - تفريد الصاج، الجمالونات، الجيربوكس، الفيزياء والإلكترونيات")
        self.root.geometry("950x700")
        self.root.configure(bg="#0d1b2a")

        # قاعدة البيانات المركزية للمزايا
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
        style.configure("TNotebook.Tab", background="#1b263b", foreground="#00f5d4", padding=[12, 6], font=("Arial", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#415a77")], foreground=[("selected", "#ffd166")])
        style.configure("TFrame", background="#1b263b")
        style.configure("TLabel", background="#1b263b", foreground="#e0e1dd", font=("Arial", 10))
        style.configure("TButton", background="#00bbf9", foreground="#000000", font=("Arial", 10, "bold"), padding=6)
    def create_widgets(self):
        header = tk.Label(self.root, text="نظام الهندسة والفيزياء وتصميم الماكينات والجيربوكس", bg="#0d1b2a", fg="#ffd166", font=("Arial", 16, "bold"), pady=10)
        header.pack(fill="x")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.build_sheet_tab()
        self.build_truss_tab()
        self.build_gearbox_tab()
        self.build_3d_tab()
        self.build_units_tab()
        self.build_elec_tab()

        # صندوق عرض النتائج الموحد في الأسفل
        res_label = tk.Label(self.root, text="مخرجات الحسابات ومسارات ملفات التصميم (DXF / STEP):", bg="#0d1b2a", fg="#00f5d4", font=("Arial", 10, "bold"))
        res_label.pack(anchor="e", padx=12)

        self.output_box = scrolledtext.ScrolledText(self.root, height=11, bg="#09121c", fg="#00ff88", font=("Consolas", 11))
        self.output_box.pack(fill="x", padx=10, pady=(0, 10))

    def show_result(self, data):
        self.output_box.delete("1.0", tk.END)
        formatted = json.dumps(data, ensure_ascii=False, indent=4)
        self.output_box.insert(tk.END, formatted)

    # --- 1. تبويب تفريد الصاج والمسلوب والخزانات ---
    def build_sheet_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="1. الصاج والمسلوب والخزانات")

        # قسم المسلوب
        ttk.Label(tab, text="تفريد المسلوب (Frustum) وتصدير أوتوكاد DXF:", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="w")
        ttk.Label(tab, text="القطر الكبير (مم):").grid(row=1, column=0, padx=5, pady=5)
        e_d1 = ttk.Entry(tab); e_d1.insert(0, "1000"); e_d1.grid(row=1, column=1)

        ttk.Label(tab, text="القطر الصغير (مم):").grid(row=1, column=2, padx=5, pady=5)
        e_d2 = ttk.Entry(tab); e_d2.insert(0, "400"); e_d2.grid(row=1, column=3)

        ttk.Label(tab, text="الارتفاع (مم):").grid(row=2, column=0, padx=5, pady=5)
        e_h = ttk.Entry(tab); e_h.insert(0, "800"); e_h.grid(row=2, column=1)

        ttk.Button(tab, text="احسب التفريد وصدر DXF", command=lambda: self.show_result(
            self.db_modules["sheet"].calculate_and_export_cone(float(e_d1.get()), float(e_d2.get()), float(e_h.get()))
        )).grid(row=2, column=2, columnspan=2, pady=10)

        # قسم الخزان والدائرة
        ttk.Label(tab, text="حساب الخزان (التكعيب) والدائرة:", font=("Arial", 11, "bold")).grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="w")
        ttk.Label(tab, text="طول الخزان (م):").grid(row=4, column=0); e_tl = ttk.Entry(tab); e_tl.insert(0, "3"); e_tl.grid(row=4, column=1)
        ttk.Label(tab, text="العرض (م):").grid(row=4, column=2); e_tw = ttk.Entry(tab); e_tw.insert(0, "2"); e_tw.grid(row=4, column=3)
        ttk.Label(tab, text="الارتفاع (م):").grid(row=5, column=0); e_th = ttk.Entry(tab); e_th.insert(0, "1.5"); e_th.grid(row=5, column=1)
        ttk.Button(tab, text="احسب تكعيب الخزان", command=lambda: self.show_result(
            self.db_modules["sheet"].calculate_tank(float(e_tl.get()), float(e_tw.get()), float(e_th.get()))
        )).grid(row=5, column=2, columnspan=2, pady=5)

    # --- 2. تبويب الجمالونات ---
    def build_truss_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="2. الجمالونات (Trusses)")

        ttk.Label(tab, text="بحر الجمالون Span (م):").grid(row=0, column=0, padx=10, pady=10)
        e_span = ttk.Entry(tab); e_span.insert(0, "12"); e_span.grid(row=0, column=1)

        ttk.Label(tab, text="ارتفاع المنتصف (م):").grid(row=0, column=2, padx=10)
        e_ch = ttk.Entry(tab); e_ch.insert(0, "2.5"); e_ch.grid(row=0, column=3)

        ttk.Label(tab, text="ارتفاع الأطراف (م):").grid(row=1, column=0, padx=10, pady=10)
        e_sh = ttk.Entry(tab); e_sh.insert(0, "1.0"); e_sh.grid(row=1, column=1)

        ttk.Label(tab, text="عدد الباكيات:").grid(row=1, column=2, padx=10)
        e_pan = ttk.Entry(tab); e_pan.insert(0, "8"); e_pan.grid(row=1, column=3)

        ttk.Button(tab, text="تصميم الجمالون وتصدير DXF", command=lambda: self.show_result(
            self.db_modules["truss"].design_gable_truss(float(e_span.get()), float(e_ch.get()), float(e_sh.get()), int(e_pan.get()))
        )).grid(row=2, column=0, columnspan=4, pady=15)
    # --- 3. تبويب التروس والطنابير والجيربوكس ---
    def build_gearbox_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="3. التروس والطنابير والجيربوكس")

        # الطنابير
        ttk.Label(tab, text="أولاً: حساب الطنابير والسيور:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)
        ttk.Label(tab, text="قطر الطانبورة 1 (مم):").grid(row=1, column=0); e_p1 = ttk.Entry(tab, width=10); e_p1.insert(0, "100"); e_p1.grid(row=1, column=1)
        ttk.Label(tab, text="سرعة الموتور RPM:").grid(row=1, column=2); e_prpm = ttk.Entry(tab, width=10); e_prpm.insert(0, "1400"); e_prpm.grid(row=1, column=3)
        ttk.Label(tab, text="قطر الطانبورة 2 (مم):").grid(row=1, column=4); e_p2 = ttk.Entry(tab, width=10); e_p2.insert(0, "300"); e_p2.grid(row=1, column=5)
        ttk.Button(tab, text="احسب الطنابير", command=lambda: self.show_result(
            self.db_modules["gearbox"].calculate_pulley_drive(float(e_p1.get()), float(e_prpm.get()), float(e_p2.get()))
        )).grid(row=1, column=6, padx=5)

        # الجيربوكس متعدد المراحل
        ttk.Label(tab, text="ثانياً: تصميم جيربوكس متعدد التروس (أدخل السرعة والاتجاه لكل مرحلة):", font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=6, sticky="w", padx=10, pady=(15, 5))
        ttk.Label(tab, text="سرعة الدخول RPM:").grid(row=3, column=0); e_in_rpm = ttk.Entry(tab, width=10); e_in_rpm.insert(0, "1500"); e_in_rpm.grid(row=3, column=1)
        ttk.Label(tab, text="اتجاه الدخول (CW/CCW):").grid(row=3, column=2); e_in_dir = ttk.Entry(tab, width=10); e_in_dir.insert(0, "CW"); e_in_dir.grid(row=3, column=3)
        ttk.Label(tab, text="الموديول (Module):").grid(row=3, column=4); e_mod = ttk.Entry(tab, width=10); e_mod.insert(0, "3.0"); e_mod.grid(row=3, column=5)

        ttk.Label(tab, text="مراحل الجيربوكس (الصيغة: السرعة,الاتجاه مفصولة بفاصلة منقوطة ;):").grid(row=4, column=0, columnspan=6, sticky="w", padx=10, pady=5)
        e_stages = ttk.Entry(tab, width=60)
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

        ttk.Button(tab, text="صمم الجيربوكس وصدر DXF", command=run_gb).grid(row=5, column=5, columnspan=2)

    # --- 4. تبويب الماكينات 3D ---
    def build_3d_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="4. الماكينات والتروس 3D")

        ttk.Label(tab, text="بناء ترس ثلاثي الأبعاد للتشغيل على CNC (ملف STEP):", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)
        ttk.Label(tab, text="عدد الأسنان:").grid(row=1, column=0); e_gz = ttk.Entry(tab); e_gz.insert(0, "24"); e_gz.grid(row=1, column=1)
        ttk.Label(tab, text="الموديول:").grid(row=1, column=2); e_gm = ttk.Entry(tab); e_gm.insert(0, "3.0"); e_gm.grid(row=1, column=3)
        ttk.Label(tab, text="سمك الترس (مم):").grid(row=2, column=0); e_gt = ttk.Entry(tab); e_gt.insert(0, "25"); e_gt.grid(row=2, column=1)
        ttk.Label(tab, text="قطر ثقب العمود (مم):").grid(row=2, column=2); e_gb = ttk.Entry(tab); e_gb.insert(0, "30"); e_gb.grid(row=2, column=3)

        ttk.Button(tab, text="توليد ترس 3D STEP", command=lambda: self.show_result(
            self.db_modules["cad3d"].build_3d_gear_assembly(int(e_gz.get()), float(e_gm.get()), float(e_gt.get()), float(e_gb.get()))
        )).grid(row=3, column=0, columnspan=4, pady=15)
    # --- 5. تبويب الوحدات والفيزياء ---
    def build_units_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="5. الوحدات والفيزياء")

        ttk.Label(tab, text="القسم (length / area / volume / mass):").grid(row=0, column=0, padx=5, pady=10)
        e_cat = ttk.Entry(tab); e_cat.insert(0, "area"); e_cat.grid(row=0, column=1)

        ttk.Label(tab, text="القيمة:").grid(row=0, column=2); e_val = ttk.Entry(tab); e_val.insert(0, "1"); e_val.grid(row=0, column=3)
        ttk.Label(tab, text="من وحدة (feddan, qirat, sahm, weiba, kela, inch, qasaba):").grid(row=1, column=0, columnspan=2)
        e_u1 = ttk.Entry(tab); e_u1.insert(0, "feddan"); e_u1.grid(row=1, column=2)

        ttk.Label(tab, text="إلى وحدة (sqm, liter, m, cm, kg):").grid(row=2, column=0, columnspan=2)
        e_u2 = ttk.Entry(tab); e_u2.insert(0, "sqm"); e_u2.grid(row=2, column=2)

        ttk.Button(tab, text="تحويل الوحدة", command=lambda: self.show_result(
            self.db_modules["units"].convert(e_cat.get().strip(), float(e_val.get()), e_u1.get().strip(), e_u2.get().strip())
        )).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(tab, text="عرض ثوابت الفيزياء والإلكترون والضوء", command=lambda: self.show_result(
            self.db_modules["units"].get_physics_constants()
        )).grid(row=3, column=2, columnspan=2, pady=10)

    # --- 6. تبويب الإلكترونيات والترددات ---
    def build_elec_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="6. الإلكترونيات والترددات")

        ttk.Label(tab, text="قطر الكويل (مم):").grid(row=0, column=0); e_cd = ttk.Entry(tab); e_cd.insert(0, "10"); e_cd.grid(row=0, column=1)
        ttk.Label(tab, text="طول الكويل (مم):").grid(row=0, column=2); e_cl = ttk.Entry(tab); e_cl.insert(0, "20"); e_cl.grid(row=0, column=3)
        ttk.Label(tab, text="عدد اللفات:").grid(row=1, column=0); e_cn = ttk.Entry(tab); e_cn.insert(0, "15"); e_cn.grid(row=1, column=1)

        ttk.Button(tab, text="احسب محاثة الكويل", command=lambda: self.show_result(
            self.db_modules["elec"].calculate_coil_inductance(float(e_cd.get()), float(e_cl.get()), int(e_cn.get()))
        )).grid(row=1, column=2, columnspan=2, pady=10)

        ttk.Button(tab, text="رسم دائرة إرسال (Transmitter)", command=lambda: self.show_result(
            self.db_modules["elec"].draw_rf_circuit("transmitter", "tx_circuit.png")
        )).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(tab, text="رسم دائرة استقبال (Receiver)", command=lambda: self.show_result(
            self.db_modules["elec"].draw_rf_circuit("receiver", "rx_circuit.png")
        )).grid(row=2, column=2, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineeringSuiteGUI(root)
    root.mainloop()
