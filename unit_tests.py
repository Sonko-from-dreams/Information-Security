import unittest
from Lab_1_Randomizer import analyze, get_period, generate_rand_num
from Lab_2_MD5_algorithm import md5_hash, verify_file_integrity
from Lab_3_RC5_algorithm import encrypt, encrypt_cbc, decrypt, decrypt_cbc
from Lab_4_RSA_algorithm import generate_keys, save_keys, encrypt_rca, decrypt_rca, load_private_key_bytes, encrypt_chunks, decrypt_chunks, load_public_key_bytes
from cryptography.hazmat.primitives import serialization

class TestLab1(unittest.TestCase):
    # тест для перевірки генерації пвч
    def test_generation(self):
        result = generate_rand_num(10)
        self.assertEqual(result, [973, 1035, 1772, 727, 620, 1230, 29, 907, 1373, 2026])

    # тест для перевірки генерації пвч
    def test_generation_false(self):
        result = generate_rand_num(10)
        self.assertNotEqual(result, [973, 1035, 177, 727, 620, 1230, 29, 907, 1373, 2026])

    # тест для перевірки отриманих пі та похибки
    def test_analysis(self):
        pi, err = analyze(100000, generate_rand_num(100000))
        req_pi = 2.89501
        req_err = 0.24659

        error_1 = abs(pi - req_pi)
        error_2 = abs(err - req_err)

        x = error_1 <= 0.00001 and error_2 <= 0.00001

        self.assertTrue(x)

    # тест для перевірки періоду
    def test_period(self):
        period = get_period()
        self.assertEqual(period, 88)

class TestLab2(unittest.TestCase):
    # тести для перевірки хешування
    def test_hash_1(self):
        result = md5_hash(b'')
        self.assertEqual(result, ('D41D8CD98F00B204E9800998ECF8427E'.lower()))

    def test_hash_2(self):
        result = md5_hash(b'a')
        self.assertEqual(result, ('0CC175B9C0F1B6A831C399E269772661'.lower()))

    def test_hash_3(self):
        result = md5_hash(b'abc')
        self.assertEqual(result, ('900150983CD24FB0D6963F7D28E17F72'.lower()))

    def test_hash_4(self):
        result = md5_hash(b'message digest')
        self.assertEqual(result, ('F96B697D7CB7938D525A2F31AAF161D0'.lower()))

    def test_hash_5(self):
        result = md5_hash(b'abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(result, ('C3FCD3D76192E4007DFB496CCA67E13B'.lower()))

    def test_hash_6(self):
        result = md5_hash(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        self.assertEqual(result, ('D174AB98D277D9F5A5611C2C9F419D9F'.lower()))

    def test_hash_7(self):
        result = md5_hash(b'12345678901234567890123456789012345678901234567890123456789012345678901234567890')
        self.assertEqual(result, ('57EDF4A22BE3C955AC49DA2E2107B67A'.lower()))

    #тест для перевірки цілісності файлу
    def test_integrity(self):
        file = 'D:/Sofi/Information Security/test_file.txt'
        hash_file = 'D:/Sofi/Information Security/test_hash.txt'
        result = verify_file_integrity(file, hash_file)
        self.assertEqual(result, True)

    def test_integrity_wrong(self):
        file = 'D:/Sofi/Information Security/test_file.txt'
        hash_file = 'D:/Sofi/Information Security/test_hash_wrong.txt'
        result = verify_file_integrity(file, hash_file)
        self.assertEqual(result, False)


class TestLab3(unittest.TestCase):
    # змінні мого варіанту
    w, r, b = 16, 8, 16

    # тест для перевірки шифрування RC5
    def test_encryption(self):
        key = "iloveis"
        d = b'HELL'
        enc = encrypt(self.w, self.r, self.b, key, d)

        self.assertEqual(enc.hex(), '4ad7d18e')

    # тест для перевірки дешифрування RC5
    def test_decryption(self):
        key = "iloveis"
        d = b'HELL'
        enc = encrypt(self.w, self.r, self.b, key, d)
        dec = decrypt(self.w, self.r, self.b, key, enc)

        self.assertEqual(dec, d)

    # тест для перевірки кодування CBC
    def test_encryption_cbc(self):
        key = "my_secret_key"
        text = b'I am the hero the world has longed for'
        encr = encrypt_cbc(self.w, self.r, self.b, key, text)
        result = decrypt_cbc(self.w, self.r, self.b, key, encr)
        self.assertEqual(result, text)

class TestLab4(unittest.TestCase):
    # тест шифру RSA
    def test_encryption(self):
        text = 'Hello world'
        key = b'key'
        priv_key, pub_key = generate_keys()
        enc_mess = encrypt_rca(text, pub_key)
        dec_mess = decrypt_rca(enc_mess, priv_key)
        self.assertEqual(dec_mess.decode(), text)

    # тест шифру RSA для файлів довільного розміру
    def test_bloc_encryption(self):
        text = b'Hello world'
        key = b'key'
        priv_key, pub_key = generate_keys()
        enc_mess = encrypt_chunks(text, pub_key)
        dec_mess = decrypt_chunks(enc_mess, priv_key)
        self.assertEqual(dec_mess, text)

    # тест запису публічного ключа у файл
    def test_keys_public(self):
        test_priv_key, test_pub_key = generate_keys()
        save_keys(test_priv_key, test_pub_key, b'keys')
        public_key = load_public_key_bytes('public_key')
        self.assertEqual(public_key, test_pub_key)

    # тест запису приватного ключа у файл
    def test_keys_private(self):
        test_priv_key, test_pub_key = generate_keys()
        save_keys(test_priv_key, test_pub_key, b'keys')
        private_key = load_private_key_bytes('private_key', 'keys')
        test_pem = test_priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        loaded_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        self.assertEqual(test_pem, loaded_pem)

if __name__ == '__main__':
    unittest.main()