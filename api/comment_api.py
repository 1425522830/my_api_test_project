from config.settings import API_POSTS

class CommentApi:
    def __init__(self, client):
        self.client = client

    def create_post(self, discussion_id: int, content: str):
        req_body = {"data": {"type": "posts", "attributes": {"content": content},
                             "relationships": {"discussion": {"data": {"type": "discussions", "id": str(discussion_id)}}}}}
        return self.client.post(path=API_POSTS, json_data=req_body)

    def delete_post(self, post_id):
        req_body = {"data": {"type": "posts", "id": str(post_id), "attributes": {"isHidden": True}}}
        return self.client.patch(path=f"{API_POSTS}/{post_id}", json_data=req_body)