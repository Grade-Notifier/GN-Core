import os

instance_file_url = "/home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier/"

print("Starting test suite.....")

print("1. Pylint")
os.system('pylint grade-notifier.py')

print("\n2. Testing Diff")
os.system('python3 {0}grade-notifier.py --test=true --test_diff=true'.format(instance_file_url))

print("\n3. Testing Add/Remove Instance")
os.system('rm /home/fa18/313/adeh6562/public_html/grade-notifier/test-instances.txt')
os.system('touch /home/fa18/313/adeh6562/public_html/grade-notifier/test-instances.txt')
os.system('python3 {0}grade-notifier.py --test=true --test_add_remove_instance=true'.format(instance_file_url))

print("\n4. Testing Message Construction")
os.system('python3 {0}grade-notifier.py --test=true --test_message_contruction=true'.format(instance_file_url))
