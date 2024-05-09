```mermaid
classDiagram
class Weibo
class Database {<<interface>>}
class Notifier {<<interface>>}
class MySQL
Class MongoDB
class Sqlite

Database <|-- MySQL
Database <|-- MongoDB
Database <|-- Sqlite
```
