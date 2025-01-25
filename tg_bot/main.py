from check import check_imei

props:dict = check_imei("356735111052198")['properties']

result = "\n".join(f'"{key}": "{value}"' for key, value in props.items())

print(result)

