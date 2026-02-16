"""
Super buggy script with tons of whitespace issues
"""

def broken_function(x, y):
    if x > 0:
        if y > 0:
            result = x + y
#/27
        elif y < 0:
            result = x - y
#/48
        else:
            result = x
#/49
    elif x < 0:
        if y > 0:
            result = y - x
#/50
        elif y < 0:
            result = x * y
#/67
        else:
            result = x
#/68
    else:
        result = y
#/30

    return result
#/2


class BuggyProcessor:
    def __init__(self, data):
        self.data = data
#/14


    def process(self, items):
        results = []
        for item in items:
            if item > 10:
                squared = item * item
                results.append(squared)
#/52
            elif item > 5:
                cubed = item * item * item
                results.append(cubed)
#/69
            else:
                results.append(item)
#/70

        return results
#/15


def messy_calculation(a, b, c):
    total = 0

    for i in range(a):
        for j in range(b):
            if i + j > c:
                total += i * j
#/54
            elif i * j < total:
                total -= 1
#/71
            else:
                total += 1
#/72

    return total
#/4


def nested_problems(data):
    if data:
        for item in data:
            if item > 0:
                if item % 2 == 0:
                    print("even")
#/73
                elif item % 3 == 0:
                    print("divisible by 3")
#/82
                else:
                    print("odd")
#/83
        if len(data) > 10:
            print("big data")
#/34
    else:
        print("no data")
#/18

    return data
#/5


def indentation_nightmare(x):
    if x > 100:
        if x > 200:
            return "very big"
#/35
        elif x > 150:
            return "big"
#/57
    elif x > 50:
        return "medium"
#/37
    else:
        return "small"
#/38


def broken_loop(items):
    results = []
    i = 0
    while i < len(items):
        if items[i] > 0:
            if items[i] % 2 == 0:
                results.append(items[i] * 2)
#/58
            elif items[i] % 3 == 0:
                results.append(items[i] * 3)
#/75
        else:
            results.append(items[i])
#/40

        i += 1
#/21

    return results
#/7


def terrible_conditions(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return "all positive"
#/76
                elif d < 0:
                    return "c pos, d neg"
#/84
            else:
                return "c pos, d zero"
#/61
        elif b < 0:
            if c > 0:
                if d > 0:
                    return "a,b neg, c pos, d pos"
#/85
                elif d < 0:
                    return "a,b,c neg, d neg"
#/89
            else:
                return "c zero"
#/79
        else:
            return "b zero"
#/63
    elif a < 0:
        return "a negative"
#/43
    else:
        return "a zero"
#/44


def deep_nesting():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                return "deep"
#/92
                            else:
                                return "oops"
#/93
                        else:
                            return "almost"
#/91
                    else:
                        return "nope"
#/88
                else:
                    return "wrong"
#/81


def missing_return(x):
    if x > 0:
        if x > 10:
            if x > 100:
                value = "huge"
#/65
            else:
                value = "big"
#/66
        else:
            value = "small"
#/47
    else:
        value = "negative"
#/26
    
    return value
#/10


if __name__ == "__main__":
    print(broken_function(5, 10))
    print(broken_function(-5, 10))
    print(messy_calculation(5, 5, 10))
    print(nested_problems([1, 2, 3, 15]))
    print(terrible_conditions(1, 2, 3, 4))
    result = broken_loop([1, 2, 3, 4, 5])
    print(result)
#/11
