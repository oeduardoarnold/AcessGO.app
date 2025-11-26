# Importar componentes necessários do Flask
from flask import Blueprint, render_template
# Importar decorators e objetos do Flask-Login
from flask_login import login_required, current_user

# Criar Blueprint para rotas principais da aplicação
# Sem url_prefix, as rotas começam diretamente da raiz (/)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
# @login_required  # Decorator que protege a rota - requer autenticação
def index():
    """
    Página inicial do sistema (protegida).
    
    Apenas usuários autenticados podem acessar esta página.
    Se não autenticado, será redirecionado para a página de login.
    
    Returns:
        Renderiza o template index.html com dados do usuário atual
    """
    # current_user é um objeto especial do Flask-Login que representa
    # o usuário atualmente autenticado na sessão
    
    
    slides_data = [
        {
            "image": "static/images/bento.jpg",
            "title": "Bento Gonçalves - RS",
            "link": "/destinos/bento", # Rota para onde o botão vai
            "button_text": "Ver mais"
        },
        {
            "image": "static/images/porto.jpg",
            "title": "Porto Alegre - RS",
            "link": "/destinos/porto",
            "button_text": "Ver mais"
        },
        {
            "image": "static/images/gramado.jpg",
            "title": "Gramado - RS",
            "link": "/destinos/gramado",
            "button_text": "Ver mais"
        }
    ]
    
    return render_template('index.html', user=current_user, slides=slides_data)

@main_bp.route('/dashboard')
@login_required  # Esta rota também requer autenticação
def dashboard():
    """
    Página de dashboard (protegida).
    
    Exemplo de rota adicional protegida. Pode ser usada para
    exibir estatísticas, relatórios ou informações do usuário.
    
    Returns:
        Renderiza o template dashboard.html com dados do usuário
    """
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/perfil')
@login_required
def perfil():
    """
    Pagina de perfil limitada a quem ja tem login na plaraforma
    """
    return render_template('perfil.html',user=current_user)


@main_bp.route("/destinos/<destino>")
def destinos(destino):
    print(destino)
    if destino == "bento":
        return render_template("bento.html",user=current_user )

    if destino == "porto":
        return render_template("porto.html",user=current_user )

    if destino == "gramado":
        return render_template("gramado.html",user=current_user )
