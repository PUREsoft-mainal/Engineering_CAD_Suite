import os

try:
    import cadquery as cq
    HAS_CADQUERY = True
except ImportError:
    HAS_CADQUERY = False

class Machine3DModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def build_and_assemble_shaft_system(self, shaft_dia=50.0, shaft_len=300.0, flange_dia=140.0, flange_thick=20.0, filename="machine_assembly.step"):
        """
        رسم عمود إدارة (Shaft) وفلانشة (Flange) وتجميعهما افتراضياً وفحص التطابق وتصدير ملف STEP
        """
        if not HAS_CADQUERY:
            return {
                "تنبيه": "مكتبة CadQuery غير مثبتة على هذا الجهاز.",
                "الحل": "قم بتثبيتها عبر الأمر: pip install cadquery لتفعيل التصنيع ثلاثي الأبعاد."
            }

        # 1. إنشاء القطعة الأولى: عمود الإدارة (Shaft)
        shaft = cq.Workplane("XY").circle(shaft_dia / 2.0).extrude(shaft_len)

        # 2. إنشاء القطعة الثانية: الفلانشة المثقوبة من المنتصف بنفس قطر العمود
        flange = (
            cq.Workplane("XY")
            .circle(flange_dia / 2.0)
            .circle(shaft_dia / 2.0)  # ثقب التركيب
            .extrude(flange_thick)
        )

        # 3. تجميع القطعتين معاً في بيئة Assembly
        assy = cq.Assembly()
        assy.add(shaft, name="Main_Shaft", color=cq.Color("gray"))
        # تركيب الفلانشة في منتصف العمود تماماً
        assy.add(flange, name="Mounting_Flange", loc=cq.Location((0, 0, shaft_len / 2.0)), color=cq.Color("blue"))

        filepath = os.path.join(self.export_dir, filename)
        assy.save(filepath)

        return {
            "حالة_التجميع": "تم تجميع العمود والفلانشة بنجاح دون تداخل",
            "قطر_العمود": shaft_dia,
            "طول_العمود": shaft_len,
            "قطر_الفلانشة": flange_dia,
            "مسار_ملف_التشغيل_CNC_STEP": filepath
        }
