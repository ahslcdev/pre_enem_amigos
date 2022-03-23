from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class BaseManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extrafields):
        if not username:
            raise ValueError('Informe o usuário')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extrafields)

    def create_superuser(self, username, password, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError('Precisa ser true')
        if extrafields.get('is_superuser') is not True:
            raise ValueError('Precisa ser true')

        return self._create_user(username, password, **extrafields)


class Usuario(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        max_length=255, blank=False, null=False)

    status = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = BaseManager()

    class Meta:
        db_table = 'usuario'

class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    genero = models.CharField('Gênero', max_length=255)

    class Meta:
        db_table = 'genero'

class Cor(models.Model):
    id = models.AutoField(primary_key=True)
    cor = models.CharField('Cor', max_length=255)
    class Meta:
        db_table = 'cor'

class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    disciplina = models.CharField('Disciplina', max_length=255)
    descricao = models.CharField('Descricao', max_length=255)
    class Meta:
        db_table = 'disciplina'

class Graduacao(models.Model):
    id = models.AutoField(primary_key=True)
    graduacao = models.CharField('Graduação', max_length=255)
    class Meta:
        db_table = 'graduacao'

class Pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    nome_oficial = models.CharField('Nome oficial', max_length=255)
    nome_social = models.CharField('Nome social', max_length=255)
    data_nasc = models.DateField('Data de nascimento')
    cpf = models.CharField('CPF', max_length=14, unique=True)

    cep = models.CharField('CEP', max_length=10)
    endereco = models.CharField('Endereco', max_length=255)
    numero = models.IntegerField('Número')
    bairro = models.CharField('Bairro', max_length=255)
    cidade = models.CharField('Cidade', max_length=255)
    estado = models.CharField('Estado', max_length=255)

    observacoes = models.TextField('Observacoes')

    id_genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    id_cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pessoa'


class Professor(Pessoa):
    eh_adm = models.BooleanField('É professor administrador?', default=False)
    telefone = models.CharField('Telefone', max_length=11, null=True, blank=True)
    eh_wpp = models.BooleanField('É whatsapp?', default=False)
    id_graduacao = models.ForeignKey(Graduacao, on_delete=models.CASCADE)

    class Meta:
        db_table = 'professor'

class ProfessorDisciplina(models.Model):
    id = models.AutoField(primary_key=True)
    id_professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    class Meta:
        db_table = 'prof_disciplina'

class Aluno(Pessoa):
    class Meta:
        db_table = 'aluno'
