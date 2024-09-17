import os

def signin_email_template(user: str, url: str):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="text-align: left;">
    <h2> Olá {user},</h2>
    <h3>Você fez um cadastro na plataforma Vitalize Centro Estético.</h3>
    <h3>Confirme seu cadastro clicando no link abaixo.</h3>
    <h3><a href="{os.getenv('CSRF_TRUSTED_ORIGINS', '')}{url}">Confirmar Cadastro.</a><h4>
    <p>&copy; 2024 Vitalize Centro Estético.</p>
    </body>
    </html>
  """
