import sys
from modules.sheet_metal import SheetMetalModule
from modules.trusses import TrussModule
from modules.machine_3d import Machine3DModule
from modules.unit_converter import UnitAndPhysicsModule
from modules.electronics import ElectronicsModule

class EngineeringDatabaseCore:
    def __init__(self):
        # قاعدة البيانات المركزية لاستدعاء جميع المزايا والخصائص المستقلة
        self.database = {
            "1": {
                "title": "تفريد الصاج، المسلوب، الدوائر، والخزانات",
                "module": SheetMetalModule()
            },
            "2": {
                "title": "تصميم وحساب الجمالونات (Trusses) وتصدير DXF",
                "module": TrussModule()
            },
            "3": {
                "title": "رسم وتجميع أجزاء الماكينات ثلاثية الأبعاد (3D Assembly)",
                "module": Machine3DModule()
            },
            "4": {
                "title": "محول الوحدات (الفدان، الويبة، الكيلة) والفيزياء الذرية",
                "module": UnitAndPhysicsModule()
            },
            "5": {
                "title": "الإلكترونيات، الكويل، الرنين، ورسم دوائر الإرسال والاستقبال",
                "module": ElectronicsModule()
            }
        }

    def run_cli(self):
        while True:
            print("\n" + "="*55)
            print("   نظام الهندسة والفيزياء وتفريد الصاج والماكينات (DB Core)")
            print("="*55)
            for key, item in self.database.items():
                print(f" [{key}] {item['title']}")
            print(" [0] خروج")

            choice = input("\nاختر رقم الوحدة من قاعدة البيانات: ").strip()

            if choice == "0":
                print("تم إغلاق البرنامج.")
                break

            elif choice == "1":
                mod = self.database["1"]["module"]
                print("\n--- وحدة الصاج والخزانات ---")
                print("1: دائرة | 2: خزان | 3: مسلوب (تفريد + DXF)")
                sub = input("اختر: ")
                if sub == "1":
                    d = float(input("أدخل قطر الدائرة: "))
                    print(mod.calculate_circle(d))
                elif sub == "2":
                    l = float(input("الطول (م): "))
                    w = float(input("العرض (م): "))
                    h = float(input("الارتفاع (م): "))
                    print(mod.calculate_tank(l, w, h))
                elif sub == "3":
                    d1 = float(input("القطر الكبير: "))
                    d2 = float(input("القطر الصغير: "))
                    h = float(input("الارتفاع: "))
                    print(mod.calculate_and_export_cone(d1, d2, h))

            elif choice == "2":
                mod = self.database["2"]["module"]
                print("\n--- وحدة الجمالونات ---")
                span = float(input("بحر الجمالون (Span) بالمتر: "))
                ch = float(input("ارتفاع المنتصف بالمتر: "))
                sh = float(input("ارتفاع الأطراف بالمتر: "))
                panels = int(input("عدد الباكيات (مثال 6 أو 8): "))
                print(mod.design_gable_truss(span, ch, sh, panels))

            elif choice == "3":
                mod = self.database["3"]["module"]
                print("\n--- وحدة تجميع الماكينات 3D ---")
                sd = float(input("قطر العمود (مم): "))
                sl = float(input("طول العمود (مم): "))
                fd = float(input("قطر الفلانشة (مم): "))
                print(mod.build_and_assemble_shaft_system(sd, sl, fd))

            elif choice == "4":
                mod = self.database["4"]["module"]
                print("\n--- وحدة الوحدات والفيزياء ---")
                print("1: تحويل وحدات | 2: ثوابت الفيزياء والإلكترون | 3: سرعة الصوت بالحرارة")
                sub = input("اختر: ")
                if sub == "1":
                    cat = input("القسم (length / area / volume / mass): ").strip()
                    val = float(input("القيمة: "))
                    u1 = input("من وحدة (مثال: feddan, qirat, sahm, weiba, kela, inch, qasaba): ").strip()
                    u2 = input("إلى وحدة (مثال: sqm, liter, m, cm, kg): ").strip()
                    print(mod.convert(cat, val, u1, u2))
                elif sub == "2":
                    for k, v in mod.get_physics_constants().items():
                        print(f" - {k}: {v}")
                elif sub == "3":
                    t = float(input("درجة الحرارة المئوية: "))
                    print(mod.sound_speed_by_temp(t))

            elif choice == "5":
                mod = self.database["5"]["module"]
                print("\n--- وحدة الإلكترونيات والترددات ---")
                print("1: مقاومة بالألوان | 2: حساب الكويل | 3: تردد الرنين | 4: رسم دائرة إرسال/استقبال")
                sub = input("اختر: ")
                if sub == "1":
                    c1 = input("اللون الأول (مثال brown): ")
                    c2 = input("اللون الثاني (مثال black): ")
                    c3 = input("لون الضرب (مثال red): ")
                    print(mod.calculate_resistor(c1, c2, c3))
                elif sub == "2":
                    d = float(input("قطر الملف (مم): "))
                    l = float(input("طول الملف (مم): "))
                    n = int(input("عدد اللفات: "))
                    print(mod.calculate_coil_inductance(d, l, n))
                elif sub == "3":
                    l_uh = float(input("قيمة الملف بالميكروهنري (uH): "))
                    c_pf = float(input("سعة المكثف بالبيكوفاراد (pF): "))
                    print(mod.calculate_resonance(l_uh, c_pf))
                elif sub == "4":
                    ctype = input("اكتب transmitter للإرسال أو receiver للاستقبال: ").strip()
                    print(mod.draw_rf_circuit(ctype))
            else:
                print("اختيار غير صحيح.")

if __name__ == "__main__":
    app = EngineeringDatabaseCore()
    app.run_cli()
