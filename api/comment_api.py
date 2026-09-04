from config.settings import API_POSTS

class CommentApi:
    def __init__(self, client):
        self.client = client

    # 发表评论（一级评论）或 回复评论（二级评论）
    # 二级评论只需要在 content 里带上 @用户名 #楼层ID
    def create_post(self, discussion_id: int, content: str):
        req_body = {
            "data": {
                "type": "posts",
                "attributes": {
                    "content": content
                },
                "relationships": {
                    "discussion": {
                        "data": {
                            "type": "discussions",
                            "id": str(discussion_id)
                        }
                    }
                }
            }
        }
        return self.client.post(path=API_POSTS, json_data=req_body)

    # 删除评论（抓包确认：软删除，使用 POST 携带 isHidden: true）
    def delete_post(self, post_id: int):
        req_body = {
            "data": {
                "type": "posts",
                "id": str(post_id),
                "attributes": {
                    "isHidden": True
                }
            }
        }
        return self.client.post(path=f"{API_POSTS}/{post_id}", json_data=req_body)