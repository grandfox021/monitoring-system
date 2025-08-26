import random, string
def random_pass(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(chars) for _ in range(length))
with open("random_users.txt", "w") as f:
    for i in range(1, 10001):
        f.write(f"user{i}:{random_pass()}\n")