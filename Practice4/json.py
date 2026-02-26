import json

# loading JSON from file
with open("sample-data.json") as f:
    data = json.load(f)    #читаем JSON в виде словаря

#Creating articles of the table
print("Interface Status")
print("="*79)
print(f"{'DN':<50} {'Description':<20} {'Speed':<6} {'MTU':<6}")
print("-"*50 + " " + "-"*20 + " " + "-"*6 + " " + "-"*6)

#Going through each interface
for item in data["imdata"]:    #список интерфейсов
    attr = item["l1PhysIf"]["attributes"]   #ишет словать по ключу "l1PhysIf" и врутри него еще 1 словар по
    #ключу "attributes" и берет все данные из него, потом присваевает на переменную attr
    dn = attr.get("dn", "")     #берем dn, descr, speed, mtu для каждого интерфейса
    descr = attr.get("descr", "")     #без get() код может выдать ошибку если там нет нечего чтобы вывести
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")
    
    #printing string and выравнование короче
    print(f"{dn:<50} {descr:<20} {speed:<6} {mtu:<6}")