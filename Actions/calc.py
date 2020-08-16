def calc(msg):
    sum=0
    x=msg
    if "+" in msg:
        numbers=x.split(" + ")
        for number in numbers:
            sum+=int(number)
        return sum
    if "-" in msg:
        numbers=x.split(" - ")
        sum=int(numbers[0])-int(numbers[1])
        return sum
    if "x" in msg:
        sum=1
        numbers=x.split(" x ")
        for number in numbers:
            sum*=int(number)
        return sum
