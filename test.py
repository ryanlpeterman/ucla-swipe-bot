import unittest
import messenger_interface as fb

from subprocess import call

class TestMessengerInterface(unittest.TestCase):
    # my person fb uid: for ryan peterman
    my_uid = 1118923488216801

    def test_send_message(self):
        res_code = fb.send_message(self.my_uid, fb.setup_str("Test 1"))
        self.assertEqual(res_code, 200)

    def test_send_buyer_question(self):
        res_code = fb.send_message(self.my_uid, fb.init_user())
        self.assertEqual(res_code, 200)

    def test_send_location_question(self):
        res_code = fb.send_message(self.my_uid, fb.init_location())
        self.assertEqual(res_code, 200)

if __name__ == '__main__':
    unittest.main()