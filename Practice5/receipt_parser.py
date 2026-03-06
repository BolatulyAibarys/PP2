import re
import json

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# 1. Extract all prices
prices = re.findall(r'\b\d{1,3}(?: \d{3})*,\d{2}\b', text)

# 2. Find all product names
product_names = re.findall(r'^\d+\.\s*\n(.+)', text, re.MULTILINE)

# 3. Calculate total amount
total_match = re.search(r'ИТОГО:\s*\n?(\d{1,3}(?: \d{3})*,\d{2})', text)
total_amount = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else None

# 4. Extract date and time
datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None

# 5. Find payment method
payment_match = re.search(r'(Банковская карта|Наличными|Карта)', text)
payment_method = payment_match.group(1) if payment_match else None

# 6. Structured output
products = re.findall(
    r'^\d+\.\s*\n(.+?)\n(\d+,\d{3}) x (\d{1,3}(?: \d{3})*,\d{2})\n(\d{1,3}(?: \d{3})*,\d{2})',
    text,
    re.MULTILINE
)

items = []
for name, qty, unit_price, cost in products:
    items.append({
        "name": name.strip(),
        "quantity": qty,
        "unit_price": float(unit_price.replace(" ", "").replace(",", ".")),
        "cost": float(cost.replace(" ", "").replace(",", "."))
    })

result = {
    "all_prices": prices,
    "product_names": product_names,
    "total_amount": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "items": items
}

print(json.dumps(result, ensure_ascii=False, indent=4))