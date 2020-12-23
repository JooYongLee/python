import uuid

# 0XFF_FF_
_16bytes = (1 << 64 ) - 1
def split_uid_bits(uid_value:int):
    lsb = uid_value & _16bytes
    msb = uid_value >> 64
    return msb, lsb

def merge_uid_bits(msb, lsb):
    msb_shift = msb << 64
    concat_bit = msb_shift | lsb
    return concat_bit

for _ in range(10):
    x = uuid.uuid4()
    value = x.int
    # a = value >> 16
    # x2 = value & _16bytes
    # x1 = value >> 64
    msb, lsb = split_uid_bits(value)
    r = merge_uid_bits(msb, lsb)
    # print(x1, x2)
    # r1 = x1 << 64
    # r = r1 | x2
    print(r)
    print(value)
    print(r==value)


a = 0
