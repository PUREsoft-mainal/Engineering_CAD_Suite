import os
import math

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
        if not HAS_CADQUERY:
            return {"تنبيه": "مكتبة CadQuery غير مثبتة. ثبتها عبر: pip install cadquery"}

        shaft = cq.Workplane("XY").circle(shaft_dia / 2.0).extrude(shaft_len)
        flange = cq.Workplane("XY").circle(flange_dia / 2.0).circle(shaft_dia / 2.0).extrude(flange_thick)

        assy = cq.Assembly()
        assy.add(shaft, name="Main_Shaft", color=cq.Color("gray"))
        assy.add(flange, name="Mounting_Flange", loc=cq.Location((0, 0, shaft_len / 2.0)), color=cq.Color("blue"))

        filepath = os.path.join(self.export_dir, filename)
        assy.save(filepath)
        return {"حالة_التجميع": "تم تجميع العمود والفلانشة بنجاح", "مسار_ملف_STEP": filepath}

    def build_3d_gear_assembly(self, teeth=24, module=3.0, thickness=25.0, bore_dia=30.0, filename="gear_3d.step"):
        """بناء مجسم ترس ثلاثي الأبعاد مع ثقب العمود والخابور للتشغيل على CNC"""
        if not HAS_CADQUERY:
            return {"تنبيه": "مكتبة CadQuery غير مثبتة. ثبتها عبر: pip install cadquery"}

        pitch_dia = teeth * module
        outer_dia = pitch_dia + (2 * module)
        root_dia = pitch_dia - (2.5 * module)

        # بناء جسم الترس الأساسي والثقب الداخلي
        gear_body = (
            cq.Workplane("XY")
            .circle(root_dia / 2.0)
            .circle(bore_dia / 2.0)
            .extrude(thickness)
        )

        # إضافة الأسنان حول المحيط
        tooth_width = (math.pi * pitch_dia) / (2.2 * teeth)
        tooth_height = (outer_dia - root_dia) / 2.0
        
        for i in range(teeth):
            angle = i * (360.0 / teeth)
            tooth = (
                cq.Workplane("XY")
                .transformed(rotate=(0, 0, angle))
                .center(root_dia / 2.0 + tooth_height / 2.0 - 0.5, 0)
                .rect(tooth_height + 1.0, tooth_width)
                .extrude(thickness)
            )
            gear_body = gear_body.union(tooth)

        filepath = os.path.join(self.export_dir, filename)
        cq.exporters.export(gear_body, filepath)
        return {
            "حالة_التصميم_3D": "تم بناء الترس ثلاثي الأبعاد بنجاح",
            "عدد_الأسنان": teeth,
            "القطر_الخارجي_مم": round(outer_dia, 2),
            "مسار_ملف_CNC_STEP": filepath
        }
