import re

with open("regex_sum_37014.txt","r") as f:
    f = f.read()
    numbers = re.findall('([0-9]+)',f)
    for x in numbers:
        numbers[numbers.index(x)] = int(x)

    print(sum(numbers))
