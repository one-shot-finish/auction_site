import os
from auction_site.task import WinnerTask


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_site.settings')
    task = WinnerTask()
    task.go()

if __name__ == '__main__':
    main()