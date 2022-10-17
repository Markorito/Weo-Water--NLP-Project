import argparse
import pandas as pd

try:
    import colorama
except ImportError:
    colorama = None

# Name of the column used for tagging
TAG_COLUMN = 'has_geolocation'

if __name__ == '__main__':
    if colorama:
        colorama.init()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Tag data in a CSV file.',
        epilog=f'''\
It is assumed that PATH is a CSV file containing the optional `title` and the
non-optional `body` columns. A new column `{TAG_COLUMN}` is created by the program
if necessary and populated with tags input by the user. The title and the
content of the article are displayed for this.

Rows that already have a tag are skipped. The program can be ended early with
`control-c`. In any case, the new tags will be added to the CSV file at PATH in
the `{TAG_COLUMN}` column.

Alternatively, if the --review flag is specified, rows without a tag in the
`{TAG_COLUMN}` column will be skipped. For all other rows, the title and
body are displayed with the existing tag, so that they can be reviewed. The
user can choose to leave the tag as it is by pressing enter, or replace it by
entering a new tag.

The --keywords flag can be used to specify keywords that will be highlighted in
the body. If the `colorama` library is installed for Python, colors will be
used.

EXAMPLE:

  python tagger.py final_twitter_dataset.csv --keywords flood drought Flood Drought
''')
    parser.add_argument('path', metavar='PATH',
        help='path to the CSV file where the tags should be added')
    parser.add_argument('-k', '--keywords', metavar='KEYWORD',
        nargs='+', required=False,
        help='keywords that should highlighted in the text')
    parser.add_argument('-r', '--review', action='store_true',
        help='review existing tags instead of adding missing ones')
    args = parser.parse_args()
    path = args.path

    # We assume that the first column is an index column.
    # This is what pandas does by default with `to_csv`.
    # Make sure that this is actually the case!
    d = pd.read_csv(path, index_col=0, dtype=str)
    d.index = d.index.astype(int)
    d['body'] = d['body'].astype('str')

    # If the TAG_COLUMN column is missing, add it.
    if not TAG_COLUMN in d:
        d[TAG_COLUMN] = None
    else:
        d[TAG_COLUMN] = d[TAG_COLUMN].dropna('')

    for i, row in d.iterrows():
        if args.review:
            # Skip rows that were not yet tagged.
            if pd.isna(row[TAG_COLUMN]):
                continue
        else:
            # Skip rows that were already tagged.
            if not pd.isna(row[TAG_COLUMN]):
                continue

        body = row['body']
        title = row['title']
        if pd.isna(title):
            title = ''

        if colorama is None:
            print('## Id {}: "{}"\n'.format(i, title))
        else:
            print('{}## Id {}: "{}"{}\n'.format(
                colorama.Fore.GREEN, i, title, colorama.Style.RESET_ALL))

        if not pd.isna(body) and args.keywords:
            # Highlight keywords in the body
            if colorama is None:
                highlight = lambda word: f'**{word}**'
            else:
                highlight = lambda word: f'{colorama.Fore.RED}{word}{colorama.Style.RESET_ALL}'
            for kw in args.keywords:
                body = body.replace(kw, highlight(kw))
        print(body)

        # The tagging process can be stopped with ctrl-c.
        try:
            if args.review:
                # Show the existing TAG_COLUMN and ask if it should be replaced.
                tag = row[TAG_COLUMN]
                if colorama is None:
                    print(f'>>> {TAG_COLUMN} = "{tag}". Replace?', end='')
                else:
                    print(f'{colorama.Fore.GREEN}>>> {TAG_COLUMN} = "{tag}". Replace?{colorama.Style.RESET_ALL} ', end='')
                # Only replace TAG_COLUMN if a new one is entered.
                new_tag = input()
                if new_tag:
                    d.at[i, TAG_COLUMN] = new_tag
            else:
                # Ask for TAG_COLUMN.
                if colorama is None:
                    print(f'>>> {TAG_COLUMN}? ', end='')
                else:
                    print(f'{colorama.Fore.GREEN}>>> {TAG_COLUMN}?{colorama.Style.RESET_ALL} ', end='')
                d.at[i, 'category'] = input()
        except KeyboardInterrupt:
            print()
            break
        # Print a separator, to make it easier to see where the new body starts.
        print()
        print('=' * 80)
        print()

    # Overwrite the CSV file. This should only add new data, and not lose anything,
    # because we made sure to only add tags that were missing before.
    print('Storing tags in "{}".'.format(path))
    d.to_csv(path)
