import copy
import random
from abc import ABC, abstractmethod

# 1. BUILDER 

class ProductBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.product_type = None
        self.name = "Producto Personalizado"
        self.price = 0.0
        self.line = "Estándar"
        self.specs = {}
        return self
    
    def set_type(self, product_type):
        self.product_type = product_type
        return self
    
    def set_name(self, name):
        self.name = name
        return self
    
    def set_price(self, price):
        self.price = price
        return self
    
    def set_line(self, line):
        self.line = line
        return self
    
    def add_spec(self, key, value):
        self.specs[key] = value
        return self
    
    def build(self):
        if self.product_type == "computer":
            return Computer(self.name, self.price, self.line, self.specs.get("processor", "i5"))
        elif self.product_type == "phone":
            return Phone(self.name, self.price, self.line, self.specs.get("storage", "128GB"))
        elif self.product_type == "tablet":
            return Tablet(self.name, self.price, self.line, self.specs.get("screen", "10.5'"))
        return None
    
# 2. PROTOTYPE

class ElectronicProduct(ABC):
    def __init__(self, name: str, price: float, line: str):
        self.name = name
        self.price = price
        self.line = line
        self.id = random.randint(1000, 9999)
    
    @abstractmethod
    def get_specifications(self):
        pass
    
    def clone(self):
        cloned = copy.deepcopy(self)
        cloned._apply_random_variations()
        cloned.id = random.randint(1000, 9999)
        return cloned
    
    def _apply_random_variations(self):
        price_variation = random.uniform(0.7, 1.3)
        self.price = round(self.price * price_variation, 2)
        
        suffixes = ["Plus", "Pro", "Max", "Edition", "Custom", "Limited", "Turbo"]
        if random.random() > 0.4:
            self.name = f"{self.name} {random.choice(suffixes)}"

        if random.random() > 0.8:
            lines = ["Económica", "Estándar", "Premium"]
            if self.line in lines:
                lines.remove(self.line)
                self.line = random.choice(lines)
    
    def __str__(self):
        return f"{self.name} (Línea {self.line}) - ${self.price:.2f} [ID:{self.id}]"

class Computer(ElectronicProduct):
    def __init__(self, name: str, price: float, line: str, processor: str = None):
        super().__init__(name, price, line)
        self.processor = processor or self._get_default_processor(line)
        self.ram = self._get_default_ram(line)
    
    def _get_default_processor(self, line):
        processors = {"Premium": "Intel i9", "Estándar": "Intel i5", "Económica": "Intel i3"}
        return processors.get(line, "Intel i5")
    
    def _get_default_ram(self, line):
        ram = {"Premium": "32GB", "Estándar": "16GB", "Económica": "8GB"}
        return ram.get(line, "16GB")
    
    def _apply_random_variations(self):
        super()._apply_random_variations()
        if random.random() > 0.6:
            processors = ["Intel i7", "AMD Ryzen 7", "Intel i9", "AMD Ryzen 9"]
            self.processor = random.choice(processors)
    
    def get_specifications(self):
        return f"💻 {self.name} | 🚀 {self.processor} | 🎯 {self.ram} | 📊 Línea: {self.line}"

class Phone(ElectronicProduct):
    def __init__(self, name: str, price: float, line: str, storage: str = None):
        super().__init__(name, price, line)
        self.storage = storage or self._get_default_storage(line)
        self.camera = self._get_default_camera(line)
    
    def _get_default_storage(self, line):
        storages = {"Premium": "512GB", "Estándar": "256GB", "Económica": "128GB"}
        return storages.get(line, "128GB")
    
    def _get_default_camera(self, line):
        cameras = {"Premium": "200MP", "Estándar": "108MP", "Económica": "48MP"}
        return cameras.get(line, "48MP")
    
    def _apply_random_variations(self):
        super()._apply_random_variations()
        if random.random() > 0.5:
            storages = ["64GB", "128GB", "256GB", "512GB"]
            self.storage = random.choice(storages)
    
    def get_specifications(self):
        return f"📱 {self.name} | 💾 {self.storage} | 📸 {self.camera} | 📊 Línea: {self.line}"

class Tablet(ElectronicProduct):
    def __init__(self, name: str, price: float, line: str, screen: str = None):
        super().__init__(name, price, line)
        self.screen = screen or self._get_default_screen(line)
        self.battery = self._get_default_battery(line)
    
    def _get_default_screen(self, line):
        screens = {"Premium": "12.9' Retina", "Estándar": "11' LCD", "Económica": "10.2' LCD"}
        return screens.get(line, "10.5' LCD")
    
    def _get_default_battery(self, line):
        batteries = {"Premium": "12 horas", "Estándar": "10 horas", "Económica": "8 horas"}
        return batteries.get(line, "9 horas")
    
    def _apply_random_variations(self):
        super()._apply_random_variations()
        if random.random() > 0.65:
            screens = ["10.1'", "10.5'", "11'", "12.9'"]
            self.screen = f"{random.choice(screens)} LCD"
    
    def get_specifications(self):
        return f"📟 {self.name} | 🖥️ {self.screen} | 🔋 {self.battery} | 📊 Línea: {self.line}"
    
# 3. FACTORY METHOD - Creación Especializada

class ProductFactory(ABC):
    @abstractmethod
    def create_computer(self) -> Computer:
        pass
    
    @abstractmethod
    def create_phone(self) -> Phone:
        pass
    
    @abstractmethod
    def create_tablet(self) -> Tablet:
        pass

class GamingFactory(ProductFactory):
    def create_computer(self) -> Computer:
        return Computer("Gaming Beast", 2000.00, "Premium", "Ryzen 9")
    
    def create_phone(self) -> Phone:
        return Phone("Gaming Phone X", 800.00, "Premium", "256GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("Gaming Tab Pro", 600.00, "Estándar", "11'")

class OfficeFactory(ProductFactory):
    def create_computer(self) -> Computer:
        return Computer("Office Master", 800.00, "Estándar", "i5")
    
    def create_phone(self) -> Phone:
        return Phone("Business Phone", 400.00, "Estándar", "128GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("Office Tablet", 300.00, "Económica", "10.2'")

class StudentFactory(ProductFactory):
    def create_computer(self) -> Computer:
        return Computer("Student Laptop", 600.00, "Económica", "i3")
    
    def create_phone(self) -> Phone:
        return Phone("Campus Phone", 250.00, "Económica", "64GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("Study Pad", 200.00, "Económica", "10.1'")

# 4. ABSTRACT FACTORY

class LineFactory(ABC):
    @abstractmethod
    def create_computer(self) -> Computer:
        pass
    
    @abstractmethod
    def create_phone(self) -> Phone:
        pass
    
    @abstractmethod
    def create_tablet(self) -> Tablet:
        pass

class PremiumLineFactory(LineFactory):
    def create_computer(self) -> Computer:
        return Computer("Quantum Pro", 2500.00, "Premium", "Intel i9")
    
    def create_phone(self) -> Phone:
        return Phone("Galaxy Ultra", 1200.00, "Premium", "512GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("iPad Pro Max", 1500.00, "Premium", "12.9'")

class StandardLineFactory(LineFactory):
    def create_computer(self) -> Computer:
        return Computer("Workstation Plus", 1200.00, "Estándar", "Intel i5")
    
    def create_phone(self) -> Phone:
        return Phone("Nova Prime", 600.00, "Estándar", "256GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("Tab Advanced", 400.00, "Estándar", "11'")

class EconomicLineFactory(LineFactory):
    def create_computer(self) -> Computer:
        return Computer("Essential Basic", 500.00, "Económica", "Intel i3")
    
    def create_phone(self) -> Phone:
        return Phone("Spark Lite", 200.00, "Económica", "128GB")
    
    def create_tablet(self) -> Tablet:
        return Tablet("Simple Pad", 150.00, "Económica", "10.2'")

# 5. DECORATOR

class ProductDecorator(ABC):
    def __init__(self, product: ElectronicProduct):
        self.product = product
    
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_total_price(self):
        pass

class WarrantyDecorator(ProductDecorator):
    def get_description(self):
        return f"{self.product.name} 🛡️ +2 años garantía"
    
    def get_total_price(self):
        return self.product.price + 100

class AccessoriesDecorator(ProductDecorator):
    def get_description(self):
        return f"{self.product.name} 🎧 +Kit accesorios"
    
    def get_total_price(self):
        return self.product.price + 50

class DiscountDecorator(ProductDecorator):
    def get_description(self):
        return f"{self.product.name} 🎯 OFERTA ESPECIAL"
    
    def get_total_price(self):
        return self.product.price * 0.85  # 15% descuento

class PremiumSupportDecorator(ProductDecorator):
    def get_description(self):
        return f"{self.product.name} ⭐ Soporte premium 24/7"
    
    def get_total_price(self):
        return self.product.price + 150



# CATÁLOGO Y MENÚ PRINCIPAL

class ProductCatalog:
    def __init__(self):
        self.products = []
    
    def add_product(self, product):
        self.products.append(product)
        print(f"✅ Producto agregado: {product}")
    
    def show_catalog(self):
        if not self.products:
            print("\n📭 El catálogo está vacío")
            return
            
        print("\n📋 CATÁLOGO DE PRODUCTOS:")
        print("=" * 70)
        for i, product in enumerate(self.products, 1):
            print(f"{i}. {product}")
            print(f"   📝 {product.get_specifications()}")
            print()
        print("=" * 70)
    
    def clone_product(self, index):
        if 0 <= index < len(self.products):
            original = self.products[index]
            cloned = original.clone()
            self.add_product(cloned)
            return cloned
        return None
    
    def decorate_product(self, index, decorator_type):
        if 0 <= index < len(self.products):
            product = self.products[index]
            
            if decorator_type == "1":
                decorated = WarrantyDecorator(product)
            elif decorator_type == "2":
                decorated = AccessoriesDecorator(product)
            elif decorator_type == "3":
                decorated = DiscountDecorator(product)
            elif decorator_type == "4":
                decorated = PremiumSupportDecorator(product)
            else:
                return None
            
            print(f"🎁 {decorated.get_description()}")
            print(f"💰 Precio original: ${product.price:.2f}")
            print(f"💰 Precio final: ${decorated.get_total_price():.2f}")
            return decorated
        
        return None
    
    def get_stats(self):
        if not self.products:
            return "No hay productos en el catálogo"
        
        computers = sum(1 for p in self.products if isinstance(p, Computer))
        phones = sum(1 for p in self.products if isinstance(p, Phone))
        tablets = sum(1 for p in self.products if isinstance(p, Tablet))
        total_value = sum(p.price for p in self.products)
        
        return f"📊 Estadísticas: 💻{computers} 📱{phones} 📟{tablets} | Valor total: ${total_value:.2f}"
    
def mostrar_menu():
    print("\n" + "=" * 60)
    print("🏪 SISTEMA DE GESTIÓN ELECTRÓNICA")
    print("=" * 60)
    print("1. 🏭 Factory Method (Gaming/Oficina/Estudiante)")
    print("2. 🏗️ Abstract Factory (Premium/Estándar/Económica)")
    print("3. 🔨 Builder (Producto Personalizado)")
    print("4. 🌀 Prototype (Clonar con variaciones)")
    print("5. 🎨 Decorator (Agregar funcionalidades)")
    print("6. 📋 Mostrar Catálogo")
    print("7. 📊 Estadísticas")
    print("8. 🚪 Salir")
    print("=" * 60)

def main():
    catalog = ProductCatalog()
    
    while True:
        mostrar_menu()
        opcion = input("👉 Selecciona una opción: ").strip()
        
        if opcion == "1":
            print("\n🏭 FACTORY METHOD:")
            print("1. 🎮 Fábrica Gaming")
            print("2. 💼 Fábrica Oficina") 
            print("3. 🎓 Fábrica Estudiante")
            sub_op = input("Selecciona fábrica: ")
            
            if sub_op == "1":
                factory = GamingFactory()
                print("🎮 Creando productos gaming...")
            elif sub_op == "2":
                factory = OfficeFactory()
                print("💼 Creando productos oficina...")
            else:
                factory = StudentFactory()
                print("🎓 Creando productos estudiante...")
            
            catalog.add_product(factory.create_computer())
            catalog.add_product(factory.create_phone())
            catalog.add_product(factory.create_tablet())
        
        elif opcion == "2":
            print("\n🏗️ ABSTRACT FACTORY:")
            print("1. ⭐ Línea Premium")
            print("2. 🔷 Línea Estándar")
            print("3. 💰 Línea Económica")
            sub_op = input("Selecciona línea: ")
            
            if sub_op == "1":
                factory = PremiumLineFactory()
                print("⭐ Creando línea premium...")
            elif sub_op == "2":
                factory = StandardLineFactory()
                print("🔷 Creando línea estándar...")
            else:
                factory = EconomicLineFactory()
                print("💰 Creando línea económica...")
            
            catalog.add_product(factory.create_computer())
            catalog.add_product(factory.create_phone())
            catalog.add_product(factory.create_tablet())
        
        elif opcion == "3":
            print("\n🔨 BUILDER - Crear Producto Personalizado:")
            builder = ProductBuilder()
            
            print("Tipos disponibles: computer, phone, tablet")
            p_type = input("Tipo de producto: ")
            name = input("Nombre del producto: ")
            price = float(input("Precio: $"))
            line = input("Línea (Premium/Estándar/Económica): ")
            
            product = (builder.reset()
                      .set_type(p_type)
                      .set_name(name)
                      .set_price(price)
                      .set_line(line)
                      .build())
            
            if product:
                catalog.add_product(product)
            else:
                print("❌ Error: Tipo de producto no válido")
        
        elif opcion == "4":
            print("\n🌀 PROTOTYPE - Clonar Producto:")
            catalog.show_catalog()
            if catalog.products:
                try:
                    idx = int(input("Número del producto a clonar: ")) - 1
                    cloned = catalog.clone_product(idx)
                    if cloned:
                        print(f"✅ Clon creado exitosamente!")
                except (ValueError, IndexError):
                    print("❌ Número de producto no válido")
        
        elif opcion == "5":
            print("\n🎨 DECORATOR - Agregar funcionalidades:")
            catalog.show_catalog()
            if catalog.products:
                try:
                    idx = int(input("Número del producto a decorar: ")) - 1
                    print("Decoradores disponibles:")
                    print("1. 🛡️ Garantía extendida (+$100)")
                    print("2. 🎧 Kit de accesorios (+$50)") 
                    print("3. 🎯 Descuento especial (15% off)")
                    print("4. ⭐ Soporte premium (+$150)")
                    dec_type = input("Selecciona decorador: ")
                    
                    catalog.decorate_product(idx, dec_type)
                except (ValueError, IndexError):
                    print("❌ Número de producto no válido")
        
        elif opcion == "6":
            catalog.show_catalog()
        
        elif opcion == "7":
            print(f"\n{catalog.get_stats()}")
        
        elif opcion == "8":
            print("👋 ¡Gracias por usar el sistema! Hasta pronto!")
            break
        
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()