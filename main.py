import requests
import hashlib
import sys

# 將hash過後的密碼前5碼傳到api 並回傳response
def request_api_data(query_char):
    # just pass first 5 letter after SHA-1 hashing to check if password is safe
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    # 回傳200表示api正常運作
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

# 讀response
def read_res(response):
    print(response.text)

# 讀取response中hash跟有問題的次數
def get_password_leaks_count(hashes, hash_to_check):
    # 把hash拆成h跟count
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# check password if it exists in API response
def pwned_api_check(password):
    # 加密
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    #前5碼跟後面的
    first5_char, tail = sha1password[:5], sha1password[5:]
    # 取得response
    response = request_api_data(first5_char)
    # print(response)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'password {password} was found {count} times')
        else:
            print(f'{password} was not found.')
    return 'done!'

if __name__ == '__main__':
    print('-----start-----')

    # sys.exit(main(sys.argc[1:]))
    main(['123'])

