"""Food delivery order queue manager.

Creates orders from a menu, moves them through delivery statuses, totals the
day's revenue and backs the queue up to disk as JSON.
"""
import json
from datetime import datetime

VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}


class OrderQueue:
    """Holds the menu and all orders for one kitchen."""

    def __init__(self):
        self.orders = {}
        self.menu = {}
        self.next_id = 1

    def read_menu_config(self, file="menu.json"):
        """Load the menu from a JSON file, falling back to the default."""
        try:
            with open(file, encoding="utf-8") as menu_file:
                self.menu = json.load(menu_file)
        except (OSError, json.JSONDecodeError):
            self.menu = dict(DEFAULT_MENU)

    def create_order(self, customer, items):
        """Create an order and return its id.

        Raises ValueError for a missing customer, an empty order or a dish
        that is not on the menu (instead of silently charging a fake price).
        """
        if not customer or not customer.strip():
            raise ValueError("customer name is required")
        if not items:
            raise ValueError("order must contain at least one item")
        unknown = [item for item in items if item not in self.menu]
        if unknown:
            raise ValueError(f"not on the menu: {', '.join(unknown)}")
        total = sum(self.menu[item] for item in items)
        order_id = self.next_id
        self.orders[order_id] = {
            "customer": customer,
            "items": items,
            "total": total,
            "status": "placed",
        }
        self.next_id += 1
        return order_id

    def update_order_status(self, order_id, status):
        """Set an order's status; return False if the id or status is bad."""
        if order_id not in self.orders:
            print("Unknown order id:", order_id)
            return False
        if status not in VALID_STATUSES:
            print("Invalid status:", status)
            return False
        self.orders[order_id]["status"] = status
        return True

    def daily_revenue(self):
        """Return the total of all delivered orders."""
        return sum(
            order["total"]
            for order in self.orders.values()
            if order["status"] == "delivered"
        )

    def backup_orders(self, file="orders.json"):
        """Write all orders to a JSON file."""
        with open(file, "w", encoding="utf-8") as backup_file:
            json.dump(self.orders, backup_file)

    def restore_orders(self, file="orders.json"):
        """Reload orders from a JSON file and continue id numbering."""
        with open(file, encoding="utf-8") as backup_file:
            data = json.load(backup_file)
        self.orders = {int(key): value for key, value in data.items()}
        self.next_id = max(self.orders, default=0) + 1

    def print_queue(self):
        """Print every order with its customer, status and total."""
        print(f"Order queue at {datetime.now()}")
        for order_id, order in self.orders.items():
            print(order_id, order["customer"], order["status"], order["total"])


def _try_create(queue, customer, items):
    """Create an order for the demo, reporting rejected ones."""
    try:
        return queue.create_order(customer, items)
    except ValueError as error:
        print(f"Order rejected for {customer!r}: {error}")
        return None


def main():
    """Run the demo scenario."""
    queue = OrderQueue()
    queue.read_menu_config()
    first = _try_create(queue, "Asha", ["pizza", "coke"])
    second = _try_create(queue, "Ravi", ["burger", "sushi"])
    third = _try_create(queue, "", [])
    queue.update_order_status(first, "delivered")
    queue.update_order_status(second, "teleported")
    queue.update_order_status(42, "delivered")
    queue.update_order_status(third, "delivered")
    print("Revenue today:", queue.daily_revenue())
    queue.backup_orders()
    queue.restore_orders()
    queue.print_queue()


if __name__ == "__main__":
    main()
