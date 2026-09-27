# week5_lab.py
# Author: Noah Chavez
# Business domain: Instruments

product_name = "Guitar"
status = "Pending"
quantity = 1
unit_price = 750
is_over_limit = unit_price * quantity > 1800

print(type(product_name), type(quantity), type(unit_price), type(is_over_limit))

subtotal = unit_price * quantity
tax = subtotal * 0.07
total = subtotal + tax
requires_approval = total > 1000

print("=== Purchase Request Summary ===")
print(f"Product:  {product_name}")
print(f"Qty:      {quantity}")
print(f"Subtotal: ${subtotal:.2f}")
print(f"Tax:      ${tax:.2f}")
print(f"Total:    ${total:.2f}")
print(f"Requires approval: {requires_approval}")

user_qty = int(input("Enter a new quantity: "))
new_total = unit_price * user_qty * 1.07
print(f"New total for {user_qty} units: ${new_total:.2f}")
print(f"Requires approval: {new_total > 1000}")
