from parser import Parser

def main():
    filename = input('Название файла: ')
    url = input('URL: ')
    Parser(url, filename).parse()


if __name__ == '__main__':
    main()
