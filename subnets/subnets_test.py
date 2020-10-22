from unittest import TestCase

from subnets import Subnet


class SubnetsTests(TestCase):
    a = Subnet("192.168.1.0/24")
    b = Subnet("192.168.1.16/29")

    def test_regular_networks_work(self):
        result = self.a - self.b
        expected = [
            Subnet(complete_address="192.168.1.24/29"),
            Subnet(complete_address="192.168.1.0/28"),
            Subnet(complete_address="192.168.1.32/27"),
            Subnet(complete_address="192.168.1.64/26"),
            Subnet(complete_address="192.168.1.128/25")
        ]

        self.assertEqual(5, len(result))
        self.assertEqual(expected, result)

    def test_extra_case1(self):
        c = Subnet(complete_address="1.2.3.4/30")
        d = Subnet(complete_address="1.2.3.5/32")

        expected = [
            Subnet(complete_address="1.2.3.4/32"), Subnet(complete_address="1.2.3.6/31")
        ]

        self.assertEqual(expected, c-d)

    def test_extra_case2(self):
        c = Subnet(complete_address="192.168.1.0/24")
        d = Subnet(complete_address="192.168.1.128/25")

        expected = [
            Subnet(complete_address="192.168.1.0/25")
        ]

        self.assertEqual(expected, c-d)

    def test_subtracting_self_returns_empty(self):
        result = self.a - self.a

        self.assertEqual(0, len(result))

    def test_subtracting_outside_raises_error(self):
        with self.assertRaises(ValueError):
            self.b - self.a
