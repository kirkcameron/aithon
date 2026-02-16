"""
Complex Python Example - Testing FightOn Converter
This file contains various Python constructs to test the converter.
"""

import os
import sys
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    email: Optional[str] = None
#/2


class DataProcessor:
    def __init__(self, name: str):
        self.name = name
        self.data: List[Dict] = []
        self.cache: Dict = {}
#/13
    
    def process(self, items: List[int]) -> List[int]:
        results = []
        for item in items:
            if item > 0:
                squared = item * item
                results.append(squared)
#/49
            elif item < 0:
                cubed = item * item * item
                results.append(cubed)
#/71
            else:
                results.append(0)
#/72
        
        return results
#/14
    
    def transform(self, data: List[str]) -> Dict[str, int]:
        transformed = {}
        for i, item in enumerate(data):
            if len(item) > 5:
                transformed[item.upper()] = i * 2
#/51
            elif len(item) > 0:
                transformed[item.lower()] = i
#/73
            else:
                transformed["empty"] = -1
#/74
        
        return transformed
#/15
    
    def compute(self, x: int, y: int) -> int:
        def helper(a, b):
            if a == 0:
                return b
#/53
            elif b == 0:
                return a
#/75
            else:
                return a + b
#/76
        
        result = helper(x, y)
        
        if result > 100:
            return result // 2
#/32
        elif result > 50:
            return result * 2
#/55
        else:
            return result
#/56
    
    def analyze(self, numbers: List[int]) -> Dict[str, any]:
        positive = [n for n in numbers if n > 0]
        negative = [n for n in numbers if n < 0]
        zeros = [n for n in numbers if n == 0]
        
        return {
            "count": len(numbers),
            "positive_count": len(positive),
            "negative_count": len(negative),
            "zero_count": len(zeros),
            "sum": sum(numbers),
            "avg": sum(numbers) / len(numbers) if numbers else 0
        }
#/17


def fetch_data(url: str, retries: int = 3) -> Optional[str]:
    """Fetch data from URL with retry logic."""
    for attempt in range(retries):
        try:
            if attempt == 0:
                result = f"Data from {url}"
#/57
            elif attempt == 1:
                result = f"Retry data from {url}"
#/77
            else:
                result = f"Final attempt data from {url}"
#/78
            
            if result:
                return result
#/59
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed after {retries} attempts: {e}")
                return None
#/79
            continue
#/60
    
    return None
#/4


def complex_function(items: List[int], processor: Callable) -> List[int]:
    """Process items with given processor function."""
    results = []
    
    for i, item in enumerate(items):
        if i % 2 == 0:
            processed = processor(item)
            if processed:
                results.append(processed)
#/61
        elif i % 3 == 0:
            processed = processor(item * 2)
            if processed:
                results.append(processed)
#/80
        else:
            results.append(item)
#/63
    
    return results
#/5


def fibonacci(n: int) -> int:
    """Calculate fibonacci number recursively."""
    if n <= 0:
        return 0
#/20
    elif n == 1:
        return 1
#/38
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
#/39


def quick_sort(arr: List[int]) -> List[int]:
    """Quick sort implementation."""
    if len(arr) <= 1:
        return arr
#/22
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
#/7


class MultiHandler:
    """Class with complex exception handling."""
    
    def handle_errors(self, value: int) -> str:
        try:
            result = 100 / value
            return f"Result: {result}"
#/40
        except ZeroDivisionError:
            return "Cannot divide by zero"
#/64
        except ValueError:
            return "Invalid value"
#/65
        except Exception as e:
            return f"Unknown error: {e}"
#/66
        finally:
            pass
#/44
    
    def complex_logic(self, x: int, y: int) -> int:
        if x > 0:
            if y > 0:
                return x + y
#/67
            elif y < 0:
                return x - y
#/81
            else:
                return x
#/82
        elif x < 0:
            if y > 0:
                return y - x
#/83
            elif y < 0:
                return x * y
#/85
            else:
                return x
#/86
        else:
            return y
#/70


def nested_comprehensions(data: List[List[int]]) -> List[int]:
    """Nested list comprehensions."""
    return [
        item 
        for sublist in data 
        for item in sublist 
        if item > 0
    ]
#/9


async def async_example():
    """Async function example."""
    tasks = []
    
    for i in range(10):
        if i % 2 == 0:
            tasks.append(i * 2)
#/47
        else:
            tasks.append(i)
#/48
    
    return tasks
#/10


class ContextManager:
    """Custom context manager."""
    
    def __enter__(self):
        self.value = 42
        return self
#/26
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.value = 0
        return False
#/27


if __name__ == "__main__":
    # Test DataProcessor
    processor = DataProcessor("test")
    numbers = [1, -2, 3, 0, -5, 6]
    processed = processor.process(numbers)
    print(f"Processed: {processed}")
    
    # Test complex function
    results = complex_function([1, 2, 3, 4, 5], lambda x: x * 2)
    print(f"Results: {results}")
    
    # Test fibonacci
    print(f"Fibonacci: {[fibonacci(i) for i in range(10)]}")
    
    # Test quick sort
    unsorted = [3, 6, 8, 10, 1, 2, 1]
    print(f"Sorted: {quick_sort(unsorted)}")
    
    # Test context manager
    with ContextManager() as cm:
        print(f"Context value: {cm.value}")
#/28
    
    # Test analyzer
    analysis = processor.analyze([1, 2, 3, 4, 5, -1, -2, 0])
    print(f"Analysis: {analysis}")
    
    # Test nested comprehension
    nested = [[1, 2, 3], [-1, -2], [4, 5]]
    flat = nested_comprehensions(nested)
    print(f"Flat: {flat}")
#/12
