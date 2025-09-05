import os
import string
import random
import hashlib
import platform
import sys
"""
The tool is based on other creator from internet.

Change Log
2025/09/05
1. modify the original code , change the tk mode to cli mode.
2. add new function to enum the correct versionMagic in the new version 11.x.x and later.
"""

py_version = platform.python_version()
if py_version[0] != '3':
    print("Can't run under python2 env ! please run tool under python 3.2 or later version !")
    os.system("pause")
    os._exit(0)
#
BASE16 = '0123456789ABCDEF'
BASE30 = '123456789ABCDEFGHJKLMNPQRTVWXY'


def RandomString(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join((random.choice(chars) for _ in range(size)))


def BaseConvert(number, fromdigits, todigits, ignore_negative=True):
    if not ignore_negative and str(number)[0] == '-':
        number = str(number)[1:]
        neg = 1
    else:
        neg = 0
    x = 0
    for digit in str(number):
        x = x * len(fromdigits) + fromdigits.index(digit)

    res = ''
    while x > 0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x //= len(todigits)

    if neg:
        res = '-' + res
    return res


def AddHyphens(code):
    return code[:5] + '-' + code[5:10] + '-' + code[10:15] + '-' + code[15:]


def SHAToBase30(digest):
    tdigest = ''.join([c for i, c in enumerate(digest) if i // 2 * 2 == i])
    result = BaseConvert(tdigest, BASE16, BASE30)
    while len(result) < 17:
        result = '1' + result
    return result


def loop(ecx, lichash):
    part = 0
    for c in lichash:
        part = ecx * part + ord(c) & 1048575
    return part

g_version_list = ('11.x.x','10.x.x','9.x.x','8.x.x', '7.x.x', '6.x.x', '5.x.x')
g_version_magics = {
    '5.x.x': [7, 123, 23, 87],
    '6.x.x': [23, 161, 47, 9],
    '7.x.x': [221, 13, 93, 27],
    '8.x.x': [179, 95, 45, 245],
    '9.x.x': [123, 17, 42, 7],
    '10.x.x': [102, 99, 107, 117],
    '11.x.x': [6, 24, 15, 22]
}

   
# 
def genALK(**argv):
    #
    
    # # Generate License ID
    licenseID = AddHyphens('CN' + RandomString(18, '123456789ABCDEFGHJKLMNPQRTVWXY'))
    print('License id: ' + licenseID)

    requestCode = input('Enter request code:')
    if requestCode.strip() == '':
        print("Hints", "Please input the Request Code !")
        return
    # # SHA1
    shaHasher = hashlib.sha1()
    shaHasher.update(requestCode.encode('utf-8'))
    shaHasher.update(licenseID.encode('utf-8'))
    hashResult = shaHasher.hexdigest().upper()
    lichash = AddHyphens(requestCode[:3] + SHAToBase30(hashResult))

    versionMagic = None
    print('Support Version:')
    for k, v in enumerate(g_version_list) :
        print('{0} : {1}'.format(k, v))
        pass
    wingIDEProVerStr= input('Enter version code:')
    print('Cracking WingIDE Version : ' + wingIDEProVerStr)
    vv = -1
    try:
        vv = int(wingIDEProVerStr)
        pass
    except:
        vv = -1
        pass
        
    if vv >= 0:
        versionMagic = g_version_magics[g_version_list[vv]]
        pass

    if versionMagic:
        activationCode = format(loop(versionMagic[0], lichash), '05x') + \
            format(loop(versionMagic[1], lichash), '05x') + \
            format(loop(versionMagic[2], lichash), '05x') + \
            format(loop(versionMagic[3], lichash), '05x')
        #pass
    else:
        print('Get wrong WingIDE version, exit...')
        os._exit(0)
    activationCode = BaseConvert(activationCode.upper(), BASE16, BASE30)
    #
    while len(activationCode) < 17:
        activationCode = '1' + activationCode

    activationCode = AddHyphens('AXX' + activationCode)
    print('Activation code: ' + activationCode)
    pass

def enumVersionMagic(licenseCode, requestCode, activationCode):
    #licenseCode = licenseCode.replace('-', '')
    #requestCode = requestCode.replace('-', '')
    activationCode = activationCode.replace('-', '')
    # SHA1
    shaHasher = hashlib.sha1()
    shaHasher.update(requestCode.encode('utf-8'))
    shaHasher.update(licenseCode.encode('utf-8'))
    hashResult = shaHasher.hexdigest().upper()
    lichash = AddHyphens(requestCode[:3] + SHAToBase30(hashResult))
    
    aCode = activationCode[3:]
    if aCode[0] == '1' :
        aCode = aCode[1:]
        pass
    print('Try2 Match Code : ', aCode)
    #
    versionMagic = [1, 1, 1, 1]
    def enumVersionMagicValue(verMagic, list_index, match_start_str):
        testCode = ""
        matched_v = -1
        for v in range(1, 256):
            verMagic[list_index] = v
            testCode = format(loop(verMagic[0], lichash), '05x') + \
                format(loop(verMagic[1], lichash), '05x') + \
                format(loop(verMagic[2], lichash), '05x') + \
                format(loop(verMagic[3], lichash), '05x')
            testCode = BaseConvert(testCode.upper(), BASE16, BASE30)
            #print(verMagic, testCode)
            if testCode.startswith(match_start_str):
                matched_v = v
                print(verMagic, testCode)
                break
            else:
                pass
            pass
        if matched_v < 0:
            print("Can not match the versionMagic {0} ".format(list_index))
            sys.exit(1)
        else:
            print("Matched the versionMagic {0} : {1}".format(list_index, matched_v))
        return testCode
    for i in range(4):
        enumVersionMagicValue(versionMagic, i, aCode[:4*i+3])
    #
    print('Get the VersionMagic : ' + str(versionMagic))    
    pass


if __name__ == '__main__':
    def print_usage():
        print("Usage : {0} [action] [param]".format(sys.argv[0]))
        print("")
        print("action : g|gen|t|test")
        print("")
        
        print("g|gen  : generate the activation code, default action is gen" )
        print("{0} ".format(sys.argv[0]))
        print("{0} gen".format(sys.argv[0]))
        print("{0} g".format(sys.argv[0]))
        print("")
        print("t|test : test the new version magic , need licenseCode,requestCode and activationCode from another crask tool such as DVT or purchase method!")
        print("{0} t licenseCode requestCode  activationCode".format(sys.argv[0]))
        print("{0} test licenseCode requestCode  activationCode".format(sys.argv[0]))
        pass
        
    argc = len(sys.argv)
    if argc > 1:
        print(sys.argv)
        action = sys.argv[1]
        if action.lower() in ['g', 'gen']:
            print('Enter gen mode...')
            genALK()
            pass
        elif action.lower() in ['t', 'test']:
            print('Enter test mode...')
            if argc < 5:
                print_usage()
                sys.exit(1)
            licenseCode = sys.argv[2]
            requestCode = sys.argv[3]
            activationCode = sys.argv[4]
            print('License    Code : ', licenseCode)
            print('Request    Code : ', requestCode)
            print('Activation Code : ', activationCode)
            enumVersionMagic(licenseCode, requestCode, activationCode)
            pass
        else:
            print('Not support action !')
            print_usage()
            sys.exit(1)
        pass
    else:
        print('Enter gen mode...')
        genALK()
        pass
    print("==DONE==")
    pass