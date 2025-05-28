import pytest
from BitMask import BitMask

import pytest
from your_package import BitMask  # Assuming your BitMask class is in 'your_package' directory

class TestBitMask:
    def test_initialization(self):
        bm = BitMask(8)
        assert bm.max_length == 8
        assert bm.value == 0

        bm_with_value = BitMask(10, 5)
        assert bm_with_value.max_length == 10
        assert bm_with_value.value == 5

    def test_initialization_errors(self):
        with pytest.raises(TypeError):
            BitMask("8")
        with pytest.raises(ValueError):
            BitMask(0)
        with pytest.raises(ValueError):
            BitMask(-5)
        with pytest.raises(TypeError):
            BitMask(8, "5")
        with pytest.raises(ValueError):
            BitMask(8, -1)
        with pytest.raises(ValueError):
            BitMask(8, 256) # 256 is 1 << 8

    def test_max_length_property(self):
        bm = BitMask(16)
        assert bm.max_length == 16

    def test_value_property(self):
        bm = BitMask(5, 7)
        assert bm.value == 7
        bm.value = 15
        assert bm.value == 15

    def test_value_setter_errors(self):
        bm = BitMask(4)
        with pytest.raises(TypeError):
            bm.value = "3"
        with pytest.raises(ValueError):
            bm.value = -1
        with pytest.raises(ValueError):
            bm.value = 16 # 16 is 1 << 4

    def test_set_bit(self):
        bm = BitMask(8)
        bm.set_bit(0)
        assert bm.value == 1
        bm.set_bit(3)
        assert bm.value == 9 # 1001 in binary

    def test_set_bit_errors(self):
        bm = BitMask(4)
        with pytest.raises(TypeError):
            bm.set_bit("2")
        with pytest.raises(IndexError):
            bm.set_bit(4)
        with pytest.raises(IndexError):
            bm.set_bit(-1) # Negative index should raise IndexError

    def test_set_all(self):
        bm = BitMask(5)
        bm.set_all()
        assert bm.value == 31 # 11111 in binary

    def test_flip_bit(self):
        bm = BitMask(6, 10) # 001010
        bm.flip_bit(1)
        assert bm.value == 8  # 001000
        bm.flip_bit(4)
        assert bm.value == 24 # 011000

    def test_flip_bit_errors(self):
        bm = BitMask(3)
        with pytest.raises(TypeError):
            bm.flip_bit(1.5)
        with pytest.raises(IndexError):
            bm.flip_bit(3)
        with pytest.raises(IndexError):
            bm.flip_bit(-2) # Negative index should raise IndexError

    def test_flip_all(self):
        bm = BitMask(4, 5) # 0101
        bm.flip_all()
        assert bm.value == 10 # 1010

    def test_reset_bit(self):
        bm = BitMask(7, 55) # 0110111
        bm.reset_bit(0)
        assert bm.value == 54 # 0110110
        bm.reset_bit(3)
        assert bm.value == 46 # 0101110

    def test_reset_bit_errors(self):
        bm = BitMask(2)
        with pytest.raises(TypeError):
            bm.reset_bit([0])
        with pytest.raises(IndexError):
            bm.reset_bit(2)
        with pytest.raises(IndexError):
            bm.reset_bit(-3) # Negative index should raise IndexError

    def test_reset_all(self):
        bm = BitMask(6, 63) # 111111
        bm.reset_all()
        assert bm.value == 0

    def test_reverse_bit_order(self):
        bm = BitMask(4, 5) # 0101
        bm.reverse_bit_order()
        assert bm.value == 10 # 1010

        bm2 = BitMask(7, 21) # 0010101
        bm2.reverse_bit_order()
        assert bm2.value == 42 # 1010100

    def test_get_bit(self):
        bm = BitMask(5, 13) # 01101
        assert bm.get_bit(0) == 1
        assert bm.get_bit(1) == 0
        assert bm.get_bit(2) == 1
        assert bm.get_bit(3) == 1
        assert bm.get_bit(4) == 0

    def test_get_bit_errors(self):
        bm = BitMask(3, 3)
        with pytest.raises(TypeError):
            bm.get_bit({0})
        with pytest.raises(IndexError):
            bm.get_bit(3)
        with pytest.raises(IndexError):
            bm.get_bit(-1) # Negative index should raise IndexError

    def test_get_count(self):
        bm = BitMask(8, 170) # 10101010
        assert bm.get_count() == 4
        bm2 = BitMask(6, 63) # 111111
        assert bm2.get_count() == 6
        bm3 = BitMask(4, 0)
        assert bm3.get_count() == 0

    def test_get_non_zero(self):
        bm = BitMask(7, 45) # 0101101
        assert bm.get_non_zero() == (0, 2, 3, 5)
        bm2 = BitMask(3, 0)
        assert bm2.get_non_zero() == ()

    def test_get_zero(self):
        bm = BitMask(5, 13) # 01101
        assert bm.get_zero() == (1, 4)
        bm2 = BitMask(4, 15) # 1111
        assert bm2.get_zero() == ()

    def test_get_lsb(self):
        bm = BitMask(8, 40) # 00101000
        assert bm.get_lsb() == 3
        bm2 = BitMask(5, 1) # 00001
        assert bm2.get_lsb() == 0
        bm3 = BitMask(3, 0)
        assert bm3.get_lsb() == -1

    def test_set_binary(self):
        bm = BitMask(6)
        bm.set_binary("101101")
        assert bm.value == 45
        bm.set_binary("00011")
        bm2 = BitMask(5)
        bm2.set_binary("11")
        assert bm2.value == 3

    def test_set_binary_errors(self):
        bm = BitMask(4)
        with pytest.raises(TypeError):
            bm.set_binary(101)
        with pytest.raises(ValueError):
            bm.set_binary("1201")
        with pytest.raises(ValueError):
            bm.set_binary("11111") # Longer than max_length 4
        with pytest.raises(ValueError):
            bm.set_binary("-10")

    def test_set_hexadecimal(self):
        bm = BitMask(8)
        bm.set_hexadecimal("A5")
        assert bm.value == 165
        bm2 = BitMask(4)
        bm2.set_hexadecimal("F")
        assert bm2.value == 15

    def test_set_hexadecimal_errors(self):
        bm = BitMask(4)
        with pytest.raises(TypeError):
            bm.set_hexadecimal(0xA)
        with pytest.raises(ValueError):
            bm.set_hexadecimal("G")
        with pytest.raises(ValueError):
            bm.set_hexadecimal("100") # Longer than max_length 4 (in bits)
        with pytest.raises(ValueError):
            bm.set_hexadecimal("-1")

    def test_set_decimal(self):
        bm = BitMask(7)
        bm.set_decimal(42)
        assert bm.value == 42

    def test_set_decimal_errors(self):
        bm = BitMask(3)
        with pytest.raises(TypeError):
            bm.set_decimal("5")
        with pytest.raises(ValueError):
            bm.set_decimal(-1)
        with pytest.raises(ValueError):
            bm.set_decimal(8) # Greater than or equal to 2**3

    def test_to_binary(self):
        bm = BitMask(6, 45)
        assert bm.to_binary() == "0b101101"

    def test_to_hexadecimal(self):
        bm = BitMask(8, 170)
        assert bm.to_hexadecimal() == "0xaa"

    def test_to_decimal(self):
        bm = BitMask(5, 27)
        assert bm.to_decimal() == 27

    def test_str(self):
        bm = BitMask(4, 5) # 0101
        assert str(bm) == "1 0 1 0"
        bm2 = BitMask(7, 42) # 0101010
        assert str(bm2) == "0 1 0 1 0 1 0"

    def test_getitem_index(self):
        bm = BitMask(5, 13) # 01101
        assert bm[0] == 1
        assert bm[1] == 0
        assert bm[4] == 0
        assert bm[-1] == 0 # Last bit
        assert bm[-5] == 1 # First bit

    def test_getitem_index_errors(self):
        bm = BitMask(3)
        with pytest.raises(IndexError):
            _ = bm[3]
        with pytest.raises(IndexError):
            _ = bm[-4]
        with pytest.raises(TypeError):
            _ = bm[1.5]

    def test_getitem_slice(self):
        bm = BitMask(8, 170) # 10101010
        assert bm[0:3].value == 5 # 0101 -> 101 (reversed due to storage)
        assert bm[2:6].value == 10 # 0101 -> 0101 -> 1010 (reversed)
        assert bm[:4].value == 10 # 0101 -> 0101 -> 1010
        assert bm[4:].value == 5 # 1010 -> 0101
        assert bm[::-1].value == 85 # 01010101

    def test_setitem_index(self):
        bm = BitMask(6)
        bm[0] = 1
        assert bm.value == 1
        bm[3] = 1
        assert bm.value == 9
        bm[0] = 0
        assert bm.value == 8
        bm[-1] = 1
        assert bm.value == 24 # 011000

    def test_setitem_index_errors(self):
        bm = BitMask(3)
        with pytest.raises(TypeError):
            bm[1.5] = 1
        with pytest.raises(IndexError):
            bm[3] = 1
        with pytest.raises(IndexError):
            bm[-4] = 1
        with pytest.raises(ValueError):
            bm[1] = 2
        with pytest.raises(TypeError):
            bm[:] = 1 # Slicing assignment not supported

    def test_len(self):
        bm = BitMask(12)
        assert len(bm) == 12

    def test_equality(self):
        bm1 = BitMask(5, 7)
        bm2 = BitMask(5, 7)
        bm3 = BitMask(5, 10)
        bm4 = BitMask(6, 7)
        assert bm1 == bm2
        assert bm1 != bm3
        assert bm1 != 7
        assert bm1 == 7 # Comparing with int value
        assert bm1 != bm4
        assert bm1 != "7"
        assert bm1.__eq__("7") is NotImplemented

    def test_inequality(self):
        bm1 = BitMask(4, 3)
        bm2 = BitMask(4, 5)
        assert bm1 < bm2
        assert bm1 <= bm2
        assert bm2 > bm1
        assert bm2 >= bm1
        assert bm1 < 5
        assert bm1 <= 3
        assert bm2 > 2
        assert bm2 >= 5
        with pytest.raises(TypeError):
            _ = bm1 < BitMask(5, 3)

    def test_iteration(self):
        bm = BitMask(5, 13) # 01101
        bits = [bit for bit in bm]
        assert bits == [1, 0, 1, 1, 0]

    def test_invert(self):
        bm = BitMask(4, 5) # 0101
        inverted_bm = ~bm
        assert inverted_bm.value == 10 # 1010
        assert inverted_bm.max_length == 4 # Inversion should return a new BitMask

    def test_hash(self):
        bm = BitMask(3, 5)
        assert hash(bm) is None # __hash__ returns None