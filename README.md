Для поиска ближайших соседей используется пакет nmslib/hnswlib с реализацией алгоритма HNSW.  
Координаты (долгота и широта) переводятся в трехмерные. Соседи находятся по хордам. Затем находится соответствующая длина дуги.  
При запуске сервиса пользователи загружаются из базы в NeighborIndex с предварительно конвертированными координатами.  

Сборка docker compose и запуск:  
```
docker-compose build  
docker-compose up  
```
Далее сервис доступен по url: _http://0.0.0.0:8080_
