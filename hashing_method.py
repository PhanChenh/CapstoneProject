import random
import string
import hashlib 

# Class for hashing and pseudonymization
class HashPseudonymization:
    def __init__(self):
        self.encryption_key = self.generate_encryption_key()
        self.pseudonym_mapping = {}

    @staticmethod
    def generate_encryption_key():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # 16 characters long key

    @staticmethod
    def hash_value_with_key(value, key):
        value_with_key = f'{value}_{key}'
        return hashlib.sha256(value_with_key.encode()).hexdigest()

    def generate_pseudonym(self, index, column_name):
        return f'{column_name}_{chr(65 + index)}'  # Pseudonyms like columnName_A, columnName_B, etc.

    def apply_hashing(self, df, column):
        if self.encryption_key:
            df[f'{column} Hashed'] = df[column].apply(lambda loc: self.hash_value_with_key(loc, self.encryption_key))

    def apply_pseudonymization(self, df, column):
        unique_values = df[column].unique()
        for index, value in enumerate(unique_values):
            hashed_value = self.hash_value_with_key(value, self.encryption_key)
            self.pseudonym_mapping[hashed_value] = self.generate_pseudonym(index, column)
        df[f'{column} Pseudonymized'] = df[column].apply(lambda loc: self.pseudonym_mapping[self.hash_value_with_key(loc, self.encryption_key)])
