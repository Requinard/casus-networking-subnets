class Subnet:
    """
    Holds data for a subnet.

    IRL I'd use a library like netaddr to do this.
    """

    def __init__(self, complete_address=None, ip_number=None, subnet_mask=None):
        if complete_address:
            net_split = complete_address.split("/")

            self.subnetmask = int(net_split[1])
            self.quads = [int(x) for x in net_split[0].split(".")]
            self.address_int = 0

            for i in range(4):
                shift_range = (3 - i) * 8
                shifted = self.quads[i] << shift_range
                self.address_int = self.address_int ^ shifted
        elif ip_number and subnet_mask:
            self.address_int = ip_number
            self.subnetmask = subnet_mask
        else:
            raise ValueError("We cannot parse this!")

    def __str__(self):
        return f"{self.convert_number_to_string()}/{self.subnetmask}"

    def __repr__(self):
        return self.__str__()

    def convert_number_to_string(self) -> str:
        q1 = self.address_int >> 24
        q2 = (self.address_int & (255 << 16)) >> 16
        q3 = (self.address_int & (255 << 8)) >> 8
        q4 = self.address_int & 255

        return f"{q1}.{q2}.{q3}.{q4}"

    def __sub__(self, other):
        if not isinstance(other, Subnet):
            raise ValueError("I'm sorry, but I'm afraid I cannot do that")

        if other.subnetmask < self.subnetmask:
            raise ValueError("We cannot subtract from a subnetmask greater than out own")

        results = []

        for subnet_mask in reversed(range(self.subnetmask + 1, other.subnetmask + 1)):
            mask_bits = 2 ** (32 - subnet_mask)  # Get the new mask
            new_subnet_number = other.address_int ^ mask_bits  # Calculate the new IP range
            new_subnet_number &= ~(mask_bits - 1)  # Discard all bits that no longer subnet, but are now addresses
            new_subnet = Subnet(ip_number=new_subnet_number, subnet_mask=subnet_mask)

            results.append(new_subnet)

        return results


if __name__ == '__main__':
    a = Subnet("192.168.1.0/24")
    b = Subnet("192.168.1.16/29")

    print(a)
    print(b)
    print(a - b)
