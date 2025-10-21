# file: src/services/order_service.py

class OrderService:
    def __init__(self):
        # Dictionary chứa các item trong giỏ hàng (key: product_id, value: item_data)
        self.items = {}
        self.customer_info = None

    def add_item(self, product_data):
        product_id = product_data.get('product_id')
        if product_id in self.items:
            self.items[product_id]['quantity'] += 1
        else:
            self.items[product_id] = {
                'data': product_data,
                'quantity': 1
            }

    def remove_item(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def update_quantity(self, product_id, new_quantity):
        if product_id in self.items:
            self.items[product_id]['quantity'] = new_quantity

    def get_total_amount(self):
        total = 0
        for item in self.items.values():
            price = item['data'].get('selling_price', 0)
            quantity = item['quantity']
            total += price * quantity
        return total

    def increase_item_quantity(self, product_id):
        if product_id in self.items:
            self.items[product_id]['quantity'] += 1

    def clear_order(self):
        self.items.clear()
        self.customer_info = None