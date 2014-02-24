from application import admin, models, db
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Problem, db.session))
admin.add_view(ModelView(models.News, db.session))
admin.add_view(ModelView(models.Contest, db.session))
admin.add_view(ModelView(models.Submission, db.session))