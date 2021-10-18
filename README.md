# Table2JSON
Convert Tabular Data to JSON

**Python 3.9 >= 3.X >= 3.7**

## Ubuntu
    sudo apt-get install python3.X-venv python3.X-dev libssl-dev libmysqlclient-dev

Note: Replace X with Python Minor Version

## Windows
Download, MS VS C++ Redistributable: [Microsoft Visual Studio C++ Redistributable]

Download, Python 3.X: [Python 3.X]

Note: Replace X with Python Minor Version

## Requirements [For Build]
    pip install tox pluggy

## Requirements [For Development]
    pip install tox pluggy
    pip install -r requirements.txt

## Compile
    tox -c src -e py3X-pyinstaller

Find Dist Under src/dist/Table2JSON-py3X

Note: Replace X with Python Minor Version

## Help
### CSV
Table2JSON csv -h

### Excel
Table2JSON excel -h

### SQLite
Table2JSON sqlite -h

### MySQL
Table2JSON mysql -h

### Neo4j
Table2JSON neo4j -h

[Microsoft Visual Studio C++ Redistributable]: https://www.microsoft.com/en-in/download/details.aspx?id=48145
[Python 3.X]: https://www.python.org/downloads/windows/
