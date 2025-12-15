import load_data
def main():
    loader = load_data.load_data()
    loader.load()
    currencies = loader.parse()
    print(currencies)
    print(loader.fetched)


if __name__ == "__main__":
    main()