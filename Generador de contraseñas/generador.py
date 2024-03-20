import re
import secrets
import string


def generate_password(length, nums, special_chars, uppercase, lowercase):
    # Define the possible characters for the password
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    # Combine all characters
    all_characters = letters + digits + symbols

    while True:
        password = ''
        # Generate password
        for _ in range(length):
            password += secrets.choice(all_characters)
       
        constraints = [
            (nums, r'\d'),
            (lowercase, r'[a-z]'),
            (uppercase, r'[A-Z]'),            
            (special_chars, fr'[{symbols}]')            
        ]

        # Check constraints
        if all(  
               
                constraint <= len(re.findall(pattern, password))
                for constraint, pattern in constraints
            
        ):
                break

    return password

# genero la contraseña con caracteres aleatorios e imprimo
if  __name__ == '__main__':
    new_password = generate_password()
    print('Contraseña generada: ', new_password)
