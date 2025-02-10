class BitMask:
    def __init__(self, length: int, num: int = 0):
        """
        Initialize a BitMask with a specified length and an optional initial integer value.

        :param int length: The maximum number of bits the BitMask can hold.
        :param int num: An integer value to initialize the BitMask. Defaults to 0.
        """
        self.__max_length = length

        if num >= (1 << self.__max_length):
            raise ValueError(f"Value {num} must be less than {1 << self.__max_length}")

        self.value = num

    @property
    def max_length(self) -> int:
        return self.__max_length

    def set_bit(self, pos: int) -> None:
        """
        Set the bit at the specified position to 1.

        :param int pos: The position of the bit to set (0-indexed).
        """
        if not isinstance(pos, int):
            raise TypeError(f"Expected type int, got type {type(pos)}")

        if pos >= self.__max_length:
            raise IndexError(f"Index {pos} is out of range")

        self.value |= 1 << pos

    def set_all(self) -> None:
        """Set all bits in the BitMask to 1."""
        self.value |= (1 << self.__max_length) - 1

    def flip_bit(self, pos: int) -> None:
        """
        Flip the bit at the specified position.

        :param int pos: The position of the bit to flip (0-indexed).
        """
        if not isinstance(pos, int):
            raise TypeError(f"Expected type int, got type {type(pos)}")

        if pos >= self.__max_length:
            raise IndexError(f"Index {pos} is out of range")

        self.value ^= 1 << pos

    def flip_all(self) -> None:
        """Flip all bits in the BitMask."""
        self.value ^= (1 << self.__max_length) - 1

    def reset_bit(self, pos: int) -> None:
        """
        Reset the bit at the specified position to 0.

        :param int pos: The position of the bit to reset (0-indexed).
        """
        if not isinstance(pos, int):
            raise TypeError(f"Expected type int, got type {type(pos)}")

        if pos >= self.__max_length:
            raise IndexError(f"Index {pos} is out of range")

        self.value &= ~(1 << pos)

    def reset_all(self) -> None:
        """Reset all bits in the BitMask to 0."""
        self.value = 0

    def reverse_bits(self) -> None:
        """Reverses the bit order of the BitMask"""
        self.set_binary(self.__str__() [::-1])

    def get_bit(self, pos: int) -> int:
        """
        Get the value of the bit at the specified position.

        :param int pos: The position of the bit to retrieve (0-indexed).
        :return int: The value of the bit (0 or 1).
        """
        if not isinstance(pos, int):
            raise TypeError(f"Expected type int, got type {type(pos)}")

        if pos >= self.__max_length:
            raise IndexError(f"Index {pos} is out of range")

        return (self.value >> pos) & 1

    def get_count(self) -> int:
        """
        Count the number of set bits (1s) in the BitMask.

        :return int: The count of set bits.
        """
        temp = self.value
        count = 0
        while temp:
            temp &= temp - 1
            count += 1

        return count

    def get_non_zero(self) -> tuple [int, ...]:
        """
        Get the indices of all set bits (1s).

        :return int: A list of indices where bits are set to 1.
        """
        return tuple(index for index in range(self.__max_length) if (self.value >> index) & 1)

    def get_zero(self) -> tuple [int, ...]:
        """
        Get the indices of all unset bits (0s).

        :return int: A list of indices where bits are set to 0.
        """
        return tuple(index for index in range(self.__max_length) if not (self.value >> index) & 1)

    def get_lsb(self) -> int:
        """
        Get the index of the least significant set bit (LSB).

        :return int: The index of the least significant bit that is set to 1, or -1 if no bits are set.
        """
        return (self.value & -self.value).bit_length() - 1

    def set_binary(self, num: str) -> None:
        """
        Set the BitMask value using a binary string.

        :param str num: A binary string representation of the value.
        """
        if not isinstance(num, str):
            raise TypeError(f"Expected type str, got type {type(num)}")

        try:
            value = int(num, 2)
            if value >= (1 << self.__max_length):
                raise ValueError(f"Value {bin(value)} must be less than {bin(1 << self.__max_length)}")
            elif value < 0:
                raise ValueError(f"Value {num} must be positive")
            else:
                self.value = value
        except ValueError:
            raise ValueError(f"{num} is not a valid binary string")
        except Exception:
            raise Exception

    def set_hexadecimal(self, num: str):
        """
        Set the BitMask value using a hexadecimal string.

        :param str num: A hexadecimal string representation of the value.
        """
        if not isinstance(num, str):
            raise TypeError(f"Expected type str, got type {type(num)}")

        try:
            value = int(num, 16)
            if value >= (1 << self.__max_length):
                raise ValueError(f"Value {hex(value)} must be less than {hex(1 << self.__max_length)}")
            elif value < 0:
                raise ValueError(f"Value {num} must be positive")
            else:
                self.value = value
        except ValueError:
            raise ValueError(f"{num} is not a valid hexadecimal string")
        except Exception:
            raise Exception

    def set_decimal(self, num: int) -> None:
        """
        Set the BitMask value using an integer.

        :param int num: The value to set.
        """
        if not isinstance(num, int):
            raise TypeError(f"Expected type int, got type {type(num)}")

        if num >= (1 << self.__max_length):
            raise ValueError(f"Value {num} must be less than {1 << self.__max_length}")
        elif num < 0:
            raise ValueError(f"Value {num} must be positive")

        self.value = num

    def __str__(self) -> str:
        return bin(self.value).replace("0b", "").zfill(self.__max_length)

    def to_binary(self) -> str:
        """Return a binary string representation of the BitMask."""
        return bin(self.value)

    def to_hexadecimal(self) -> str:
        """Return a hexadecimal string representation of the BitMask."""
        return hex(self.value)

    def to_decimal(self) -> int:
        """Return the decimal value of the BitMask."""
        return self.value

    def __getitem__(self, item):
        if isinstance(item, slice):
            start, stop, step = item.indices(self.__max_length)
            sliced = 0
            length = abs(start - stop)

            for i, pos in enumerate(range(start, stop, step)):
                sliced |= ((self.value >> pos) & 1) << (length - i - 1)

            return BitMask(length, sliced)

        if not isinstance(item, int):
            raise TypeError(f"'BitMask' indices must be integers ot slices, not {type(item)}")

        if item < 0:
            if abs(item) > self.__max_length:
                raise IndexError(f"Index {item} is out of range")
            else:
                item += self.__max_length

        return self.get_bit(item)

    def __setitem__(self, key: int, value: int) -> None:
        if not isinstance(key, int):
            if isinstance(key, slice):
                raise TypeError(f"'BitMask' object does not support slicing assignments")
            else:
                raise TypeError(f"'BitMask' indices must be integers, not {type(key)}")

        if key < 0:
            if abs(key) > self.__max_length:
                raise IndexError(f"Index {key} is out of range")
            else:
                key += self.__max_length

        if key >= self.__max_length:
            raise IndexError(f"Index {key} is out of range")

        if value not in [0, 1]:
            raise ValueError(f"Cannot assign {value} to position {key} because '{value}' is not 0 or 1")
        if value:
            self.set_bit(key)
        else:
            self.reset_bit(key)

    def __len__(self):
        return self.__max_length
