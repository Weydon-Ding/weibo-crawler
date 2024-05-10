```mermaid
classDiagram
class WeiboCrawler
class Weibo
class Database {<<interface>>}
class Notifier {<<interface>>}
class MySQL
Class MongoDB
class Sqlite

WeiboCrawler --> Weibo
WeiboCrawler --> Database
WeiboCrawler --> Notifier
Database <|-- MySQL
Database <|-- MongoDB
Database <|-- Sqlite
```
