# How to setup local environment
1. Install `Python ^3.10`
2. Install `poetry` by executing following command
    ```bash
    # Linux
    curl -sSL https://install.python-poetry.org | python3 -

    # Powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
3. Install dependencies  by executing following command
    ```bash
    poetry install
    ```
4. Run `./main.py` by executing following command
    ```bash
    poetry run python ./scripts/main.py -s /path/to/source/file -o /path/to/output/dir
    ```

    **Options :**
    | option | argument |
    | ---- | ---- |
    | -s | path to source file |
    | --source | path to source file |
    | -o | path to output directory (it won't output csv file if this option not given) |
    | --output | path to output directory (it won't output csv file if this option not given) |

</br>

# Source files formatting rules

| **Category** | **Rule** | **Examples** |
| ---- | ---- | ---- |
| File format | Source file must be formatted in Excel | .xlsx, .xls |
| Sheet name | yyyy-{grade}-{semester} | 2023-1-後 </br> 2023-3編-前 | 
| Table position | Table must start from (row, column) = (0, 0) | |
| Row format | Each day must consists of 2 rows * 5(or 6) columns representing Mon - Sat | |
| Cell format | Each cell must concists of subjects, groups, and rooms, and each component must be separated with `space`. Groups must be in open and closing `parentheses`, and each group must be separated by `forward slash`  </br> Supported patterns: </br> 1. {subject} </br> 2. {subject} {groups} </br> 3. {subject} {groups} ({rooms}) </br> 4. ({rooms}) | 心理学 </br> 英語Ⅱ AB </br> 情報リテ A (102) </br> (N202)