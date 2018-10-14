def find_hidden_flag(lines):
    for i in lines:
        print(i[0])
        line_len = i[0] - 32
        padding = line_len * 4 % 3


if __name__ == '__main__':
    f = open("poem.txt", "r")
    enc_lines = f.read().splitlines()
    find_hidden_flag(enc_lines)