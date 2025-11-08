from src.services.query_data_manager.manager_query_data import QueryData

class addInvoiceController:
    def __init__(self, mainview):
            self.query_data = QueryData()
            self.view = mainview

    def render_product_infor(self):
        data = self.view.get_selected_product_import_data()
        if data:
            print(f"DEBUG: DATA RENDER: {data}")
        else:
            print(f"DEBUG: DATA RENDER IS NONE")
        self.view.view.product_id_import.setText(data["product_id"])
        self.view.view.type_import.setText(data["product_type"])
        self.view.view.name_import.setText(data["product_name"])
        self.view.view.quantity_import.clear()
        self.view.view.import_price.clear()
        self.view.set_disable_btn()



