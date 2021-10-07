# coeus-api

This is a main API service of `coeus`

## API Documentation
### `GET /heathcheck`
Request: `None`

Response: `'OK'` with HTTP Status `200`

### `POST /semi-structured/predict`
Request:
- `"wiki_path"` is a path to wikipedia document.
```json
{
  "wiki_path": "Pol%27and%27Rock_Festival"
}
```
Response:
`"result"` is an array of an array of edges and nodes.
```json
{
    "result": {
        "edges": [
            {
                "childId": 2,
                "parentId": 1
            },
            .
            .
            .
        ],
        "nodes": [
            {
                "id": 1,
                "text": "Pol'and'Rock Festival"
            },
            .
            .
            .
        ]
    }
}
```

### `POST /unstructured/predict`
Request:
- `"topic"` is a string of the topic of an article.
- `"text"` is a string of the content of an article.
```json
{
  "topic": "News - Apple helps Encircle expand...",
  "text": "In the summer of 2017, the Toelupe family heard about a little blue house in Provo, Utah, ..."
}
```
Response:
`"result"` is an array of an array of edges and nodes.
```json
{
    "result": {
        "edges": [
            {
                "childId": 2,
                "parentId": 1
            },
            .
            .
            .
        ],
        "nodes": [
            {
                "id": 1,
                "text": "News - Apple helps Encircle expand..."
            },
            .
            .
            .
        ]
    }
}
```

## Run
1. Copy file `.env.example` into `.env` and fill in all necessary values
2. Make sure you have Docker installed on your system and running
3. Build Docker image with a name of your choice if you haven't
```shell
docker build --tag coeus-main-api .
```
5. Spin up a server
```shell
docker run -d -p 5000:5000 --name coeus-main-api coeus-main-api
```
6. Try accessing [http://127.0.0.1:5000](http://127.0.0.1:5000) with a valid route