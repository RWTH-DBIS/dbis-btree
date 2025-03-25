![DBIS Informatik 5 - Informationssysteme und Datenbank](https://dbis.rwth-aachen.de/dbis/wp-content/uploads/2022/04/dbis-logo.png)



# Dokumentation zur Nutzung des B-Baum
In der Vorlesung haben Sie B-Bäume kennengelernt.
Dieses Blatt gibt einen kurzen Überblick über ein von uns entwickeltes Python-Tool.\
Im DBIS Image des Jupyter Hub der RWTH ist dieses Package bereits integriert, falls Sie das Tool lokal benutzen möchten, können Sie diese über den folgenden Befehl installieren:
```python_pip install dbis-btree
pip install dbis-btree
# in jupyter notebooks:
!pip install dbis-btree
```
Die folgende Zelle importiert das Python Modul und ermöglicht dessen Nutzung innerhalb des Notebooks:
```python
from dbis_btree.BBaum import BTree
```

## B-Baum als Objekt

Als erstes müssen Sie eine neue Instanz der Klasse `BTree` erzeugen. Diesem Objekt werden im weiteren Verlauf Knoten `nodes` und Kanten `edges` hinzugefügt.
Geben Sie die `M`-Value für den B-Baum an.

```python
# zum Beispiel M = 4
M = 4
bbaum = BTree(4)
# anzeigen des noch leeren bbaums:
bbaum.draw()
```

## Knoten
Neue Knoten zum Baum hinzufügen: `add_node(name, elements)`

Geben sie dem Knoten einen _eindeutigen_ Namen und die Zahlen, die im Knoten sich befinden sollen.\
Wenn im Graph schon der Knoten mit diesem Namen existiert, kommt der Fehler:
```commandline
AssertionError: Bitte nutze einen anderen Name für diese Node.
```

Konstruktor einer Relation:
* `name`: String - Eindeutiger Name des Knoten
* `elements`: Int Liste - Liste aus Int

```python
bbaum = BTree(4)
# hinzufügen Knoten A
name = "A"
elements = [10,20]

bbaum.add_node(name, elements)

# hinzufügen Knoten B
bbaum.add_node("B", [1,2])

# nicht vergessen, den baum anzuzeigen:
bbaum.draw()
```
![B-Tree generated above](./examples/images/image_1.svg)


## Kanten
Neue Knoten zum Baum hinzufügen: `add_edge(parent, child, n_child):`

Dies fügt im Baum eine Kante vom `parent`-Knoten zum `child`-Knoten, an der der `n_child`-ten Stelle im `parent`-Knoten.

Konstruktor einer Relation:
* `name`: String - Eindeutiger Name des Parent Knoten
* `child`: String - Eindeutiger Name des Child Knoten
* `n_child`: Int - Position im Parent Knoten.


```python
bbaum = BTree(4)
# hinzufügen Knoten A
name = "A"
elements = [10,20]

bbaum.add_node(name, elements)

# hinzufügen Knoten B
bbaum.add_node("B", [1,2])

# hinzufügen einer Kante an 1st Stelle
positionImParentNode = 1
bbaum.add_edge("A", "B", positionImParentNode)

# nicht vergessen, den baum anzuzeigen:
bbaum.draw()
```
![B-Tree generated above](./examples/images/image_2.svg)

### Häufige Fehler und Warnungen

`Warning: node A, port f5 unrecognized`\
\
bedeutet, dass eine falsche Zahl beim Parameter `n_child` genutzt wurde.\
`add_edge(parent, child, n_child):`\
In unserem Fall wurde dieser Fehler wurde ausgelöst, als eine Kante an Stelle 5 in Knoten A hinzugefügt wurde. Jedoch besaß A nur insgesamt Stellen 1 bis 4 um Kanten hinzuzufügen.