import json
import os

database = "Projects\Jsons\database.json"


with open(database, "r") as f:
    text = f.read()
    data = json.loads(text)


def shopping_counter():
    sales = 0
    
    print("Welcome to Tesko Mall")
    
    admin = input("Press Enter to shop or enter admin password: ").strip()
    
    # ADMIN PANEL
    if admin == "jarairkhan":
        print("\nWelcome Admin!")
        print("1. List Categories")
        print("2. Add Products to Categories")
        print("3. Change prices of Products")
        print("4. Change name of Categories")
        print("5. Add Categories")
        print("6. Delete category")
        print("7. View Sales")
        
        
        query = int(input("\nEnter Your Choice (1-7): "))
        
        print("Invalid input! Please enter a number.")
            
        
        if query == 1:
            print("\nCategories:")
            for category in data:
                print(f"- {category}")
                for product, price in data[category].items():
                    print(f"  {product}: ${price}")
        
        elif query == 2:
            print("\nSelect which category to add product to:")
            for category in data:
                print(f"- {category}")
            
            category_name = input("\nSelect Category Name: ").strip()
            if category_name in data:
                product = input("Enter product name: ").strip()
                try:
                    price = int(input("Enter Product Price: "))
                    data[category_name][product] = price
                    with open(database, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f'Product "{product}" added successfully to "{category_name}"')
                except ValueError:
                    print("Invalid price! Please enter a number.")
            else:
                print("Invalid Category Name")
        
        elif query == 3:
            print("\nCategories:")
            for category in data:
                print(f"- {category}")
            
            category_name = input("\nSelect Category: ").strip()
            if category_name in data:
                print(f"\nProducts in {category_name}:")
                for product, price in data[category_name].items():
                    print(f"{product}: ${price}")
                
                product_name = input("\nEnter Product Name: ").strip()
                if product_name in data[category_name]:
                    
                    new_price = int(input("Enter New Price: "))
                    data[category_name][product_name] = new_price
                    with open(database, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"The price of {product_name} changed to ${new_price} successfully.")
                    
                    
                else:
                    print("Invalid Product Name")
            else:
                print("Invalid Category Name")
        
        elif query == 4:
            print("\nCurrent Categories:")
            for category in data:
                print(f"- {category}")
            
            old_name = input("\nEnter category name to change: ").strip()
            if old_name in data:
                new_name = input("Enter new category name: ").strip()
                data[new_name] = data.pop(old_name)
                
                with open(database, "w") as f:
                    json.dump(data, f, indent=4)
                
                print(f"Category name changed from '{old_name}' to '{new_name}'.")
                print("\nUpdated Categories:")
                for category in data:
                    print(f"- {category}")
            else:
                print("Invalid category name")
        
        elif query == 5:
            category_name = input("Enter name of new category: ").strip()
            if category_name:
                data[category_name] = {}
                with open(database, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"Category '{category_name}' created successfully.")
                print("\nAll Categories:")
                for category in data:
                    print(f"- {category}")
            else:
                print("Category name cannot be empty!")
        
        elif query == 6:
            print("\nCurrent Categories:")
            for category in data:
                print(f"- {category}")
            
            category_name = input("\nEnter name of category to delete: ").strip()
            if category_name in data:
                confirm = input(f"Are you sure you want to delete '{category_name}'? (y/n): ").lower()
                if confirm == 'y':
                    del data[category_name]
                    with open(database, "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"Category '{category_name}' deleted successfully.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid category name")
        
        elif query == 7:
            print(f"\nTotal Sales Count: {sales}")
        
        else:
            print("Invalid choice! Please enter 1-7.")
    
    # CUSTOMER SHOPPING
    else:
        print("\nWelcome Customer!")
        actual_customer = input("Want to buy products? (y/n): ").lower()
        
        if actual_customer == "n":
            print("Come next time. Goodbye!")
            return
        else:
            total_spent = 0
            
            while True:
                print("\n" + "="*40)
                print("Select a category:")
                for category in data:
                    print(f"- {category}")
                print("="*40)
                
                category_name = input("\nEnter category name (or 'exit' to finish): ").lower().strip()
                
                if category_name == 'exit':
                    print(f"\nThank you for shopping!")
                    print(f"Total items purchased: {sales}")
                    print(f"Total amount spent: ${total_spent}")
                    print("Goodbye! Come again!")
                    break
                
                if category_name in data:
                    if not data[category_name]:
                        print(f"Category '{category_name}' is empty!")
                        continue
                    
                    print(f"\nProducts in {category_name}:")
                    for product, price in data[category_name].items():
                        print(f"{product}: ${price}")
                    
                    product_name = input("\nEnter product name to buy: ").title().strip()
                    
                    if product_name in data[category_name]:
                        price = data[category_name][product_name]
                        print(f"\nPrice of {product_name}: ${price}")
                        
                        confirm = input("Do you want to buy this? (y/n): ").lower()
                        
                        if confirm == "y":
                            
                            credit = int(input("Enter your payment amount: $"))
                                
                            if credit < price:
                                print(f"Insufficient funds! Need ${price - credit} more.")
                                continue
                                
                                # Process purchase
                            change = credit - price
                            sales += 1
                            total_spent += price
                                
                            print("\n" + "="*40)
                            print("✅ PURCHASE SUCCESSFUL!")
                            print(f"Product: {product_name}")
                            print(f"Price: ${price}")
                            print(f"Paid: ${credit}")
                            print(f"Change: ${change}")
                            print(f"Total purchases: {sales}")
                            print("="*40)
                                
                                # Ask if want to buy more
                            more = input("\nDo you want to buy more products? (y/n): ").lower()
                            if more == "n":
                                print(f"\nThank you for shopping!")
                                print(f"Total items purchased: {sales}")
                                print(f"Total amount spent: ${total_spent}")
                                print("Goodbye! Come again!")
                                break
                            
                            
                        else:
                            print("Purchase cancelled.")
                    else:
                        print("Invalid product name!")
                else:
                    print("Invalid category name!")

if __name__ == "__main__":
    shopping_counter()