from codecs import encode

ori_lines = [
    "----------",
    "There is something in this world",
    "that no one has ever seen before.",
    "It is gentle and sweet.",
    "Maybe if it could be seen,",
    "everyone would fight over it.",
    "That is why the world hid it,",
    "so that no one could get their hands",
    "on it so easily.",
    "However, someday, someone will find it.",
    "The person who deserves it the most",
    "will definitely find it.",
    "----------",
    "Do you like this school?",
    "I really, really love it.",
    "But nothing can stay unchanged.",
    "Fun things... Happy things...",
    "They can't all possibly stay unchanged.",
    "Even so,",
    "can you go on loving this place?",
    "----------",
    "Sometimes I wonder,",
    "what if this town was alive?",
    "What if it had thoughts and feelings",
    "like one of us?",
    "If it did,",
    "I think it would want to make the people",
    "who live here happy.",
    "----------",
    "Expectations are what you have",
    "when you have given up.",
    "Expectations are born from",
    "a despairingly large difference in skill.",
    "----------",
    "A joke only lasts for a moment,",
    "if it leaves a misunderstanding,",
    "it becomes a lie.",
    "----------",
    "If someone didn't have any pride,",
    "wouldn't they also be lacking",
    "in self-confidence?",
    "If someone was free of greed,",
    "wouldn't they have trouble",
    "supporting their family?",
    "And if people didn't envy one another,",
    "wouldn't they stop inventing new things?",
    "----------",
    "If I don't have to do it, I won't.",
    "If I have to do it, I'll make it.",
    "----------",
    "A dream... I'm inside a dream.",
    "I can hear things...",
    "from far away and from close by...",
    "They echo like waves by the shore.",
    "Adults walk busily...",
    "without noticing the small form",
    "sitting on the bench.",
    "----------",
    "I was able to forget the pain",
    "and loneliness in my heart.",
    "Everything was just so much fun.",
    "If only every day could be like this forever.",
    "That became my only wish.",
    "----------",
    "If you turn your eyes away from sad things,",
    "they'll happen again one day.",
    "If you keep running away,",
    "you'll keep repeating the same mistakes.",
    "That's why you have to",
    "face the truth straight on.",
    "----------",
    "If you're happy, then I'm happy.",
    "When you make someone happy,",
    "you make yourself a little happier too.",
    "And that repeats over and over,",
    "making a happiness spiral.",
    "----------",
    "What do you think about the planetarium?",
    "That beautiful twinkling of eternity",
    "that will never fade, no matter when.",
    "All the stars in the sky are waiting for you.",
    "----------",
    "Everything you say and do...",
    "it all sparkles so brightly.",
    "It's too blinding for me,",
    "and I end up closing my eyes.",
    "But I can't help aspiring",
    "to be like you.",
    "----------",
    "/* Here is the end of my poem.",
    "Have you ever found my FLAG? :) */",
]
flag = b"flag{STeg_w1tH_uUeNc0DE_I5_50_fun}"


def line_padding_bits_cnt(length):
    """
    calculate how many characters are in the last grouping.
    if 1 or 2 characters are left, we can put 4 extra bits. (Not 8n bits, n = 1, 2)
    else put nothing.
    """
    left = length * 4 % 3
    if left == 1 or left == 2:
            return 4
    else:
            return 0


def poem_padding_bits_cnt(l):
    return sum(map(lambda x: line_padding_bits_cnt(len(x)), l))


def take_next_flag_chr(part_flag_taken):
    if part_flag_taken % 2 == 0:
        return (flag[part_flag_taken // 2] & 0b11110000) >> 4
    else:
        return flag[part_flag_taken // 2] & 0b00001111


def insert_flag(encoded):
    ret = list(map(lambda x: bytearray(x), encoded))
    part_flag_taken = 0  # a part is 4 bits
    for i, j in enumerate(ret):
        line_len = j[0] - 32
        left = line_len * 4 % 3
        if left == 0:
            continue
        elif left == 1:
            assert (j[-1] - 32 == 0) and (j[-2] - 32 == 0) and ((j[-3] - 32)| 0b110000 == 0b110000)
            j[-3] = ((j[-3] - 32) | take_next_flag_chr(part_flag_taken)) + 32
            part_flag_taken += 1
        elif left == 2:
            assert (j[-1] - 32 == 0) and ((j[-2] - 32) | 0b111100 == 0b111100)
            part_bits = take_next_flag_chr(part_flag_taken)
            j[-2] = ((j[-2] - 32) | (part_bits & 0b1100) >> 2) + 32
            j[-1] = ((j[-1] - 32) | part_bits & 0b0011) + 32
            part_flag_taken += 1
    assert(part_flag_taken == len(flag) * 2)
    return ret


if __name__ == "__main__":
    print(poem_padding_bits_cnt(ori_lines))
    # print(ascii(ori_lines))

    for i, j in enumerate(ori_lines):
        if len(j) > 45:  # "M"
            print("line {}: {} is too long.".format(i, j))
            raise ValueError

    if poem_padding_bits_cnt(ori_lines) != len(flag) * 8:
        print("requires {} bits.".format(len(flag) * 8))
        raise ValueError

    encoded_lines = list(map(lambda x: encode(x.encode("ascii"), "uu").splitlines()[1], ori_lines))

    print(encoded_lines)
    output = insert_flag(encoded_lines)
    print(output)

    f = open("poem.txt", "w")
    for i in output:
        f.write(i.decode("ascii") + "\n")
