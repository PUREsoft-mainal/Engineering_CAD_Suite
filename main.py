from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import json

from modules.sheet_metal import SheetMetalModule
from modules.trusses import TrussModule
from modules.gears_gearbox import GearsAndGearboxModule
from modules.unit_converter import UnitAndPhysicsModule
from modules.electronics import ElectronicsModule

class EngineeringMobileApp(App):
    def build(self):
        self.db = {
            "sheet": SheetMetalModule(),
            "truss": TrussModule(),
            "gearbox": GearsAndGearboxModule(),
            "units": UnitAndPhysicsModule(),
            "elec": ElectronicsModule()
        }

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)
        tabs = TabbedPanel(do_default_tab=False)

        # 1. تبويب المسلوب
        t_cone = TabbedPanelItem(text="المسلوب")
        b_cone = BoxLayout(orientation="vertical", spacing=6)
        in_d1 = TextInput(hint_text="القطر الكبير (مم)", text="1000", multiline=False)
        in_d2 = TextInput(hint_text="القطر الصغير (مم)", text="400", multiline=False)
        in_h = TextInput(hint_text="الارتفاع (مم)", text="800", multiline=False)
        btn_cone = Button(text="احسب تفريد المسلوب DXF", size_hint_y=None, height=50)
        btn_cone.bind(on_press=lambda x: self.display_res(
            self.db["sheet"].calculate_and_export_cone(float(in_d1.text), float(in_d2.text), float(in_h.text))
        ))
        for w in [in_d1, in_d2, in_h, btn_cone]: b_cone.add_widget(w)
        t_cone.add_widget(b_cone)
        tabs.add_widget(t_cone)

        # 2. تبويب الجمالونات
        t_truss = TabbedPanelItem(text="الجمالونات")
        b_truss = BoxLayout(orientation="vertical", spacing=6)
        in_sp = TextInput(hint_text="بحر الجمالون (م)", text="12", multiline=False)
        in_ch = TextInput(hint_text="ارتفاع المنتصف (م)", text="2.5", multiline=False)
        in_sh = TextInput(hint_text="ارتفاع الأطراف (م)", text="1.0", multiline=False)
        in_pn = TextInput(hint_text="عدد الباكيات", text="8", multiline=False)
        btn_truss = Button(text="تصميم الجمالون DXF", size_hint_y=None, height=50)
        btn_truss.bind(on_press=lambda x: self.display_res(
            self.db["truss"].design_gable_truss(float(in_sp.text), float(in_ch.text), float(in_sh.text), int(in_pn.text))
        ))
        for w in [in_sp, in_ch, in_sh, in_pn, btn_truss]: b_truss.add_widget(w)
        t_truss.add_widget(b_truss)
        tabs.add_widget(t_truss)

        # 3. تبويب الجيربوكس
        t_gb = TabbedPanelItem(text="الجيربوكس")
        b_gb = BoxLayout(orientation="vertical", spacing=6)
        in_rpm = TextInput(hint_text="سرعة الدخول RPM", text="1500", multiline=False)
        in_dir = TextInput(hint_text="الاتجاه (CW/CCW)", text="CW", multiline=False)
        in_stg = TextInput(hint_text="المراحل: 500,CCW ; 125,CW", text="500,CCW ; 125,CW", multiline=False)
        btn_gb = Button(text="تصميم الجيربوكس DXF", size_hint_y=None, height=50)
        def run_gb(inst):
            stages = [{"rpm": float(p.split(",")), "dir": p.split(",").strip()} for p in in_stg.text.split(";") if "," in p]
            self.display_res(self.db["gearbox"].design_custom_gearbox(float(in_rpm.text), in_dir.text, stages))
        btn_gb.bind(on_press=run_gb)
        for w in [in_rpm, in_dir, in_stg, btn_gb]: b_gb.add_widget(w)
        t_gb.add_widget(b_gb)
        tabs.add_widget(t_gb)

        root.add_widget(tabs)

        # شاشة عرض النتائج
        scroll = ScrollView(size_hint=(1, 0.45))
        self.res_label = Label(text="النتائج ستظهر هنا...", size_hint_y=None, halign="left", valign="top")
        self.res_label.bind(texture_size=self.res_label.setter('size'))
        scroll.add_widget(self.res_label)
        root.add_widget(scroll)

        return root

    def display_res(self, data):
        self.res_label.text = json.dumps(data, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    EngineeringMobileApp().run()
