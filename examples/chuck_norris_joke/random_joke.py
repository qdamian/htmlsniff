import requests
from htmlvis import RequestsSniffer, save_seq_diag


def main():
    sniffer = RequestsSniffer('Sample client', 'I. Chuck Norris DB')
    response = requests.get(
        'http://api.icndb.com/jokes/random', hooks={'response': sniffer})
    diag = save_seq_diag('diagram.html', [sniffer])
    print(diag)


if __name__ == '__main__':
    main()
