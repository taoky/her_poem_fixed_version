from generate import get_encoded_line_left


def get_hidden_bits(line):
    left = get_encoded_line_left(line)
    assert(left != 0)
    if left == 1:
        return (line[-3] - 32) & 0b1111
    else:
        return (((line[-2] - 32) & 0b11) << 2) | (((line[-1] - 32) & 0b1100) >> 2)


def find_hidden_flag(lines):
    lines_contain_flag = []
    flag = ""
    for i in lines:
        left = get_encoded_line_left(i)
        if left == 0:
            continue
        else:
            lines_contain_flag.append(i)
    assert (len(lines_contain_flag) % 2 == 0)
    for i in range(len(lines_contain_flag)):
        if i % 2 == 0:
            print(i)
            print(bin(get_hidden_bits(lines_contain_flag[i]) << 4))
            print(bin(get_hidden_bits(lines_contain_flag[i + 1])))
            flag_chr = (get_hidden_bits(lines_contain_flag[i]) << 4) | (get_hidden_bits(lines_contain_flag[i + 1]))
            print(flag_chr)
            assert(flag_chr <= 0b01111111)
            flag += chr(flag_chr)
    print(flag)


if __name__ == '__main__':
    f = open("poem.txt", "r")
    enc_lines = f.read().splitlines()
    enc_lines = list(map(lambda x: bytes(x, encoding="ascii"), enc_lines))
    find_hidden_flag(enc_lines)