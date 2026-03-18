# Brute Force Password Cracker

import itertools

def brute_force_password_cracker(password, charset, max_length):
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            attempt = ''.join(attempt)
            if attempt == password:
                return attempt
    return None

# Example usage
password = "secret"
charset = "abcdefghijklmnopqrstuvwxyz"
max_length = 5

cracked_password = brute_force_password_cracker(password, charset, max_length)
if cracked_password:
    print(f"Password cracked: {cracked_password}")
