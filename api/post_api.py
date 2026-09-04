from config.settings import API_DISCUSSIONS, API_POSTS

class PostApi:
    def __init__(self, client):
        self.client = client

    def get_primary_tag_id(self):
        resp = self.client.get(path="/api/tags")
        tags = resp.json()["data"]
        for tag in tags:
            if tag["attributes"].get("isPrimary"):
                return tag["id"]
        return tags[0]["id"] if tags else None

    def create_discussion(self, title, content, tag_ids=None):
        tags_data = []
        if tag_ids:
            for tag_id in tag_ids:
                tags_data.append({"type": "tags", "id": str(tag_id)})
        req_body = {"data": {"type": "discussions", "attributes": {"title": title, "content": content},
                             "relationships": {"tags": {"data": tags_data}}}}
        return self.client.post(path=API_DISCUSSIONS, json_data=req_body)

    def get_discussions_list(self, page_offset=0, sort="-lastPostedAt"):
        params = {"include": "user,lastPostedUser,tags,tags.parent,firstPost", "sort": sort, "page[offset]": page_offset}
        return self.client.get(path=API_DISCUSSIONS, params=params)

    def get_discussion_detail(self, discussion_id):
        return self.client.get(path=f"{API_DISCUSSIONS}/{discussion_id}")

    def get_first_post_id(self, discussion_id):
        resp = self.client.get(path=f"{API_DISCUSSIONS}/{discussion_id}", params={"include": "firstPost"})
        if resp.status_code == 200:
            return resp.json()["data"]["relationships"]["firstPost"]["data"]["id"]
        return None

    def edit_post(self, post_id, content=None):
        req_body = {"data": {"type": "posts", "id": str(post_id), "attributes": {}}}
        if content is not None: req_body["data"]["attributes"]["content"] = content
        return self.client.patch(path=f"{API_POSTS}/{post_id}", json_data=req_body)

    def delete_post(self, post_id):
        req_body = {"data": {"type": "posts", "id": str(post_id), "attributes": {"isHidden": True}}}
        return self.client.post(path=f"{API_POSTS}/{post_id}", json_data=req_body)

    def delete_discussion(self, discussion_id):
        req_body = {"data": {"type": "discussions", "id": str(discussion_id), "attributes": {"isHidden": True}}}
        return self.client.patch(path=f"{API_DISCUSSIONS}/{discussion_id}", json_data=req_body)