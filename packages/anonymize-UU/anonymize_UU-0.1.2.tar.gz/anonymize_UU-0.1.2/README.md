# Anonymize UU

This description can be found [on GitHub here](https://github.com/cskaandorp/anonymize)

Anonymize_UU facilitates the replacement of keywords or regex-patterns within a file tree or zipped archive. It recursively traverses the tree, opens supported files and substitutes any found pattern or keyword with a replacement. Besides contents, anomize_UU will substitue keywords/patterns in file/folder-paths as well.

The result will be either a copied or replaced version of the original file-tree with all substitutions made.

As of now, Anonymize_UU supports text-based files, like .txt, .html, .json and .csv. UTF-8 encoding is assumed. Besides text files, Anonymize_UU is also able to handle (nested) zip archives. These archives will be unpacked in a temp folder, processed and zipped again.

## Installation

`$ pip install anonymize_UU`

## Usage

Import the Anomymize class in your code and create an anonymization object like this:

```
from anonymize import Anonymize

# refer to csv files in which keywords and substitutions are paired
anonymize_csv = Anonymize('/Users/casper/Desktop/keys.csv')

# using a dictionary instead of a csv file:
my_dict = {
    'A1234': 'aaaa',
    'B9876': 'bbbb',
}
anonymize_dict = Anonymize(my_dict)

# specifying a zip-format to zip unpacked archives after processing (.zip is default)
anonymize_zip = Anonymize('/Users/casper/Desktop/keys.csv', zip_format='gztar')
```

When using a csv-file, anonymize_UU will assume your file contains two columns: the left column contains the keywords which need to be replaced, the right column contains their substitutions. **Column headers are mandatory**, but don't have to follow a specific format.

When using a dictionary, the keys will be replaced by their values.

Performance might be enhanced when your keywords can be generalized into regular expressions. Anynomize_UU will search these patterns and replace them instead of matching the entire dictionary/csv-file against file contents or file/folder-paths. Example:

```
anonymize_regex = Anonymize(my_dict, pattern=r'[A-B]\d{4}')
```

### Copy vs. replacing

Anonymize_UU is able to create a copy of the processed file-tree or replace it. The `substitute` method takes a mandatory source-path argument (path to a file, folder or zip-archive, either a string or a [Path](https://docs.python.org/3/library/pathlib.html#basic-use) object) and an optional target-path argument (again, a string or [Path](https://docs.python.org/3/library/pathlib.html#basic-use) object). The target **needs to refer to a folder**. The target-folder will be created if it doesn't exist.

When the target argument is provided, anonymize_UU will create a processed copy of the source into the target-folder. When the target argument is omitted, the source will be overwritten by a processed version of it:

```
# process the datadownload.zip file, replace all patterns and write
# a copy to the 'bucket' folder.
anonymize_regex.substitute(
    '/Users/casper/Desktop/datadownload.zip', 
    '/Users/casper/Desktop/bucket'
)

# process the 'download' folder and replace the original by its processed 
# version
anonymize_regex.substitute('/Users/casper/Desktop/download')

# process a single file, and replace it
anonymize_regex.substitute('/Users/casper/Desktop/my_file.json')
```

## Todo

Testing ;)