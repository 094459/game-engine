"""Generate 20 varied coding questions (Java, Python, TypeScript) and import via API."""
import requests

BASE = "http://127.0.0.1:5001"
TOKEN = requests.post(f"{BASE}/api/auth/token").json()["token"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# ──────────────────────────────────────────────
# Python questions (7 questions)
# ──────────────────────────────────────────────
python_questions = [
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "python",
        "description": "Given a list of numbers, find the second largest value. Input: - nums: A list of numbers",
        "correct_answer": "result = sorted(set(nums), reverse=True)[1]",
        "code_sample_input": "{'nums': [10, 5, 20, 15, 8]}",
        "code_sample_output": "15",
        "code_hidden_input": "{'nums': [100, 200, 50, 150, 75]}",
        "code_hidden_output": "150",
        "hint": "Sort the unique values in descending order and pick the second one.",
    },
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "python",
        "description": "Count how many times a specific character appears in a string (case-insensitive). Input: - s: A string - char: Character to count",
        "correct_answer": "result = s.lower().count(char.lower())",
        "code_sample_input": "{'s': 'Hello World', 'char': 'l'}",
        "code_sample_output": "3",
        "code_hidden_input": "{'s': 'Programming', 'char': 'g'}",
        "code_hidden_output": "2",
        "hint": "Convert both to lowercase and use the count() method.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "python",
        "description": "Given a list of words, group them by their first letter. Return a dictionary where keys are letters and values are lists of words. Input: - words: A list of words",
        "correct_answer": "result = {}\nfor word in words:\n    first = word[0].lower()\n    if first not in result:\n        result[first] = []\n    result[first].append(word)",
        "code_sample_input": "{'words': ['apple', 'banana', 'apricot', 'blueberry', 'cherry']}",
        "code_sample_output": "{'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}",
        "code_hidden_input": "{'words': ['dog', 'cat', 'duck', 'cow', 'deer']}",
        "code_hidden_output": "{'d': ['dog', 'duck', 'deer'], 'c': ['cat', 'cow']}",
        "hint": "Iterate through words and build a dictionary using the first letter as the key.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "python",
        "description": "Calculate the factorial of a number using iteration. Input: - n: A non-negative integer",
        "correct_answer": "result = 1\nfor i in range(1, n + 1):\n    result *= i",
        "code_sample_input": "{'n': 5}",
        "code_sample_output": "120",
        "code_hidden_input": "{'n': 7}",
        "code_hidden_output": "5040",
        "hint": "Multiply all integers from 1 to n.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "python",
        "description": "Remove all duplicate values from a list while preserving the original order. Input: - items: A list of items",
        "correct_answer": "seen = set()\nresult = []\nfor item in items:\n    if item not in seen:\n        seen.add(item)\n        result.append(item)",
        "code_sample_input": "{'items': [1, 2, 2, 3, 4, 3, 5]}",
        "code_sample_output": "[1, 2, 3, 4, 5]",
        "code_hidden_input": "{'items': ['a', 'b', 'a', 'c', 'b', 'd']}",
        "code_hidden_output": "['a', 'b', 'c', 'd']",
        "hint": "Use a set to track seen items and build a new list.",
    },
    {
        "category": "Coding",
        "difficulty": "Hard",
        "code_programming_language": "python",
        "description": "Find all prime numbers up to n using the Sieve of Eratosthenes. Return them as a list. Input: - n: Upper limit (exclusive)",
        "correct_answer": "sieve = [True] * n\nif n > 0:\n    sieve[0] = False\nif n > 1:\n    sieve[1] = False\nfor i in range(2, int(n**0.5) + 1):\n    if sieve[i]:\n        for j in range(i*i, n, i):\n            sieve[j] = False\nresult = [i for i in range(n) if sieve[i]]",
        "code_sample_input": "{'n': 20}",
        "code_sample_output": "[2, 3, 5, 7, 11, 13, 17, 19]",
        "code_hidden_input": "{'n': 30}",
        "code_hidden_output": "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]",
        "hint": "Create a boolean array and mark multiples of each prime as non-prime.",
    },
    {
        "category": "Coding",
        "difficulty": "Hard",
        "code_programming_language": "python",
        "description": "Rotate a list to the right by k positions. Input: - arr: A list - k: Number of positions to rotate",
        "correct_answer": "k = k % len(arr) if arr else 0\nresult = arr[-k:] + arr[:-k] if k else arr",
        "code_sample_input": "{'arr': [1, 2, 3, 4, 5], 'k': 2}",
        "code_sample_output": "[4, 5, 1, 2, 3]",
        "code_hidden_input": "{'arr': [10, 20, 30, 40], 'k': 3}",
        "code_hidden_output": "[20, 30, 40, 10]",
        "hint": "Use list slicing to move the last k elements to the front.",
    },
]

# ──────────────────────────────────────────────
# TypeScript questions (7 questions)
# ──────────────────────────────────────────────
typescript_questions = [
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "typescript",
        "description": "Check if a number is even or odd. Set `result` to 'even' or 'odd'. Input: - num: A number",
        "correct_answer": "const result = num % 2 === 0 ? 'even' : 'odd';",
        "code_sample_input": '{"num": 4}',
        "code_sample_output": "even",
        "code_hidden_input": '{"num": 7}',
        "code_hidden_output": "odd",
        "hint": "Use the modulo operator to check divisibility by 2.",
    },
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "typescript",
        "description": "Find the minimum value in an array of numbers. Input: - nums: An array of numbers",
        "correct_answer": "const result = Math.min(...nums);",
        "code_sample_input": '{"nums": [5, 2, 9, 1, 7]}',
        "code_sample_output": "1",
        "code_hidden_input": '{"nums": [100, 50, 75, 25]}',
        "code_hidden_output": "25",
        "hint": "Use Math.min with the spread operator.",
    },
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "typescript",
        "description": "Reverse a string. Input: - s: A string",
        "correct_answer": "const result = s.split('').reverse().join('');",
        "code_sample_input": '{"s": "hello"}',
        "code_sample_output": "olleh",
        "code_hidden_input": '{"s": "typescript"}',
        "code_hidden_output": "tpircsepyt",
        "hint": "Split the string into an array, reverse it, then join back.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "typescript",
        "description": "Count the frequency of each character in a string. Return an object with characters as keys and counts as values. Input: - s: A string",
        "correct_answer": "const result: Record<string, number> = {}; for (const c of s) { result[c] = (result[c] || 0) + 1; }",
        "code_sample_input": '{"s": "hello"}',
        "code_sample_output": '{"h": 1, "e": 1, "l": 2, "o": 1}',
        "code_hidden_input": '{"s": "aabbcc"}',
        "code_hidden_output": '{"a": 2, "b": 2, "c": 2}',
        "hint": "Loop through each character and increment its count in an object.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "typescript",
        "description": "Find the sum of all odd numbers in an array. Input: - nums: An array of numbers",
        "correct_answer": "const result = nums.filter((n: number) => n % 2 !== 0).reduce((sum: number, n: number) => sum + n, 0);",
        "code_sample_input": '{"nums": [1, 2, 3, 4, 5]}',
        "code_sample_output": "9",
        "code_hidden_input": '{"nums": [10, 15, 20, 25, 30]}',
        "code_hidden_output": "40",
        "hint": "Filter odd numbers and use reduce to sum them.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "typescript",
        "description": "Check if a string is a palindrome (reads the same forwards and backwards, case-insensitive). Input: - s: A string",
        "correct_answer": "const clean = s.toLowerCase(); const result = clean === clean.split('').reverse().join('');",
        "code_sample_input": '{"s": "Racecar"}',
        "code_sample_output": "true",
        "code_hidden_input": '{"s": "hello"}',
        "code_hidden_output": "false",
        "hint": "Convert to lowercase, reverse it, and compare with the original.",
    },
    {
        "category": "Coding",
        "difficulty": "Hard",
        "code_programming_language": "typescript",
        "description": "Find the missing number in an array containing n distinct numbers from 0 to n. Input: - nums: An array of numbers",
        "correct_answer": "const n = nums.length; const expectedSum = (n * (n + 1)) / 2; const actualSum = nums.reduce((sum: number, num: number) => sum + num, 0); const result = expectedSum - actualSum;",
        "code_sample_input": '{"nums": [0, 1, 3, 4, 5]}',
        "code_sample_output": "2",
        "code_hidden_input": '{"nums": [0, 1, 2, 3, 5, 6, 7]}',
        "code_hidden_output": "4",
        "hint": "Calculate the expected sum using the formula n*(n+1)/2 and subtract the actual sum.",
    },
]

# ──────────────────────────────────────────────
# Java questions (6 questions)
# ──────────────────────────────────────────────
java_questions = [
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "java",
        "description": 'Check if a number is positive, negative, or zero. Given n as JSON, return "positive", "negative", or "zero". Example: {"n": -5} → "negative"',
        "correct_answer": 'public static String solve(String input) {\n    String clean = input.replaceAll("[{}\\"]", "");\n    int n = Integer.parseInt(clean.split(":")[1].trim());\n    return n > 0 ? "positive" : n < 0 ? "negative" : "zero";\n}',
        "code_sample_input": '{"n": 10}',
        "code_sample_output": "positive",
        "code_hidden_input": '{"n": 0}',
        "code_hidden_output": "zero",
        "hint": "Parse n and use conditional logic to determine the sign.",
    },
    {
        "category": "Coding",
        "difficulty": "Easy",
        "code_programming_language": "java",
        "description": 'Count the number of words in a sentence. Given s as JSON, return the word count. Example: {"s": "hello world"} → "2"',
        "correct_answer": 'public static String solve(String input) {\n    String s = input.split(":")[1].trim().replaceAll("[}\\"]", "").trim();\n    if (s.isEmpty()) return "0";\n    return String.valueOf(s.split("\\\\s+").length);\n}',
        "code_sample_input": '{"s": "the quick brown fox"}',
        "code_sample_output": "4",
        "code_hidden_input": '{"s": "Java programming language"}',
        "code_hidden_output": "3",
        "hint": "Split the string on whitespace and count the resulting array length.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "java",
        "description": 'Find the sum of digits in a number. Given n as JSON, return the sum. Example: {"n": 123} → "6"',
        "correct_answer": 'public static String solve(String input) {\n    String clean = input.replaceAll("[{}\\"]", "");\n    int n = Integer.parseInt(clean.split(":")[1].trim());\n    int sum = 0;\n    n = Math.abs(n);\n    while (n > 0) {\n        sum += n % 10;\n        n /= 10;\n    }\n    return String.valueOf(sum);\n}',
        "code_sample_input": '{"n": 456}',
        "code_sample_output": "15",
        "code_hidden_input": '{"n": 789}',
        "code_hidden_output": "24",
        "hint": "Extract each digit using modulo 10 and divide by 10 repeatedly.",
    },
    {
        "category": "Coding",
        "difficulty": "Moderate",
        "code_programming_language": "java",
        "description": 'Check if a number is a perfect square. Given n as JSON, return "true" or "false". Example: {"n": 16} → "true"',
        "correct_answer": 'public static String solve(String input) {\n    String clean = input.replaceAll("[{}\\"]", "");\n    int n = Integer.parseInt(clean.split(":")[1].trim());\n    int sqrt = (int) Math.sqrt(n);\n    return String.valueOf(sqrt * sqrt == n);\n}',
        "code_sample_input": '{"n": 25}',
        "code_sample_output": "true",
        "code_hidden_input": '{"n": 26}',
        "code_hidden_output": "false",
        "hint": "Take the square root, convert to integer, and check if squaring it gives the original number.",
    },
    {
        "category": "Coding",
        "difficulty": "Hard",
        "code_programming_language": "java",
        "description": 'Calculate the power of a number (x^y) without using Math.pow(). Given x and y as JSON, return the result. Example: {"x": 2, "y": 3} → "8"',
        "correct_answer": 'public static String solve(String input) {\n    String clean = input.replaceAll("[{}\\"]", "");\n    String[] parts = clean.split(",");\n    int x = 0, y = 0;\n    for (String p : parts) {\n        String[] kv = p.split(":");\n        String key = kv[0].trim();\n        int val = Integer.parseInt(kv[1].trim());\n        if (key.equals("x")) x = val;\n        else if (key.equals("y")) y = val;\n    }\n    long result = 1;\n    for (int i = 0; i < y; i++) result *= x;\n    return String.valueOf(result);\n}',
        "code_sample_input": '{"x": 3, "y": 4}',
        "code_sample_output": "81",
        "code_hidden_input": '{"x": 5, "y": 3}',
        "code_hidden_output": "125",
        "hint": "Use a loop to multiply x by itself y times.",
    },
    {
        "category": "Coding",
        "difficulty": "Hard",
        "code_programming_language": "java",
        "description": 'Find the largest prime factor of a number. Given n as JSON, return the largest prime factor. Example: {"n": 15} → "5"',
        "correct_answer": 'public static String solve(String input) {\n    String clean = input.replaceAll("[{}\\"]", "");\n    long n = Long.parseLong(clean.split(":")[1].trim());\n    long largest = -1;\n    while (n % 2 == 0) {\n        largest = 2;\n        n /= 2;\n    }\n    for (long i = 3; i * i <= n; i += 2) {\n        while (n % i == 0) {\n            largest = i;\n            n /= i;\n        }\n    }\n    if (n > 2) largest = n;\n    return String.valueOf(largest);\n}',
        "code_sample_input": '{"n": 28}',
        "code_sample_output": "7",
        "code_hidden_input": '{"n": 100}',
        "code_hidden_output": "5",
        "hint": "Divide by 2 repeatedly, then check odd numbers up to sqrt(n).",
    },
]

# ──────────────────────────────────────────────
# Import all questions via the API
# ──────────────────────────────────────────────
all_questions = python_questions + typescript_questions + java_questions

print(f"Importing {len(all_questions)} coding questions ({len(python_questions)} Python, {len(typescript_questions)} TypeScript, {len(java_questions)} Java)...\n")

resp = requests.post(
    f"{BASE}/api/questions/import",
    headers=HEADERS,
    json={"questions": all_questions},
)

if resp.status_code == 201:
    data = resp.json()
    print(f"Successfully imported {data['imported']} questions.\n")
    for q in data["questions"]:
        lang = q.get("code_programming_language", "?")
        print(f"  Q{q['id']} [{lang:10s}] [{q['difficulty']:8s}] {q['description'][:70]}...")
else:
    print(f"Import failed ({resp.status_code}): {resp.text}")
