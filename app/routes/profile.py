from flask import Blueprint, render_template, session, redirect
from app.models.user import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/perfil')
def perfil():
    user_id = session.get('user_id')

    if not user_id:
        return redirect('/login')

    user = User.query.get(user_id)
    return render_template('perfil.html', user=user)