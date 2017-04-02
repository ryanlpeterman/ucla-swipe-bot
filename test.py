import unittest
import messenger_interface as fb
import database as db
import match as m
from subprocess import call

class TestMessengerInterface(unittest.TestCase):
    # my person fb uid: for ryan peterman
    # my_uid = 1118923488216801
    my_uid = 1439331329412505

    def test_send_message(self):
        res_code = fb.send_message(self.my_uid, fb.setup_str("Test 1"))
        self.assertEqual(res_code, 200)

    def test_send_buyer_question(self):
        res_code = fb.send_message(self.my_uid, fb.init_user())
        self.assertEqual(res_code, 200)

    def test_send_location_question(self):
        res_code = fb.send_message(self.my_uid, fb.init_location())
        self.assertEqual(res_code, 200)

    def test_send_time_question(self):
        res_code = fb.send_message(self.my_uid, fb.setup_time())
        self.assertEqual(res_code, 200)

class TestDatabase(unittest.TestCase):
    def test_add_user(self):
        db.reset_db()
        # insert user
        test_user = {unicode('id'):1234, unicode('buyer'):True}
        db.update_user_obj(test_user)

        get_user = db.get_user_obj(1234)
        self.assertEqual(get_user, test_user)

    def test_set_buyer(self):
        db.reset_db()
        db.set_buyer(1234, True)

        get_user = db.get_user_obj(1234)
        self.assertEqual(get_user["is_buyer"], True)

    def test_add_hall(self):
        db.reset_db()
        db.add_hall(1234, "bplate")

        get_user = db.get_user_obj(1234)
        self.assertEqual(get_user["where"], ["bplate"])

        db.add_hall(1234, "deneve")
        get_user = db.get_user_obj(1234)
        self.assertEqual("bplate" in get_user["where"], True)
        self.assertEqual("deneve" in get_user["where"], True)
        self.assertEqual(len(get_user["where"]), 2)

    def test_add_time(self):
        db.reset_db()
        db.add_time(1234, 4)

        get_user = db.get_user_obj(1234)
        self.assertEqual(get_user["when"], [4])

        db.add_time(1234, 5)
        get_user = db.get_user_obj(1234)
        self.assertEqual(4 in get_user["when"], True)
        self.assertEqual(5 in get_user["when"], True)
        self.assertEqual(len(get_user["when"]), 2)

    def test_user_complete(self):
        db.reset_db()

        db.add_time(1234, 4)
        self.assertEqual(db.is_user_complete(1234), False)

        db.add_hall(1234, "bplate")
        self.assertEqual(db.is_user_complete(1234), False)

        db.set_buyer(1234, True)
        self.assertEqual(db.is_user_complete(1234), True)

class TestMatch(unittest.TestCase):
    def test_matching(self):
        m.init()
        usr1 = {'id':1234, 'where':['BPLATE', 'DENEVE'], 'when':[8], 'is_buyer':False, 'price':7}
        res1 = m.add_complete_user(usr1)
        self.assertEqual([], res1)

        usr2 = {'id':6969, 'where':['BPLATE'], 'when':[8], 'is_buyer':True, 'price':7}
        res2 = m.add_complete_user(usr2)
        self.assertEqual([(1234, 6969, 'BPLATE', 8, 7)], res2)

if __name__ == '__main__':
    unittest.main()