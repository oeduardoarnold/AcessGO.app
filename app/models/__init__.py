# Importar modelos para facilitar o acesso em outras partes da aplicação
# Isso permite fazer: from app.models import User
# Em vez de: from app.models.user import User
from app.models.user import User
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.experiencia import Experiencia
from app.models.acessibilidade import Acessibilidade
from app.models.favorito import Favorito
from app.models.carrinho import Carrinho