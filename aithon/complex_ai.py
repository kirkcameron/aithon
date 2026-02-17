"""
Super buggy script with tons of whitespace issues
"""

#/5
def broken_function(x, y):
#/6
    if x > 0:
#/7
        if y > 0:
            result = x + y
#/9
      elif y < 0:
            result = x - y
       else:
           result = x
#/13
  elif x < 0:
#/14
      if y > 0:
          result = y - x
#/16
        elif y < 0:
            result = x * y
      else:
            result = x
      else:
          result = y

    return result


#/26
class BuggyProcessor:
#/27
    def __init__(self, data):
        self.data = data


#/31
    def process(self, items):
        results = []
#/33
      for item in items:
#/34
            if item > 10:
                squared = item * item
            results.append(squared)
#/37
      elif item > 5:
                cubed = item * item * item
                results.append(cubed)
            else:
                results.append(item)

          return results


#/46
def messy_calculation(a, b, c):
    total = 0

#/49
  for i in range(a):
#/50
      for j in range(b):
#/51
        if i + j > c:
              total += i * j
#/53
            elif i * j < total:
            total -= 1
        else:
              total += 1

    return total


#/61
def nested_problems(data):
#/62
    if data:
#/63
        for item in data:
#/64
          if item > 0:
#/65
              if item % 2 == 0:
                    print("even")
#/67
               elif item % 3 == 0:
                    print("divisible by 3")
              else:
                    print("odd")
#/71
      elif len(data) > 10:
            print("big data")
    else:
        print("no data")

      return data


#/79
def indentation_nightmare(x):
#/80
    if x > 100:
#/81
          if x > 200:
              return "very big"
#/83
      elif x > 150:
              return "big"
#/85
    elif x > 50:
            return "medium"
      else:
          return "small"


#/91
def broken_loop(items):
    results = []
  i = 0
#/94
    while i < len(items):
#/95
        if items[i] > 0:
#/96
            if items[i] % 2 == 0:
                  results.append(items[i] * 2)
#/98
          elif items[i] % 3 == 0:
                results.append(items[i] * 3)
        else:
              results.append(items[i])

      i += 1

        return results


#/108
def terrible_conditions(a, b, c, d):
#/109
    if a > 0:
#/110
        if b > 0:
#/111
          if c > 0:
#/112
              if d > 0:
                  return "all positive"
#/114
            elif d < 0:
                return "c pos, d neg"
          else:
              return "c pos, d zero"
#/118
        elif b < 0:
#/119
              if c > 0:
#/120
                  if d > 0:
                      return "a,b neg, c pos, d pos"
#/122
              elif d < 0:
                    return "a,b,c neg, d neg"
            else:
                  return "c zero"
        else:
              return "b zero"
#/128
  elif a < 0:
        return "a negative"
      else:
          return "a zero"


#/134
def deep_nesting():
#/135
    if True:
#/136
        if True:
#/137
            if True:
#/138
                if True:
#/139
                    if True:
#/140
                        if True:
#/141
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


#/153
def missing_return(x):
#/154
    if x > 0:
#/155
        if x > 10:
#/156
            if x > 100:
                value = "huge"
            else:
                value = "big"
        else:
            value = "small"
    else:
        value = "negative"


#/166
if __name__ == "__main__":
    print(broken_function(5, 10))
    print(broken_function(-5, 10))
    print(messy_calculation(5, 5, 10))
    print(nested_problems([1, 2, 3, 15]))
    print(terrible_conditions(1, 2, 3, 4))
    result = broken_loop([1, 2, 3, 4, 5])
    print(result)
