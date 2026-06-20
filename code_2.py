from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name : str, price : float, quantity: int):
        self.__name = name
        if price < 0 or quantity < 0:
            raise ValueError("Values cannot be Negative")
        else:
            self.__price = price
            self.__quantity = quantity
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, amount):
        if amount < 0:
            raise ValueError("Price cannot be negative")
        else:
            self.__price = amount
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, given_name : str):
        if isinstance(given_name, str):
            self.__name = given_name
        else:
            raise TypeError("Name must of string type")
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self, amount : int):
        if amount < 0:
            raise ValueError("Quantity cannot be negative")
        else:
            self.__quantity = amount
    @abstractmethod
    def get_detail(self) -> str:
        pass
class PhysicalProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, weight: float, shipping_cost: float):
        super().__init__(name, price, quantity)
        if weight < 0 or shipping_cost < 0:
            raise ValueError("Values cannot be Negative")
        self.__weight = weight
        self.__shipping_cost = shipping_cost
    @property
    def weight(self):
        return self.__weight
    @property
    def shipping_cost(self):
        return self.__shipping_cost

    def get_detail(self):
        return f"Product name: {self.name}\nPrice: {self.price}\nQuantity: {self.quantity}\nWeight_in_kg: {self.weight}"

    def __str__(self):
        return f"Product name: {self.name}\nPrice: {self.price}\nQuantity: {self.quantity}\nWeight_in_kg: {self.weight}"


    def total_cost_with_shipping(self, length_cm, width_cm, height_cm, distance_km, express=False):
        chargeable_weight = max(self.weight, (length_cm * width_cm * height_cm) / 5000)
        distance_cost = distance_km * 0.05
        weight_cost = chargeable_weight * 0.8
        express_multiplier = 1.5 if express else 1.0
        shipping_total = (self.shipping_cost + distance_cost + weight_cost) * express_multiplier * 1.12
        return round(self.price + shipping_total, 2)


class DigitalProduct(Product):

    def __init__(self, name:str, price: float, quantity: int, file_size_mb : float, download_url_link : str):
        super().__init__(name, price, quantity)
        self.__file_size_mb = file_size_mb
        self.__download_url_link = download_url_link

    @property
    def get_file_size_mb(self):
        return self.__file_size_mb
    @property
    def get_download_url_link(self):
        return self.__download_url_link
    
    def get_detail(self):
        return f"Song: {self.name}\nPrice: {self.price}$\nQuantity: {self.quantity}\nsize: {self.get_file_size_mb}mb\nLink: {self.get_download_url_link}"

    def __str__(self):
        return f"Song: {self.name}\nPrice: {self.price}$\nQuantity: {self.quantity}\nsize: {self.get_file_size_mb}mb\nLink: {self.get_download_url_link}"

p = PhysicalProduct("Watch",5000.0,5,1,200)

class Cart:
    def __init__(self, username : str):
        if not isinstance(username,str):
            raise TypeError("Use correct username")
        if not username.strip():
            raise ValueError("username cannot be empty")
        self.__username = username
        self.__items = {}

    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self,new_username):
        if not isinstance(new_username,str):
            raise TypeError("use correct data type")
        else:
            self.__username = new_username
    def add_to_cart(self, product: Product, quantity: int):
        if not isinstance(product,Product):
            raise TypeError("Invalid Product")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if quantity == 0:
            return
        if product in self.__items:
            self.__items[product] += quantity
        else:
            self.__items[product] = quantity
    def remove_from_cart(self, product : Product, quantity : int = None) -> None:
        if product not in self.__items:
            raise ValueError("Product not in cart")
        if quantity is None:
            del self.__items[product]
        else:
            if quantity > self.__items[product]:
                raise ValueError("Quantity exceeds availabe")
            self.__items[product] -= quantity
            if self.__items[product] == 0:
                del self.__items[product]
    def get_all_items(self) -> list:
        return list(self.__items.keys())

    def get_item_quantity(self, product: Product) -> int:
        return self.__items.get(product,0)
    def __str__(self):
        return f"Items {self.get_all_items()}"
    
    def calculate_total(self) -> float:
        total = 0
        for product, qty in self.__items.items():
            if isinstance(product, PhysicalProduct):
                total += product.price * qty
            else:
                total += product.price * qty
        return round(total, 2)
    
    def clear_cart(self) -> None:
        self.__items.clear()

class ShoppingUI:
    """User interface for shopping system"""
    
    def __init__(self):
        self.cart = None
        self.products = []
    
    def display_banner(self):
        """Display welcome banner"""
        print("\n" + "="*60)
        print(" "*15 + "🛍️  SHOPPING SYSTEM 🛍️")
        print("="*60 + "\n")
    
    def display_main_menu(self):
        """Display main menu options"""
        print("\n--- MAIN MENU ---")
        print("1. Create New Cart")
        print("2. View Cart")
        print("3. Add Product to Cart")
        print("4. Remove Product from Cart")
        print("5. View Cart Total")
        print("6. Clear Cart")
        print("7. Create Sample Products")
        print("8. Exit")
        print("-" * 30)
    
    def create_cart(self):
        """Create a new shopping cart"""
        try:
            username = input("Enter username: ").strip()
            if not username:
                print("❌ Username cannot be empty!")
                return
            self.cart = Cart(username)
            print(f"✅ Cart created for user: {username}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def create_sample_products(self):
        """Create sample products for testing"""
        try:
            print("\n--- Creating Sample Products ---")
            
            # Physical Products
            p1 = PhysicalProduct("Laptop", 50000.0, 10, 2.5, 500)
            p2 = PhysicalProduct("Watch", 5000.0, 20, 0.2, 100)
            p3 = PhysicalProduct("Headphones", 3000.0, 15, 0.3, 80)
            
            # Digital Products
            d1 = DigitalProduct("Python Course", 999.0, 100, 2500, "https://example.com/python-course")
            d2 = DigitalProduct("Music Album", 199.0, 50, 450, "https://example.com/album")
            d3 = DigitalProduct("E-Book", 299.0, 75, 25, "https://example.com/ebook")
            
            self.products = [p1, p2, p3, d1, d2, d3]
            
            print("Sample products created!")
            for i, product in enumerate(self.products, 1):
                print(f"  {i}. {product.name} - ${product.price}")
        except Exception as e:
            print(f"Error: {e}")
    
    def display_products(self):
        """Display all available products"""
        if not self.products:
            print("No products available. Create sample products first!")
            return
        
        print("\n--- AVAILABLE PRODUCTS ---")
        for i, product in enumerate(self.products, 1):
            product_type = "Physical" if isinstance(product, PhysicalProduct) else "Digital"
            print(f"{i}. {product_type} | {product.name} | Price: ${product.price}")
    
    def add_product_to_cart(self):
        """Add product to cart"""
        if not self.cart:
            print("❌ Please create a cart first!")
            return
        
        if not self.products:
            print("❌ No products available!")
            return
        
        try:
            self.display_products()
            product_idx = int(input("\nEnter product number: ")) - 1
            quantity = int(input("Enter quantity: "))
            
            if 0 <= product_idx < len(self.products):
                product = self.products[product_idx]
                self.cart.add_to_cart(product, quantity)
                print(f"✅ Added {quantity}x {product.name} to cart!")
            else:
                print("❌ Invalid product number!")
        except ValueError:
            print("❌ Please enter valid numbers!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def remove_product_from_cart(self):
        """Remove product from cart"""
        if not self.cart:
            print("❌ Please create a cart first!")
            return
        
        try:
            items = self.cart.get_all_items()
            if not items:
                print("❌ Cart is empty!")
                return
            
            print("\n--- ITEMS IN CART ---")
            for i, product in enumerate(items, 1):
                qty = self.cart.get_item_quantity(product)
                print(f"{i}. {product.name} (Qty: {qty}) - ${product.price}")
            
            item_idx = int(input("\nEnter item number to remove: ")) - 1
            remove_all = input("Remove all? (y/n): ").lower() == 'y'
            
            if 0 <= item_idx < len(items):
                product = items[item_idx]
                if remove_all:
                    self.cart.remove_from_cart(product)
                    print(f"✅ Removed all {product.name} from cart!")
                else:
                    qty_to_remove = int(input(f"Enter quantity to remove (max {self.cart.get_item_quantity(product)}): "))
                    self.cart.remove_from_cart(product, qty_to_remove)
                    print(f"✅ Removed {qty_to_remove}x {product.name} from cart!")
            else:
                print("❌ Invalid item number!")
        except ValueError:
            print("❌ Please enter valid numbers!")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def view_cart(self):
        """View cart contents"""
        if not self.cart:
            print("❌ Please create a cart first!")
            return
        
        items = self.cart.get_all_items()
        if not items:
            print(f"\n🛒 Cart for {self.cart.username} is EMPTY")
            return
        
        print(f"\n🛒 Cart for {self.cart.username}")
        print("-" * 60)
        total = 0
        for i, product in enumerate(items, 1):
            qty = self.cart.get_item_quantity(product)
            item_total = product.price * qty
            total += item_total
            product_type = "📦" if isinstance(product, PhysicalProduct) else "💾"
            print(f"{i}. {product_type} {product.name:<20} | Qty: {qty:>3} | ${product.price:>8} | Subtotal: ${item_total:>10.2f}")
        print("-" * 60)
        print(f"{'TOTAL':>48}: ${total:>10.2f}")
    
    def view_cart_total(self):
        """View total cart amount"""
        if not self.cart:
            print("❌ Please create a cart first!")
            return
        
        total = self.cart.calculate_total()
        items_count = len(self.cart.get_all_items())
        print(f"\n💰 Cart Total: ${total:.2f}")
        print(f"📦 Items: {items_count}")
    
    def clear_cart(self):
        """Clear entire cart"""
        if not self.cart:
            print("❌ Please create a cart first!")
            return
        
        confirm = input("Are you sure you want to clear the cart? (yes/no): ").lower()
        if confirm == 'yes':
            self.cart.clear_cart()
            print("✅ Cart cleared!")
        else:
            print("❌ Cart not cleared!")
    
    def run(self):
        """Run the main application loop"""
        self.display_banner()
        
        while True:
            self.display_main_menu()
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                self.create_cart()
            elif choice == '2':
                self.view_cart()
            elif choice == '3':
                self.add_product_to_cart()
            elif choice == '4':
                self.remove_product_from_cart()
            elif choice == '5':
                self.view_cart_total()
            elif choice == '6':
                self.clear_cart()
            elif choice == '7':
                self.create_sample_products()
            elif choice == '8':
                print("\n👋 Thank you for using Shopping System! Goodbye!\n")
                break
            else:
                print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    app = ShoppingUI()
    app.run()