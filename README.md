# Table2JSON
Convert Tabular Data to JSON

## Ubuntu
    apt-get install python3.7-dev libssl-dev libmysqlclient-dev

## Windows
    Install Visual C++ Redistributable [Latest]

## Requirements
    pip install pandas xlrd sqlalchemy mysqlclient neo4j pyinstaller

## Compile
pyinstaller --onefile src/Table2JSON.py --hidden-import='neobolt.packstream.packer' --hidden-import='neobolt.packstream.unpacker' --hidden-import='neobolt.bolt' --hidden-import='neobolt.bolt.io'

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
