from flask import request, session, g, redirect, url_for, abort, render_template, flash
from flask.views import MethodView

from database import db_session
from models import State, City

import Objects


class SignOutView(MethodView):

    def get(self):
        username = session.get('username')
        flash('You are signed out')
        if username is not None:
          session.pop('username')
          session.pop('userid')
        return redirect(url_for('signinview'))