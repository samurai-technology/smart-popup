import os
import unittest

from app.service.EncryptionService import EncryptionService
from app.service.FileService import FileService
from config import Config

context_dir = os.path.dirname(__file__)
config = Config(context_dir)


class EncryptionServiceTestCase(unittest.TestCase):

    def test_encryption_decryption(self):
        encryption_service = EncryptionService(FileService(context_dir, config))
        message = "Secret Message"
        encrypted = encryption_service.encrypt(message)
        decrypted_bytes = encryption_service.decrypt(encrypted)
        self.assertEqual(message.encode(), decrypted_bytes)

    def test_encryption_decryption_to_string(self):
        encryption_service = EncryptionService(FileService(context_dir, config))
        message = "Secret Message"
        encrypted = encryption_service.encrypt_to_string(message)
        decrypted = encryption_service.decrypt_to_string(encrypted)
        self.assertEqual(message, decrypted)


class EncryptionServiceTests:

    def __init__(self):
        self.suite = unittest.TestSuite()
        self.suite.addTest(EncryptionServiceTestCase("test_encryption_decryption"))
        self.suite.addTest(EncryptionServiceTestCase("test_encryption_decryption_to_string"))

    def get_suite(self):
        return self.suite
