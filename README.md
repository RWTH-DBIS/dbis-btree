![DBIS Informatik 5 - Informationssysteme und Datenbank](https://dbis.rwth-aachen.de/dbis/wp-content/uploads/2022/04/dbis-logo.png)



# Dokumentation zur Nutzung des B-Baum
In der Vorlesung haben Sie B-Bäume kennengelernt.
Dieses Blatt gibt einen kurzen Überblick über ein von uns entwickeltes Python-Tool.\
Im DBIS Image des Jupyter Hub der RWTH ist dieses Package bereits integriert, falls Sie das Tool lokal benutzen möchten, können Sie diese über den folgenden Befehl installieren:
```python
!pip install dbis-btree
print("currently not implemented")
```
Die folgende Zelle importiert das Python Modul und ermöglicht dessen Nutzung innerhalb des Notebooks:
```python
from dbis-btree.BBaum import BTree
```

## B-Baum als Objekt

Als erstes müssen Sie eine neue Instanz der Klasse `BTree` erzeugen. Diesem Objekt werden im weiteren Verlauf Knoten `nodes` und Kanten `edges` hinzugefügt.
Geben Sie die `M`-Value für den B-Baum an.