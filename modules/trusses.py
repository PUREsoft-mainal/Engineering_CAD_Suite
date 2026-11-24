import math
import os
import ezdxf

class TrussModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def design_gable_truss(self, span, center_height, side_height, panels=6, filename="gable_truss.dxf"):
        """
        تصميم جمالون هرمي (Gable Truss) وحساب أطوال القوائم والمائلات وتصديره DXF
        """
        if panels % 2 != 0:
            panels += 1  # لضمان التماثل في المنتصف

        half_span = span / 2.0
        panel_width = span / panels
        slope_rise = center_height - side_height
        rafter_length = math.sqrt(half_span**2 + slope_rise**2)
        rafter_angle_deg = math.degrees(math.atan2(slope_rise, half_span))

        filepath = os.path.join(self.export_dir, filename)
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()

        # رسم الوتر السفلي (Bottom Chord)
        msp.add_line((0, 0), (span, 0))

        # رسم الوتر العلوي الأيسر والأيمن (Top Chords)
        msp.add_line((0, side_height), (half_span, center_height))
        msp.add_line((half_span, center_height), (span, side_height))

        verticals_lengths = []
        diagonals_lengths = []

        for i in range(panels + 1):
            x = i * panel_width
            # حساب ارتفاع الوتر العلوي عند النقطة x
            if x <= half_span:
                y_top = side_height + (slope_rise * (x / half_span))
            else:
                y_top = side_height + (slope_rise * ((span - x) / half_span))

            # رسم القائم الرأسي (Vertical)
            if y_top > 0:
                msp.add_line((x, 0), (x, y_top))
                verticals_lengths.append(round(y_top, 3))

            # رسم الضلع المائل الداخلي (Diagonal)
            if i < panels:
                x_next = (i + 1) * panel_width
                if x_next <= half_span:
                    y_next_top = side_height + (slope_rise * (x_next / half_span))
                    msp.add_line((x, 0), (x_next, y_next_top))
                    diag_len = math.sqrt(panel_width**2 + y_next_top**2)
                else:
                    y_next_top = side_height + (slope_rise * ((span - x_next) / half_span))
                    msp.add_line((x, y_top), (x_next, 0))
                    diag_len = math.sqrt(panel_width**2 + y_top**2)
                diagonals_lengths.append(round(diag_len, 3))

        doc.saveas(filepath)

        total_steel_length = span + (2 * rafter_length) + sum(verticals_lengths) + sum(diagonals_lengths)

        return {
            "بحر_الجمالون": span,
            "طول_الوتر_المائل_الواحد": round(rafter_length, 3),
            "زاوية_ميل_السطح": round(rafter_angle_deg, 2),
            "أطوال_القوائم_الرأسية": verticals_lengths,
            "أطوال_الشكالات_المائلة": diagonals_lengths,
            "إجمالي_أمتار_الحديد_المطلوبة": round(total_steel_length, 2),
            "مسار_ملف_الأوتوكاد": filepath
        }
