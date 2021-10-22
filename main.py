import requests

if __name__ == '__main__':
    print('-----start-----')

    url = 'https://api.pwnedpasswords.com/range/' + 'password123'
    res = requests.get(url)
    print(res)

