from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.review import Review
from flask import render_template, request
from ..extensions import app, db


class FilterByDoorNumber(MethodView):
    def post(self):
        user_door_request = request.form['searchDoorNum']
        check_request = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_door = Review.query.all() 
        return render_template(
            'searchReviewPage.html',
            user_door_request=user_door_request,
            filter_door=filter_door,
        )


app.add_url_rule(
    '/reviews/door_number',
    view_func=FilterByDoorNumber.as_view(
        name='filter_door'
    ),
)