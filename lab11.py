from fastapi import FastAPI, HTTPException, Path
from typing import Dict
import uvicorn
import requests

app = FastAPI()

# Імпровізована база даних для зберігання постів
db: Dict[int, dict] = {
    1: {"id": 1, "title": "Перший пост", "content": "Це вміст першого поста"},
    2: {"id": 2, "title": "Другий пост", "content": "Це вміст другого поста"}
}

request_counts = {"version": 0, "posts": 0, "stats": 0}

@app.get("/version")
def read_version():
    request_counts["version"] += 1
    return {"version": "1.0"}

@app.get("/posts/{post_id}")
def read_post(post_id: int = Path(..., title="The ID of the post to read")):
    request_counts["posts"] += 1
    if post_id not in db:
        raise HTTPException(status_code=404, detail="Post not found")
    return db[post_id]

@app.post("/posts")
def create_post(title: str, content: str):
    request_counts["posts"] += 1
    new_id = max(db.keys()) + 1
    db[new_id] = {"id": new_id, "title": title, "content": content}
    return db[new_id]

@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str, content: str):
    request_counts["posts"] += 1
    if post_id not in db:
        raise HTTPException(status_code=404, detail="Post not found")
    db[post_id] = {"id": post_id, "title": title, "content": content}
    return db[post_id]

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    request_counts["posts"] += 1
    if post_id not in db:
        raise HTTPException(status_code=404, detail="Post not found")
    del db[post_id]
    return {"message": "Post deleted"}

@app.get("/stats")
def get_stats():
    request_counts["stats"] += 1
    return request_counts


response = requests.get("http://127.0.0.1:8000/version")
print("Version Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())
print()

# Тестовий сценарій для /posts/{post_id} (GET)
response = requests.get("http://127.0.0.1:8000/posts/1")
print("Read Post Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())
print()

# Тестовий сценарій для /posts (POST)
new_post_data = {"title": "Третій пост", "content": "Це вміст третього поста"}
response = requests.post("http://127.0.0.1:8000/posts", json=new_post_data)
print("Create Post Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())
print()

# Тестовий сценарій для /posts/{post_id} (PUT)
updated_post_data = {"title": "Оновлений пост", "content": "Оновлений вміст третього поста"}
response = requests.put("http://127.0.0.1:8000/posts/3", json=updated_post_data)
print("Update Post Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())
print()

# Тестовий сценарій для /posts/{post_id} (DELETE)
response = requests.delete("http://127.0.0.1:8000/posts/3")
print("Delete Post Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())
print()

# Тестовий сценарій для /stats (GET)
response = requests.get("http://127.0.0.1:8000/stats")
print("Stats Endpoint Test:")
print("Status Code:", response.status_code)
print("Response Body:", response.json())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

#uvicorn lab11:app --reload
    
