from app.extensions import mongo

def get_all_videos():
    """Trả về tất cả các video"""
    return list(mongo.db.videos.find())

def get_videos_by_tag(video_tag):
    print("TAG param received:", video_tag)
    return list(mongo.db.videos.find({"tag": (video_tag)}))

def get_video_by_id(video_id):
    """Trả về video theo ObjectId"""
    from bson.objectid import ObjectId
    return mongo.db.videos.find_one({"_id": ObjectId(video_id)})

def insert_video(video_data):
    """Thêm video mới"""
    return mongo.db.videos.insert_one(video_data)

def update_video(video_id, update_data):
    """Cập nhật video"""
    from bson.objectid import ObjectId
    return mongo.db.videos.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": update_data}
    )

def delete_video(video_id):
    """Xoá video"""
    from bson.objectid import ObjectId
    return mongo.db.videos.delete_one({"_id": ObjectId(video_id)})