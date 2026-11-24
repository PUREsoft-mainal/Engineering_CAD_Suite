import math
import os
import ezdxf

class GearsAndGearboxModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def calculate_pulley_drive(self, d1, rpm1, d2, center_distance=500.0):
        """حساب سرعة الطنابير وطول السير الواصل بينهما"""
        rpm2 = (rpm1 * d1) / d2
        ratio = d2 / d1
        # حساب الطول التقريبي للسير المفتوح
        belt_length = (2 * center_distance) + (math.pi * (d1 + d2) / 2.0) + (((d2 - d1) ** 2) / (4 * center_distance))
        return {
            "سرعة_الطانبورة_المنقادة_RPM": round(rpm2, 2),
            "نسبة_النقل": f"1 : {round(ratio, 2)}",
            "طول_السير_المطلوب_مم": round(belt_length, 2)
        }

    def calculate_gear_pair(self, rpm1, z1=None, z2=None, d1=None, d2=None, module=2.0):
        """حساب نقل الحركة بين ترسين بالأسنان أو الأقطار"""
        if z1 and z2:
            rpm2 = rpm1 * (z1 / z2)
            pitch_d1 = z1 * module
            pitch_d2 = z2 * module
            ratio = z2 / z1
        elif d1 and d2:
            rpm2 = rpm1 * (d1 / d2)
            z1 = round(d1 / module)
            z2 = round(d2 / module)
            pitch_d1, pitch_d2 = d1, d2
            ratio = d2 / d1
        else:
            return {"خطأ": "أدخل إما عدد الأسنان للترسين أو الأقطار."}

        return {
            "سرعة_الترس_الثاني_RPM": round(rpm2, 2),
            "اتجاه_الترس_الثاني": "عكس اتجاه الترس الأول (تعشيق خارجي)",
            "نسبة_التخفيض": f"1 : {round(ratio, 2)}",
            "أسنان_الترس_1": z1,
            "أسنان_الترس_2": z2,
            "القطر_الخارجي_للترس_1_مم": round(pitch_d1 + (2 * module), 2),
            "القطر_الخارجي_للترس_2_مم": round(pitch_d2 + (2 * module), 2),
            "المسافة_بين_مركزي_العمودين_مم": round((pitch_d1 + pitch_d2) / 2.0, 2)
        }

    def design_custom_gearbox(self, input_rpm, input_dir, target_stages, module=3.0, min_teeth=14, filename="gearbox_layout.dxf"):
        """
        تصميم جيربوكس مكون من ترسين أو أكثر حسب السرعة والاتجاه المطلوب لكل مرحلة
        target_stages: قائمة من القواميس مثل: [{"rpm": 500, "dir": "CCW"}, {"rpm": 125, "dir": "CW"}]
        """
        gearbox_report = []
        current_rpm = input_rpm
        current_dir = input_dir.upper()  # CW (مع الساعة) أو CCW (عكس الساعة)
        
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        x_cursor = 0.0

        for idx, stage in enumerate(target_stages, start=1):
            req_rpm = stage["rpm"]
            req_dir = stage["dir"].upper()
            
            # تحديد نوع التعشيق بناءً على الاتجاه المطلوب
            if req_dir != current_dir:
                mesh_type = "تعشيق خارجي مباشر (External Spur Gears)"
                has_idler = False
            else:
                mesh_type = "تعشيق خارجي + ترس وسيط لعكس الاتجاه (Idler Gear)"
                has_idler = True

            ratio = current_rpm / req_rpm
            if ratio >= 1:
                z_driver = min_teeth
                z_driven = max(min_teeth, round(z_driver * ratio))
            else:
                z_driven = min_teeth
                z_driver = max(min_teeth, round(z_driven / ratio))

            actual_rpm = current_rpm * (z_driver / z_driven)
            d_driver = z_driver * module
            d_driven = z_driven * module
            od_driver = d_driver + (2 * module)
            od_driven = d_driven + (2 * module)

            # رسم تخطيطي للترس القائد والمنقاد في ملف DXF
            msp.add_circle((x_cursor, 0), radius=d_driver / 2.0)
            msp.add_circle((x_cursor, 0), radius=od_driver / 2.0)
            
            if has_idler:
                z_idler = min_teeth
                d_idler = z_idler * module
                x_idler = x_cursor + (d_driver + d_idler) / 2.0
                msp.add_circle((x_idler, 0), radius=d_idler / 2.0)
                x_driven = x_idler + (d_idler + d_driven) / 2.0
            else:
                x_driven = x_cursor + (d_driver + d_driven) / 2.0

            msp.add_circle((x_driven, 0), radius=d_driven / 2.0)
            msp.add_circle((x_driven, 0), radius=od_driven / 2.0)

            gearbox_report.append({
                "المرحلة": idx,
                "نوع_التعشيق": mesh_type,
                "السرعة_المطلوبة": req_rpm,
                "السرعة_الفعلية_الناتجة": round(actual_rpm, 2),
                "الاتجاه": req_dir,
                "أسنان_القائد": z_driver,
                "قطر_القائد_الخارجي_مم": round(od_driver, 2),
                "أسنان_المنقاد": z_driven,
                "قطر_المنقاد_الخارجي_مم": round(od_driven, 2),
                "ترس_وسيط_أسنان": min_teeth if has_idler else "لا يوجد"
            })

            current_rpm = actual_rpm
            current_dir = req_dir
            x_cursor = x_driven + (od_driven * 0.8)

        filepath = os.path.join(self.export_dir, filename)
        doc.saveas(filepath)

        return {
            "الموديول_المستخدم": module,
            "تفاصيل_المراحل": gearbox_report,
            "ملف_رسم_الجيربوكس_DXF": filepath
        }
