import sys
from modules.sheet_metal import SheetMetalModule

class EngineeringDatabaseCore:
    def __init__(self):
        # قاعدة بيانات تسجيل المزايا والخصائص المستقلة
        self.modules_registry = {
            "1": {
                "name": "تفريد الصاج والمسلوب والخزانات والدوائر",
                "instance": SheetMetalModule(),
                "status": "مفعل"
            },
            "2": {
                "name": "حساب ورسم الجمالونات (Trusses)",
                "instance": None,
                "status": "قيد الإضافة"
            },
            "3": {
                "name": "تصميم وتجميع الماكينات 3D",
                "instance": None,
                "status": "قيد الإضافة"
            },
            "4": {
                "name": "محول الوحدات الشامل والفيزياء",
                "instance": None,
                "status": "قيد الإضافة"
            },
            "5": {
                "name": "الدوائر الإلكترونية والترددات (RF)",
                "instance": None,
                "status": "قيد الإضافة"
            }
        }

    def get_module(self, module_key):
        module_data = self.modules_registry.get(module_key)
        if module_data and module_data["instance"]:
            return module_data["instance"]
        return None

# --- مثال لتشغيل واستدعاء الميزة من قاعدة البيانات ---
if __name__ == "__main__":
    app_db = EngineeringDatabaseCore()
    
    # استدعاء وحدة الصاج (رقم 1)
    sheet_tool = app_db.get_module("1")
    
    if sheet_tool:
        print("=== نتيجة تفريد المسلوب ===")
        cone_res = sheet_tool.calculate_and_export_cone(d_large=1000, d_small=400, height=800)
        print(cone_res)
        
        print("\n=== نتيجة حساب الخزان ===")
        tank_res = sheet_tool.calculate_tank(length=3.0, width=2.0, height=1.5)
        print(tank_res)
