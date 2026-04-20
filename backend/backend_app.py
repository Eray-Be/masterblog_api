from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."}
]


@app.route('/api/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        return jsonify(POSTS)

    elif request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        missing_fields = []

        if not data.get("title"):
            missing_fields.append("title")
        if not data.get("content"):
            missing_fields.append("content")

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

        new_post = {
            "id": new_id,
            "title": data["title"],
            "content": data["content"]
        }

        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({
                "message": f"Post with id {post_id} has been deleted successfully."
            }), 200

    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    for post in POSTS:
        if post["id"] == post_id:
            if "title" in data:
                post["title"] = data["title"]
            if "content" in data:
                post["content"] = data["content"]

            return jsonify(post), 200

    return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []

    for post in POSTS:
        title_matches = title_query in post["title"].lower() if title_query else True
        content_matches = content_query in post["content"].lower() if content_query else True

        if title_matches and content_matches:
            results.append(post)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)