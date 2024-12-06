from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma
import os
from py4web import action, Field, DAL
from py4web.utils.grid import *
from py4web.utils.form import *
from yatl.helpers import A

# Initialize the URL signer with the session
url_signer = URLSigner(session)

# Controller for the index page
@action("index", method=["GET", "POST"])
@action.uses("index.html", db, session)
def index():
    # Define the contact form with required fields
    form = Form(
        db.contact_requests, 
        csrf_session=session, 
        formstyle=FormStyleBulma
    )
    
    # Redirect back to index on successful submission
    if form.accepted:
        redirect(URL("index"))
    
    # Return the form for rendering
    return dict(form=form)

@action("contact_requests", method=["GET", "POST"])
@action("contact_requests/<path:path>", method=["GET", "POST"])
@action.uses("contact_requests.html", db, auth)
def contact_requests(path=None):
    # Check if the current user is the admin
    if get_user_email() != "admin@example.com":
        redirect(URL("index"))
    
    # Define a grid to manage contact requests
    grid = Grid(
        path,
        query=db.contact_requests.id > 0,
        search_queries=[
            ["Search by Name", lambda val: db.contact_requests.name.contains(val)],
            ["Search by Message", lambda val: db.contact_requests.message.contains(val)]
        ],
        grid_class_style=GridClassStyleBulma,
        orderby=[~db.contact_requests.created_on]
    )
    
    # Return the grid for rendering
    return dict(grid=grid)