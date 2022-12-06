from __future__ import annotations
from message_app.db.db import DB as db
import json
import time
from typing import Union, List
from sqlalchemy import func, desc, asc, not_, and_, true
from sqlalchemy.sql import label


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    student_id = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone_number = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))

    initiators = db.relationship("BuyRequest", backref="initiator", foreign_keys="BuyRequest.initiator_id")
    receivers = db.relationship("BuyRequest", backref="receiver", foreign_keys="BuyRequest.receiver_id")

    def __eq__(self, other_user: User) -> bool:
        # Compare two users using its username
        return other_user.username == self.username


    def to_json(self) -> str:
        data = {
            "id": self.id,
            "username": self.username,
            "student_id": self.student_id,
            "email": self.email,
            "phone_number": self.phone_number,
            "password_hash": self.password_hash,
        }
        return json.dumps(data)


    @classmethod
    def insert(cls, new_user: User) -> None:
        # Add a new user to the database
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def delete(cls, username: str) -> Union[User, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        user = User.select(username)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    @classmethod
    def select(cls, username="*", user_id="*", email="*") -> Union[User, None]:
        user = User.query.filter(and_(
                User.username == username if username != "*" else true(),
                User.id == user_id if user_id != "*" else true(),
                User.email == email if email != "*" else true()
            )).first()
        return user

    @classmethod
    def select_v2(cls, filter_option: dict):
        """Allow querying users with more filter options"""
        pass

    @classmethod
    def select_all(cls) -> List:
        # TODO: This method should be deprecated when add Channel
        all_users = User.query.all()
        return all_users

    @classmethod
    def get_last_user_id(cls) -> int:
        id = User.query.order_by(User.id.desc()).first().id
        return id

### cần sửa cái này ####
    @classmethod
    def find_people(cls, user_id: int) -> List:
        # query all requests that send to user_id
        sub_query = db.session.query(
                BuyRequest,
                label("latest_request", func.max(BuyRequest.request_time))
                ).filter(BuyRequest.receiver_id == user_id).group_by(BuyRequest.initiator_id).subquery()

        #query all users that send request to user_id
        sender_query = db.session.query(
                User.id,
                User.username,
                sub_query.c.id,
                sub_query.c.initiator_id,
                sub_query.c.receiver_id,
                sub_query.c.request_status,
                sub_query.c.request_time,
                sub_query.c.price
                ).join(sub_query, User.id == sub_query.c.initiator_id).order_by(asc(User.id)).all()

        # query all request that user_id send
        sub_query_2 = db.session.query(
                BuyRequest,
                label("latest_request", func.max(BuyRequest.request_time))
                ).filter(BuyRequest.initiator_id == user_id).group_by(BuyRequest.receiver_id).subquery()

        #query all users that receive request from user_id
        receiver_query = db.session.query(
                User.id,
                User.username,
                sub_query_2.c.id,
                sub_query_2.c.initiator_id,
                sub_query_2.c.receiver_id,
                sub_query_2.c.request_status,
                sub_query_2.c.request_time
                ).join(sub_query_2, User.id == sub_query_2.c.receiver_id).order_by(asc(User.id)).all()

        all_request_users = sender_query + receiver_query
        dic = {}
        request_users_id = []

        # filter conversation request between user_id with another, choose the
        # request that has latest request_time
        for i in all_request_users:
            is_receiver = i[0] == i[4]
            key = tuple(sorted([i[3], i[4]]))

            if i[0] not in request_users_id:
                request_users_id.append(i[0])

            if key not in dic:
                dic[key] = {
                        "user_id": i[0],
                        "username": i[1],
                        "request_id": i[2],
                        "request_status": i[5],
                        "request_time": i[6],
                        "is_sender": not is_receiver,
                        "is_receiver": is_receiver
                        }
            else:
                if dic[key]["request_time"] < i[6]:
                    dic[key] = {
                            "user_id": i[0],
                            "username": i[1],
                            "request_id": i[2],
                            "request_status": i[5],
                            "request_time": i[6],
                            "is_sender": not is_receiver,
                            "is_receiver": is_receiver
                            }

        result = list(dic.values())

        # query all the users that do not have any request to/from user_id
        no_request_users = db.session.query(User.id, User.username).filter(
                and_(
                    not_(User.id.in_(request_users_id)),
                    User.id != user_id
                    )
                ).all()

        for i in no_request_users:
            result.append({
                "user_id": i[0],
                "username": i[1],
                "request_id": None,
                "request_status": None,
                "request_time": None,
                "is_sender": None,
                "is_receiver": None
                })

        return result


# SQLAlchemy model for buy_request table
class BuyRequest(db.Model):
    __tablename__ = 'buy_request'
    id = db.Column(db.Integer, primary_key=True)
    initiator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    request_status = db.Column(db.String, nullable=False, default="available") # 3 status: available, pending, process, accepted, rejected
    request_time = db.Column(db.Integer, nullable=False)
    accepted_time = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __eq__(self, other_request: BuyRequest) -> bool:
        # Compare two users using its username
        return other_request.id == self.id

    def to_json(self) -> str:
        data = {
            "id": self.id,
            "initiator_id": self.initiator_id,
            "receiver_id": self.receiver_id,
            "request_status": self.request_status,
            "request_time": self.request_time,
            "accepted_time": self.accepted_time,
            "price": self.price
        }
        return json.dumps(data)

    def accept(self, time: int) -> None:
        self.request_status = "pending"
        self.accepted_time = time
        db.session.commit()

    def reject(self) -> None:
        self.request_status = "rejected"
        db.session.commit()
    
    def done(self) -> None:
        self.request_status = "done"
        db.session.commit()
    
    def process(self) -> None:
        self.request_status = "process"
        db.session.commit()

    @classmethod
    def get_all_requests(cls, request_status: str) -> List:
        """Return latest pending request between sender"""
        all_requests = BuyRequest.query.filter(
                BuyRequest.request_status == "available",
                ).order_by(BuyRequest.id.asc()).all()

        all_requests_list = []

        for request in all_requests:
            all_requests_list.append({
                    "id": request.id,
                    "initiator_id": request.initiator_id,
                    "receiver_id": request.receiver_id,
                    "request_status": request.request_status,
                    "request_time": request.request_time,
                    "accepted_time": request.accepted_time,
                    "price": request.price
                })
        return all_requests_list

    @classmethod
    def get_all_request_by_sender(cls, initiator_id: int, request_status: str) -> list:
        """Return latest pending request between sender"""
        all_requests = BuyRequest.query.filter(
                BuyRequest.initiator_id == initiator_id,
                BuyRequest.request_status == request_status
                ).order_by(BuyRequest.id.asc()).all()
        
        all_requests_list = []

        for request in all_requests:
            all_requests_list.append({
                    "id": request.id,
                    "initiator_id": request.initiator_id,
                    "receiver_id": request.receiver_id,
                    "request_status": request.request_status,
                    "request_time": request.request_time,
                    "accepted_time": request.accepted_time,
                    "price": request.price
                })
        return all_requests_list

    @classmethod
    def get_all_request_by_reciever(cls, receiver_id: int, request_status: str) -> Union[BuyRequest, None]:
        """Return latest pending request between two reciever"""
        all_requests = BuyRequest.query.filter(
                BuyRequest.receiver_id == receiver_id,
                BuyRequest.request_status == request_status
                ).order_by(BuyRequest.id.asc()).all()
        
        all_requests_list = []

        for request in all_requests:
            all_requests_list.append({
                    "id": request.id,
                    "initiator_id": request.initiator_id,
                    "receiver_id": request.receiver_id,
                    "request_status": request.request_status,
                    "request_time": request.request_time,
                    "accepted_time": request.accepted_time,
                    "price": request.price
                })
        return all_requests_list
    
    @classmethod
    def get_all_request_by_sender_reciever (cls, sender_id: int, receiver_id: int) -> list:
        all_requests = BuyRequest.query.filter(
                BuyRequest.receiver_id == receiver_id,
                BuyRequest.initiator_id == sender_id
                ).order_by(BuyRequest.id.asc()).all()
        
        all_requests_list = []

        for request in all_requests:
            all_requests_list.append({
                    "id": request.id,
                    "initiator_id": request.initiator_id,
                    "receiver_id": request.receiver_id,
                    "request_status": request.request_status,
                    "request_time": request.request_time,
                    "accepted_time": request.accepted_time,
                    "price": request.price
                })
        return all_requests_list

    @classmethod
    def get_request_by_sender_id(cls, sender_id: int, request_status: str, time: int) -> Union[BuyRequest, None]:
        request = BuyRequest.query.filter(
                BuyRequest.id == sender_id,
                BuyRequest.request_status == request_status,
                BuyRequest.request_time == time
                )
        return request

    @classmethod
    def insert(cls, new_request: BuyRequest) -> None:
        db.session.add(new_request)
        db.session.commit()

    @classmethod
    def delete(cls, request_id: int) -> Union[BuyRequest, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        request = BuyRequest.get_request_by_id(request_id)
        if request:
            db.session.delete(request)
            db.session.commit()
        return request


class item (db.model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("buyrequest.id"), nullable=False)
    item_name = db.Column(db.String, nullable=False) 
    item_quanity = db.Column(db.Integer, nullable=False)

    def __eq__(self, other_request: BuyRequest) -> bool:
        # Compare two users using its username
        return other_request.id == self.id

    def to_json(self) -> str:
        data = {
            "id": self.id,
            "initiator_id": self.request_id,
            "receiver_id": self.item_name,
            "status": self.item_quanity
        }
        return json.dumps(data)

    @classmethod
    def get_all_item_by_request_id (cls, request_id : int)-> list:
        all_items = item.query.filter(
                item.request_id == request_id,
                ).order_by(item.id.asc()).all()

        all_items_list = []

        for request in all_items:
            all_items_list.append({
                    "id": request.id,
                    "initiator_id": request.request_id,
                    "receiver_id": request.item_name,
                    "request_time": request.item_quanity
                })
        return all_items_list
    @classmethod
    def insert(cls, new_request: item) -> None:
        db.session.add(new_request)
        db.session.commit()

    @classmethod
    def delete(cls, request_id: int) -> Union[item, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        request = item.query.filter(
                item.request_id == request_id,
                ).order_by(item.id.asc()).all()
        if request:
            db.session.delete(request)
            db.session.commit()
        return request
