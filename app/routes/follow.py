from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.users import User
from ..models.follows import Follow
from ..auth import require_auth

#  following = /:id/following
#  follows = /:id

bp = Blueprint("follow", __name__)

# users who follow user of <id>
@bp.route('/<id>')
def getFollows(id):
    follows = Follow.query.filter(Follow.user_followed_id == id).all()

    followsList = []
    for follower in follows:
        user = User.query.filter(follower.user_id == User.id).first()
        followsList.append(user.to_dict())
    return {"users": followsList}

@bp.route('<id>/following')
def getFollowing(id):
    follows = Follow.query.filter(Follow.user_id == id).all()

    followsList = []
    for follower in follows:
        user = User.query.filter(follower.user_followed_id == User.id).first()
        followsList.append(user.to_dict())
    return {"users": followsList}

@bp.route('', methods=["POST"])
def followUser():
    data = request.json
    exists = Follow.query.filter(Follow.user_id == data['userId']).filter(Follow.user_followed_id == data['userFollowedId']).first()
    if exists:
        return {"error": "Already Follow!"}
    follow = Follow(user_id = data['userId'], user_followed_id = data['userFollowedId'])
    db.session.add(follow)
    db.session.commit()
    return follow.to_dict()

@bp.route('', methods = ["DELETE"])
def deleteFollow():
    data = request.json
    print(data)
    exists = Follow.query.filter(Follow.user_id == data['userId']).filter(Follow.user_followed_id == data['userFollowedId']).first()
    print(exists.to_dict())
    if not exists:
        return {"error": "Doesn't follow!"}
    follow = Follow.query.filter(Follow.user_id == data['userId']).filter(Follow.user_followed_id == data['userFollowedId']).first()
    db.session.delete(follow)
    db.session.commit()
    return follow.to_dict()
