import load_data
import converter
def main():
    loader = load_data.load_data()
    loader.load()
    currencies = loader.parse()
    print(currencies)
    print(loader.fetched)
    conv = converter.converter()
    conv.currencies = currencies
    print(conv.convert(10, "USD", "RON"))
    print(conv.convert(-10, "RON", "USD"))
    print(conv.convert(0, "RON", "USD"))
    print(conv.convert(10, "BJG", "RON"))



if __name__ == "__main__":
    main()