"""Description. 1"""
import argparse
import note_book_tkinter
import constants


def read_command_args() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        type=str,
        dest='config_file',
    )
    return parser


if __name__ == '__main__':

    parsed_args = read_command_args().parse_args()

    if parsed_args.config_file:
        config_file = parsed_args.config_file
    else:
        config_file = constants.DEFAULT_CONFIG_FILE_NAME

    note_book_tkinter.VisualNoteBook(last_config=config_file)
