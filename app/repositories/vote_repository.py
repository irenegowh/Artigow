# app/repositories/vote_repository.py

from app.models.votes import Vote
from sqlalchemy import func
from app import db

class VoteRepository:
    @staticmethod
    def add_vote(post_id):
        new_vote = Vote(post_id=post_id)
        db.session.add(new_vote)
        db.session.commit()

    @staticmethod
    def get_votes_for_post(post_id):
        return Vote.query.filter_by(post_id=post_id).all()


#    @staticmethod
#    def get_ranking():
#        ranking_data = db.session.query(Vote.post_id, func.count(Vote.id).label('vote_count')) \
#            .group_by(Vote.post_id) \
#            .order_by(func.count(Vote.id).desc()) \
#            .all()
#        
#        if not ranking_data:
#            # Si no hay votos, devolvemos una lista vacía
#            return []
        
        # Devuelves la lista con el post_id y el número de votos
#        return ranking_data