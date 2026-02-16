"""
Super buggy script with tons of whitespace issues
"""

def broken_function(x, y):
    if x > 0:
        if y > 0:
            result = x + y

        elif y < 0:
            result = x - y

        else:
            result = x

    elif x < 0:
        if y > 0:
            result = y - x

        elif y < 0:
            result = x * y

        else:
            result = x

    else:
        result = y

    return result

class BuggyProcessor:
    def __init__(self, data):
        self.data = data

    def process(self, items):
        results = []
        for item in items:
            if item > 10:
                squared = item * item
                results.append(squared)

            elif item > 5:
                cubed = item * item * item
                results.append(cubed)

            else:
                results.append(item)

        return results

def messy_calculation(a, b, c):
    total = 0

    for i in range(a):
        for j in range(b):
            if i + j > c:
                total += i * j

            elif i * j < total:
                total -= 1

            else:
                total += 1

    return total

def nested_problems(data):
    if data:
        for item in data:
            if item > 0:
                if item % 2 == 0:
                    print("even")

                elif item % 3 == 0:
                    print("divisible by 3")

                else:
                    print("odd")

        if len(data) > 10:
            print("big data")

    else:
        print("no data")

    return data

def indentation_nightmare(x):
    if x > 100:
        if x > 200:
            return "very big"

        elif x > 150:
            return "big"

    elif x > 50:
        return "medium"

    else:
        return "small"

def broken_loop(items):
    results = []
    i = 0
    while i < len(items):
        if items[i] > 0:
            if items[i] % 2 == 0:
                results.append(items[i] * 2)

            elif items[i] % 3 == 0:
                results.append(items[i] * 3)

        else:
            results.append(items[i])

        i += 1

    return results

def terrible_conditions(a, b, c, d):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    return "all positive"

                elif d < 0:
                    return "c pos, d neg"

            else:
                return "c pos, d zero"

        elif b < 0:
            if c > 0:
                if d > 0:
                    return "a,b neg, c pos, d pos"

                elif d < 0:
                    return "a,b,c neg, d neg"

            else:
                return "c zero"

        else:
            return "b zero"

    elif a < 0:
        return "a negative"

    else:
        return "a zero"

def deep_nesting():
    if True:
        if True:
            if True:
                if True:
                    if True:
                        if True:
                            if True:
                                return "deep"

                            else:
                                return "oops"

                        else:
                            return "almost"

                    else:
                        return "nope"

                else:
                    return "wrong"

def missing_return(x):
    if x > 0:
        if x > 10:
            if x > 100:
                value = "huge"

            else:
                value = "big"

        else:
            value = "small"

    else:
        value = "negative"

    return value

if __name__ == "__main__":
    print(broken_function(5, 10))
    print(broken_function(-5, 10))
    print(messy_calculation(5, 5, 10))
    print(nested_problems([1, 2, 3, 15]))
    print(terrible_conditions(1, 2, 3, 4))
    result = broken_loop([1, 2, 3, 4, 5])
    print(result)
