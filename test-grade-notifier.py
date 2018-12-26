import os

instance_file_url = "/home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier/"

print("Starting test suite.....")

print("1. Pylint")
os.system('pylint grade-notifier.py')

print("2. Testing Diff")
os.system('{0}grade-notifier.py --test --test_diff'.format(instance_file_url))

print("3. Testing Add/Remove Instance")
os.system('{0}grade-notifier.py --test --test_add_remove_instance'.format(instance_file_url))

print("4. Testing Message Construction")
os.system('{0}grade-notifier.py --test --test_message_contruction'.format(instance_file_url))
