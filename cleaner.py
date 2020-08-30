import os
import sys
import shutil
import shlex
import psutil
import subprocess


UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]


def main(PATHS, UNITS_MAPPING):

    size, amount = None, None
    print('Do you want to create a log file? (y / n)')

    while True:
        answer = input()
        if answer == 'y':
            size, amount = run_clean(PATHS, log=True)
            break
        elif answer == 'n':
            size, amount = run_clean(PATHS)
            break
        else:
            print("The answer should be 'y' or 'n'. Try it again.")

    print('Cleaning is finished!')
    print(f'Total files and dirs -- {amount}')
    print(f'Total size -- {size}')


def run_clean(PATHS, log=False):

    total_size, total_amount = 0, 0

    if not check_running_browsers():
        sys.exit('Browser needs to be closed for finish the process')

    with open(r'C:\Users\kayot\Desktop\cleaner_log', 'w') as log:
        for browser in PATHS['Browsers'].keys():
            for dir_name, dir_path in PATHS['Browsers'][browser].items():
                if dir_name == 'Cookies':
                    try:
                        size = os.path.getsize(dir_path)
                        os.remove(dir_path)
                        total_amount += 1
                        total_size += size
                        if log:
                            log.write(dir_path + '\n')
                    except FileNotFoundError:
                        continue
                else:
                    for file in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file)
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            try:
                                os.remove(file_path)
                                total_amount += 1
                                total_size += size
                                if log:
                                    log.write(file_path + '\n')
                            except PermissionError:
                                print(f'Acces is denied. {file} was not deleted.')

                        elif os.path.isdir(file_path):
                            size = os.path.getsize(file_path)
                            try:
                                shutil.rmtree(file_path, ignore_errors=True)
                                total_amount += 1
                                total_size += size
                                if log:
                                    log.write(file_path + '\n')
                            except PermissionError:
                                print(f'Acces is denied. {file} was not deleted.')

    with open(r'C:\Users\kayot\Desktop\cleaner_log', 'a') as log:
        for dir_path in (PATHS['Temp'], PATHS['UserTemp']):
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    try:
                        os.remove(file_path)
                        total_amount += 1
                        total_size += size
                        if log:
                            log.write(file_path + '\n')
                    except PermissionError:
                        print(f'Acces is denied. {file} was not deleted.')

                elif os.path.isdir(file_path):
                    size = os.path.getsize(file_path)
                    try:
                        shutil.rmtree(file_path)
                        total_amount += 1
                        total_size += size
                        if log:
                            log.write(file_path + '\n')
                    except PermissionError:
                        print(f'Acces is denied. {file} was not deleted.')

    return (pretty_size(total_size), total_amount)


def pretty_size(bytes, units=UNITS_MAPPING):

    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple

    return str(amount) + suffix


def check_running_browsers():

    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in ['chrome.exe', 'browser.exe', 'msedge.exe', 'opera.exe', 'iexplore.exe']:
            name = proc.info['name'][:-4].capitalize()
            task_name = proc.info['name']
            print(f'{name} needs to be closed to clean the Internet Cache')
            print(f'Do you want to close {name}? (y / n)')
            while True:
                answer = input()
                if answer == 'y':
                    args = shlex.split(f'taskkill /IM "{task_name}" /F')
                    subprocess.Popen(args)
                    return True
                elif answer == 'n':
                    return False
                else:
                    print('The answer should be "y" or "n". Try it again.')

    return True


PATHS = {
    'Temp': 'C:\\Windows\\Temp',
    'UserTemp': 'C:\\Users\\kayot\\AppData\\Local\\Temp',
    'Browsers': {
        'Chrome': {'Cookies': 'C:\\Users\\kayot\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies',
                   'Cache': 'C:\\Users\\kayot\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache',
                   'ShaderCache': 'C:\\Users\\kayot\\AppData\\Local\\Google\\Chrome\\User Data\\ShaderCache\\GPUCache',
                   'GrShaderCache': 'C:\\Users\\kayot\\AppData\\Local\\Google\\Chrome\\User Data\\GrShaderCache\\GPUCache'},
        'Yandex': {'Cookies': 'C:\\Users\\kayot\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies',
                   'ShaderCache': 'C:\\Users\\kayot\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\ShaderCache\\GPUCache',
                   'CacheStorage': 'C:\\Users\\kayot\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Service Worker\\CacheStorage',
                   'Cache': 'C:\\Users\\kayot\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cache',
                   'GPUCache': 'C:\\Users\\kayot\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\GPUCache'},
        'EdgChr': {'Cookies': 'C:\\Users\\kayot\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies',
                   'Cache': 'C:\\Users\\kayot\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache',
                   'GPUCache': 'C:\\Users\\kayot\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\GPUCache',
                   'ShaderCache': 'C:\\Users\\kayot\\AppData\\Local\\Microsoft\\Edge\\User Data\\ShaderCache\\GPUCache'},
    }
}


if __name__ == '__main__':
    main(PATHS, UNITS_MAPPING)
