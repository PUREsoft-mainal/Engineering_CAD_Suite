import math

class UnitAndPhysicsModule:
    def __init__(self):
        # معاملات التحويل إلى الوحدة القياسية (متر، متر مربع، لتر، كيلوجرام)
        self.length_to_meter = {
            "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
            "inch": 0.0254, "foot": 0.3048, "mile": 1609.344,
            "qasaba": 3.55,  # القصبة المصرية
            "light_year": 9.46073047e15  # السنة الضوئية
        }
        self.area_to_sqm = {
            "sqm": 1.0,
            "sahm": 7.293,       # السهم
            "qirat": 175.035,    # القيراط (24 سهم)
            "feddan": 4200.83    # الفدان (24 قيراط)
        }
        self.volume_to_liter = {
            "liter": 1.0, "m3": 1000.0,
            "kela": 16.5,        # الكيلة المصرية
            "weiba": 33.0,       # الويبة (2 كيلة)
            "ardeb": 198.0       # الأردب (6 ويبات)
        }
        self.mass_to_kg = {
            "gram": 0.001, "kg": 1.0, "ton": 1000.0
        }

        # الثوابت الفيزيائية والذرية
        self.constants = {
            "سرعة_الضوء_متر_ثانية": 299792458,
            "سرعة_الصوت_في_الهواء_20C": 343.0,
            "السنة_الضوئية_بالمتر": 9.46073047e15,
            "نصف_قطر_الإلكترون_الكلاسيكي_متر": 2.8179403262e-15,
            "كتلة_الإلكترون_كجم": 9.1093837015e-31,
            "شحنة_الإلكترون_كولوم": 1.602176634e-19
        }

    def convert(self, category, value, from_unit, to_unit):
        tables = {
            "length": self.length_to_meter,
            "area": self.area_to_sqm,
            "volume": self.volume_to_liter,
            "mass": self.mass_to_kg
        }
        table = tables.get(category)
        if not table or from_unit not in table or to_unit not in table:
            return {"خطأ": "وحدة غير مدعومة أو قسم غير صحيح"}

        base_value = value * table[from_unit]
        result = base_value / table[to_unit]
        return {
            "القيمة_المدخلة": f"{value} {from_unit}",
            "النتيجة": f"{round(result, 6)} {to_unit}"
        }

    def sound_speed_by_temp(self, temp_celsius):
        speed = 331.3 + (0.606 * temp_celsius)
        return {"درجة_الحرارة": temp_celsius, "سرعة_الصوت_متر_ثانية": round(speed, 2)}

    def get_physics_constants(self):
        return self.constants
