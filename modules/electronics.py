import math
import os

try:
    import schemdraw
    import schemdraw.elements as elm
    HAS_SCHEMDRAW = True
except ImportError:
    HAS_SCHEMDRAW = False

class ElectronicsModule:
    def __init__(self, export_dir="exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)
        self.color_codes = {
            "black": 0, "brown": 1, "red": 2, "orange": 3, "yellow": 4,
            "green": 5, "blue": 6, "violet": 7, "grey": 8, "white": 9
        }
        self.tolerances = {
            "brown": "±1%", "red": "±2%", "gold": "±5%", "silver": "±10%"
        }

    def calculate_resistor(self, band1, band2, multiplier_color, tolerance_color="gold"):
        b1 = self.color_codes.get(band1.lower(), 0)
        b2 = self.color_codes.get(band2.lower(), 0)
        mult = 10 ** self.color_codes.get(multiplier_color.lower(), 0)
        tol = self.tolerances.get(tolerance_color.lower(), "±5%")
        ohms = (b1 * 10 + b2) * mult
        return {
            "القيمة_بالأوم": ohms,
            "القيمة_بالكيلو_أوم": ohms / 1000.0,
            "نسبة_الخطأ_الفئة": tol
        }

    def calculate_coil_inductance(self, diameter_mm, length_mm, turns):
        """حساب محاثة الملف الهوائي بالميكروهنري (Wheeler's Formula)"""
        d_inch = diameter_mm / 25.4
        l_inch = length_mm / 25.4
        inductance_uh = (d_inch**2 * turns**2) / (18 * d_inch + 40 * l_inch)
        return {
            "المحث_بالميكروهنري_uH": round(inductance_uh, 4),
            "المحث_بالملي_هنري_mH": round(inductance_uh / 1000.0, 6)
        }

    def calculate_resonance(self, inductance_uh, capacitance_pf):
        """حساب تردد الرنين لدائرة LC"""
        L = inductance_uh * 1e-6
        C = capacitance_pf * 1e-12
        freq_hz = 1.0 / (2 * math.pi * math.sqrt(L * C))
        return {
            "تردد_الرنين_هرتز": round(freq_hz, 2),
            "تردد_الرنين_ميجاهرتز_MHz": round(freq_hz / 1e6, 4)
        }

    def draw_rf_circuit(self, circuit_type="transmitter", filename="rf_circuit.png"):
        """رسم مخطط دائرة إرسال أو استقبال ترددات كصورة هندسية"""
        if not HAS_SCHEMDRAW:
            return {"تنبيه": "مكتبة schemdraw غير مثبتة. ثبتها عبر: pip install schemdraw"}

        filepath = os.path.join(self.export_dir, filename)
        with schemdraw.Drawing(file=filepath, show=False) as d:
            if circuit_type == "transmitter":
                d += elm.BatteryCell().up().label('9V')
                d += elm.Resistor().right().label('R1 10k')
                d += (q1 := elm.BjtNpn(circle=True).anchor('base').label('Q1 RF'))
                d += elm.Inductor2().up().at(q1.collector).label('L1 Tank')
                d += elm.Capacitor().right().label('C1 Var')
                d += elm.Antenna().up().label('TX Antenna')
                d += elm.Ground().at(q1.emitter)
            else:  # receiver
                d += elm.Antenna().down().label('RX Antenna')
                d += elm.Inductor2().down().label('L1 Tune')
                d += elm.Ground()
                d += elm.CapacitorVar().right().label('C1 Tune')
                d += elm.Diode().right().label('D1 Detector')
                d += elm.Capacitor().down().label('C2 Filter')
                d += elm.Ground()

        return {"نوع_الدائرة": circuit_type, "مسار_صورة_المخطط": filepath}
