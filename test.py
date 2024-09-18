from datetime import datetime

datetime_str = '13:55 19/9/22'

datetime_object = datetime.strptime(datetime_str, '%H:%M %d/%m/%y')

print(type(datetime_object))
print(datetime_object)  # printed in default format
