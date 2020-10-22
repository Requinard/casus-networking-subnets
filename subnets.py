from unittest import TestCase


class Subnet:
    """
    Holds data for a subnet.

    IRL I'd use a library like netaddr to do this.
    """

    def __init__(self, complete_address=None, ip_number=None, subnet_mask=None):
        if complete_address:
            # If we're handed a complete address, we first start by translating it into some numbers
            net_split = complete_address.split("/")

            assert len(net_split) == 2

            self.subnet_mask = int(net_split[1])

            quads = [int(x) for x in net_split[0].split(".")]
            self.address_int = 0

            for i in range(4):
                shift_range = (3 - i) * 8
                shifted = quads[i] << shift_range
                self.address_int ^= shifted

        elif ip_number and subnet_mask:
            # If we're initialized with ip_number and subnet_mask, read them directly
            self.address_int = ip_number
            self.subnet_mask = subnet_mask
        else:
            # if none of these holds, raise an error
            raise ValueError("We cannot parse this!")

    def __str__(self):
        return f"{self.address}/{self.subnet_mask}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Subnet):
            raise ValueError("Cannot compare this subnet to a not-subnet")

        return self.address_int == other.address_int and self.subnet_mask == other.subnet_mask

    @property
    def address(self) -> str:
        """
        Converts the address number into its string representation
        """
        q1 = self.address_int >> 24
        q2 = (self.address_int & (255 << 16)) >> 16
        q3 = (self.address_int & (255 << 8)) >> 8
        q4 = self.address_int & 255

        return f"{q1}.{q2}.{q3}.{q4}"

    def __sub__(self, other):
        """
        Overwrite subtract operator to get proper subnet subtracting
        """
        if not isinstance(other, Subnet):
            raise ValueError("I'm sorry, but I'm afraid I cannot do that")

        if other.subnet_mask < self.subnet_mask:
            raise ValueError("We cannot subtract from a subnetmask greater than out own")

        results = []

        for subnet_mask in reversed(range(self.subnet_mask + 1, other.subnet_mask + 1)):
            mask_bits = 2 ** (32 - subnet_mask)  # Get the new mask
            new_subnet_number = other.address_int ^ mask_bits  # Calculate the new IP range
            new_subnet_number &= ~(mask_bits - 1)  # Discard all bits that no longer subnet, but are now addresses
            new_subnet = Subnet(ip_number=new_subnet_number, subnet_mask=subnet_mask)

            results.append(new_subnet)

        return results


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

    def test_subtracting_self_returns_empty(self):
        result = self.a - self.a

        self.assertEqual(0, len(result))

    def test_subtracting_outside_raises_error(self):
        with self.assertRaises(ValueError):
            self.b - self.a
