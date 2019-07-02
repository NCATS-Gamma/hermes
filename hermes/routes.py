"""Routes."""
from hermes.views import index, fetch


def setup_routes(app):
    """Set up routes."""
    app.router.add_post('/run', index)
    app.router.add_get('/fetch/{job_id}', fetch)
