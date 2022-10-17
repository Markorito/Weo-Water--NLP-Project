import argparse
import pandas as pd
try:
    import colorama
except ImportError:
    colorama = None

if __name__ == '__main__':
    if colorama:
        colorama.init()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Tag data in a CSV file.',
        epilog='''\
It is assumed that PATH is a CSV file containing the `article_title` and
`article_content` columns. A new column `category` is created by the program if
necessary and populated with tags input by the user. The title and the content
of the article are displayed for this.

Rows that already have a tag are skipped. The program can be ended early with
`control-c`. In any case, the new tags will be added to the CSV file at PATH in
the `category` column.

Alternatively, if the --review flag is specified, rows without a tag in the
`category` column will be skipped. For all other rows, the article's title and
content are displayed with the existing tag, so that they can be reviewed. The
user can choose to leave the tag as it is by pressing enter, or replace it by
entering a new tag.

The --keywords flag can be used to specify keywords that will be highlighted in
the article content. If the `colorama` library is installed for Python, colors
will be used.

EXAMPLE:

  python tagger.py FL-2021-000038-KEN.csv --keywords flood drought Flood Drought
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

    # If the 'category' column is missing, add it.
    if not 'category' in d:
        d['category'] = None
    else:
        d['category'] = d['category'].dropna('')

    for i, row in d.iterrows():
        if args.review:
            # Skip rows that were not yet tagged.
            if pd.isna(row['category']):
                continue
        else:
            # Skip rows that were already tagged.
            if not pd.isna(row['category']):
                continue

        article = row['article_content']
        title = row['article_title']

        if colorama is None:
            print('## Article {}: "{}"\n'.format(i, title))
        else:
            print('{}## Article {}: "{}"{}\n'.format(
                colorama.Fore.GREEN, i, title, colorama.Style.RESET_ALL))

        if not pd.isna(article) and args.keywords:
            # Highlight keywords in the article
            if colorama is None:
                highlight = lambda word: f'**{word}**'
            else:
                highlight = lambda word: f'{colorama.Fore.RED}{word}{colorama.Style.RESET_ALL}'
            for kw in args.keywords:
                article = article.replace(kw, highlight(kw))
        print(article)

        # The tagging process can be stopped with ctrl-c.
        try:
            if args.review:
                # Show the existing category and ask if it should be replaced.
                category = row['category']
                if colorama is None:
                    print(f'>>> category = "{category}". Replace?', end='')
                else:
                    print(f'{colorama.Fore.GREEN}>>> category = "{category}". Replace?{colorama.Style.RESET_ALL} ', end='')
                # Only replace category if a new one is entered.
                new_category = input()
                if new_category:
                    d.at[i, 'category'] = new_category
            else:
                # Ask for category.
                if colorama is None:
                    print('>>> category? ', end='')
                else:
                    print(f'{colorama.Fore.GREEN}>>> category?{colorama.Style.RESET_ALL} ', end='')
                d.at[i, 'category'] = input()
        except KeyboardInterrupt:
            print()
            break
        # Print a separator, to make it easier to see where the new article starts.
        print()
        print('=' * 80)
        print()

    # Overwrite the CSV file. This should only add new data, and not lose anything,
    # because we made sure to only add tags that were missing before.
    print('Storing tags in "{}".'.format(path))
    d.to_csv(path)
