import pandas as pd
import click
import json
from pathlib import Path


@click.command()
@click.option('--anns', '-a', required=True, help='Annotations path')
@click.option('--csv', '-c', required=True, help='CSV file path')
@click.option('--overwrite', '-o', is_flag=True, help='If overwrite then work inplace, else create new')
@click.option('--index-column', default='name', help='(default: name)')
@click.option('--url-column', default='url', help='(default: url)')
def main(anns: str, csv: str, overwrite: bool, index_column: str, url_column: str):

    with open(anns, 'r') as f:
        dataset = json.load(f)

    urls = pd.read_csv(csv, index_col=index_column)

    for image in dataset['images']:
        file_name = Path(image['file_name']).stem
 
        try:
            image['flickr_url'] = urls.loc[file_name][url_column]
            print(image['id'])
        except:
            pass

    if overwrite:
        with open(anns, 'w') as f:
            json.dump(dataset, f)
    else:
        with open(anns.replace('.json', '_new.json'), 'w') as f:
            json.dump(dataset, f)

if __name__ == '__main__':
    main()