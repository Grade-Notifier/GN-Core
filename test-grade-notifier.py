import os

print("Starting test suite.....")

print("1. Pylint")
os.system('pylint grade-notifier.py')

print("2. Testing Diff")
os.system('grade-notifier.py --test --test_diff')

print("3. Testing Add/Remove Instance")
os.system('grade-notifier.py --test --test_add_remove_instance')

print("4. Testing Message Construction")
os.system('grade-notifier.py --test --test_message_contruction')
