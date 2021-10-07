# Table2JSON
Convert Tabular Data to JSON

**Python 3.9 >= 3.X >= 3.7**

## Ubuntu
    apt-get install python3.X-venv python3.X-dev libssl-dev libmysqlclient-dev

## Windows
    Install Visual C++ Redistributable [Latest]

## Requirements [For Build]
    pip install -r requirements/build.txt

## Requirements [For Development]
    pip install -r requirements/build.txt
    pip install -r requirements/development.txt

## Compile
tox -c . -e py{37,38,39}-pyinstaller
Find Build Under src/dist/Table2JSON-py{37,38,39}

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
