import math
import os
import ezdxf

class SheetMetalModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def calculate_circle(self, diameter):
        radius = diameter / 2.0
        circumference = math.pi * diameter
        area = math.pi * (radius ** 2)
        return {
            "المحيط": round(circumference, 3),
            "المساحة": round(area, 3)
        }

    def calculate_tank(self, length, width, height):
        volume_m3 = length * width * height
        capacity_liters = volume_m3 * 1000.0
        return {
            "التكعيب_متر_مكعب": round(volume_m3, 3),
            "السعة_باللتر": round(capacity_liters, 2)
        }

    def calculate_and_export_cone(self, d_large, d_small, height, filename="cone_pattern.dxf"):
        if d_large == d_small:
            return {"خطأ": "القطران متساويان؛ هذا الشكل أسطوانة وليس مسلوباً."}

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
            "المساحة_التربيعية": round(surface_area, 2),
            "نصف_القطر_الكبير_R1": round(R1, 2),
            "نصف_القطر_الصغير_R2": round(R2, 2),
            "زاوية_التقطيع": round(angle_deg, 2),
            "مسار_ملف_التقطيع": filepath
        }
