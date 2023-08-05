import unittest

from securenative.utils.encryption_utils import EncryptionUtils


class EncryptionUtilsTest(unittest.TestCase):

    def setUp(self):
        self.SECRET_KEY = "B00C42DAD33EAC6F6572DA756EA4915349C0A4F6"
        self.PAYLOAD = "{\"cid\":\"198a41ff-a10f-4cda-a2f3-a9ca80c0703b\",\"vi\":\"148a42ff-b40f-4cda-a2f3-a8ca80c0703b\",\"fp\":\"6d8cabd95987f8318b1fe01593d5c2a5.24700f9f1986800ab4fcc880530dd0ed\"}"
        self.CID = "198a41ff-a10f-4cda-a2f3-a9ca80c0703b"
        self.FP = "6d8cabd95987f8318b1fe01593d5c2a5.24700f9f1986800ab4fcc880530dd0ed"

    def test_decrypt(self):
        result = EncryptionUtils.encrypt(self.PAYLOAD, self.SECRET_KEY)

        self.assertIsNotNone(result)
        self.assertGreater(len(self.PAYLOAD), len(result))

    def test_encrypt(self):
        encrypted_payload = "5208ae703cc2fa0851347f55d3b76d3fd6035ee081d71a401e8bc92ebdc25d42440f62310bda60628537744ac03f200d78da9e61f1019ce02087b7ce6c976e7b2d8ad6aa978c532cea8f3e744cc6a5cafedc4ae6cd1b08a4ef75d6e37aa3c0c76954d16d57750be2980c2c91ac7ef0bbd0722abd59bf6be22493ea9b9759c3ff4d17f17ab670b0b6fc320e6de982313f1c4e74c0897f9f5a32d58e3e53050ae8fdbebba9009d0d1250fe34dcde1ebb42acbc22834a02f53889076140f0eb8db1"
        result = EncryptionUtils.decrypt(encrypted_payload, self.SECRET_KEY)

        self.assertEqual(result.cid, self.CID)
        self.assertEqual(result.fp, self.FP)

    def test_encrypt_decrypt(self):
        enc_res = EncryptionUtils.encrypt(self.PAYLOAD, self.SECRET_KEY)
        dec_res = EncryptionUtils.decrypt(enc_res, self.SECRET_KEY)

        self.assertIsNotNone(dec_res)
        self.assertIsNotNone(enc_res)

    def test_encrypt_with_invalid_key_length(self):
        with self.assertRaises(ValueError):
            secret_key = "BAD_KEY"
            EncryptionUtils.encrypt(self.PAYLOAD, secret_key)

    def test_decrypt_with_invalid_key_length(self):
        with self.assertRaises(ValueError):
            secret_key = "BAD_KEY"
            encrypted_payload = "5208ae703cc2fa0851347f55d3b76d3fd6035ee081d71a401e8bc92ebdc25d42440f62310bda60628537744ac03f200d78da9e61f1019ce02087b7ce6c976e7b2d8ad6aa978c532cea8f3e744cc6a5cafedc4ae6cd1b08a4ef75d6e37aa3c0c76954d16d57750be2980c2c91ac7ef0bbd0722abd59bf6be22493ea9b9759c3ff4d17f17ab670b0b6fc320e6de982313f1c4e74c0897f9f5a32d58e3e53050ae8fdbebba9009d0d1250fe34dcde1ebb42acbc22834a02f53889076140f0eb8db1"
            EncryptionUtils.decrypt(encrypted_payload, secret_key)

    def test_encrypt_decrypt_with_key_too_long(self):
        with self.assertRaises(ValueError):
            secret_key = "B00C42DAD33EAC6F6572DA756EA4915349C0A4F6B00C42DAD33EAC6F6572DA756EA4915349C0A4F6";
            enc_res = EncryptionUtils.encrypt(self.PAYLOAD, secret_key)
            EncryptionUtils.decrypt(enc_res, secret_key)
