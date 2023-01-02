
from commands import commands
from collections import OrderedDict
import os


class Option:
    def __init__(self, name, command, prep_call=None) -> None:
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def _handle_message(self, message):
        if isinstance(message, list):
            print_bookmarks(message)
        else:
            print(message)

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(
            data) if data else self.command.execute()
        self._handle_message(message)


def print_bookmarks(message: list):
    print(' '.join(map(str, message)))


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option.name}')
        print()


def options_choice_is_valid(choice: str, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('操作を選択してください: ')
    while not options_choice_is_valid(choice=choice, options=options):
        print('A,B,T,D,Qのいずれかを入力してください(小文字でもOK ただし半角文字)')
        choice = input('操作を選択してください: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return{
        'title': get_user_input('タイトル'),
        'url': get_user_input('URL'),
        'memo': get_user_input('メモ', required=False)
    }


def get_bookmark_id_for_deletion():
    return get_user_input('削除するブックマークのIDを指定')


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)
    return


def loop():
    clear_screen()
    print_options(options=options)
    chosen_option = get_option_choice(options)
    chosen_option.choose()
    _ = input('Enterキーを押すとメニューに戻ります!')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()
    options = OrderedDict({
        'A': Option(name='追加', command=commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option(name='登録順にリスト', command=commands.ListBookmarksCommand()),
        'T': Option(name='タイトル順にリスト', command=commands.ListBookmarksCommand(order_by='title')),
        'D': Option(name='削除', command=commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
        'Q': Option(name='終了', command=commands.QuiteCommand())
    })
    while True:
        loop()
