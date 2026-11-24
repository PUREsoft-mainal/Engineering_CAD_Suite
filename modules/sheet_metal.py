import math
import os
import ezdxf

class SheetMetalModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def calculate_circle(self, diameter):
        radius = diameter / 2.0
        return {
            "القطر": diameter,
            "المحيط": round(math.pi * diameter, 3),
            "المساحة": round(math.pi * (radius ** 2), 3)
        }

    def calculate_tank(self, length, width, height):
        volume_m3 = length * width * height
        return {
            "التكعيب_متر_مكعب": round(volume_m3, 3),
            "السعة_باللتر": round(volume_m3 * 1000.0, 2)
        }

    def calculate_and_export_cone(self, d_large, d_small, height, filename="cone_pattern.dxf"):
        if d_large == d_small:
            return {"خطأ": "القطران متساويان؛ هذا الشكل أسطوانة (مستطيل مفرود) وليس مسلوباً."}

        radius_diff = abs(d_large - d_small) / 2.0
        slant_height = math.sqrt(height**2 + radius_diff**2)
        surface_area = math.pi * ((d_large + d_small) / 2.0) * slant_height

        max_d = max(d_large, d_small)
        min_d = min(d_large, d_small)

        R1 = (max_d * slant_height) / (max_d - min_d)
        R2 = R1 - slant_height
        angle_deg = (180.0 * max_d) / R1

        filepath = os.path.join(self.export_dir, filename)
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()

        msp.add_arc(center=(0, 0), radius=R1, start_angle=0, end_angle=angle_deg)
        msp.add_arc(center=(0, 0), radius=R2, start_angle=0, end_angle=angle_deg)

        angle_rad = math.radians(angle_deg)
        msp.add_line(start=(R2, 0), end=(R1, 0))
        msp.add_line(
            start=(R2 * math.cos(angle_rad), R2 * math.sin(angle_rad)),
            end=(R1 * math.cos(angle_rad), R1 * math.sin(angle_rad))
        )

        doc.saveas(filepath)

        return {
            "المساحة_التربيعية_للصاج": round(surface_area, 2),
            "طول_الراسم_المائل": round(slant_height, 2),
            "نصف_قطر_البرجل_الكبير_R1": round(R1, 2),
            "نصف_قطر_البرجل_الصغير_R2": round(R2, 2),
            "زاوية_التقطيع_بالدرجات": round(angle_deg, 2),
            "مسار_ملف_الأوتوكاد": filepath
        }
