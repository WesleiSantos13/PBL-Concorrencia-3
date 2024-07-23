from infra.config import config
from datetime import datetime, timedelta
import time

# timestamp1 = datetime.now()
# time.sleep(2)
# timestamp2 = datetime.now()
# difference = abs(timestamp1 - timestamp2)


# print(   difference > timedelta(seconds=3)   )
# print(datetime.now())

# input_string = "342391"

# # Agrupar em pares de dígitos
# ascii_values = [input_string[i:i+2] for i in range(0, len(input_string), 2)]

# # Converter para caracteres ASCII
# ascii_chars = [chr(int(value)) for value in ascii_values]

# # Unir os caracteres em uma string
# output_string = ''.join(ascii_chars)

# print(output_string)

import ast

string_list = "['172.16.103.7', '172.16.103.11', '172.16.103.4']"
print(ast.literal_eval(string_list))
