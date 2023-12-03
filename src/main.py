from pkg.parser import Parser


def main():
    subtitle = Parser("data/test.srt").parse()

    print(">>>DBGUR: IN MAIN")
    for i in range(len(subtitle)):
        print(subtitle[i].offset)
        print(subtitle[i].start_timestamp)
        print(subtitle[i].end_timestamp)
        print(subtitle[i].dialogue)


if __name__ == "__main__":
    main()
