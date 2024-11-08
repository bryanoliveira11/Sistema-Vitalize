import os


def schedule_confirmation(user: str, url: str, date, time):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="text-align: left;">
    <h2> Olá {user},</h2>
    <h3>
    Você fez agendamento na plataforma Vitalize Centro Estético
    para o dia {date} às {time}.
    </h3>
    <h4><a href="{os.getenv('CSRF_TRUSTED_ORIGINS', '')}{url}">
    Veja seus Agendamentos.</a>
    <h4>
    <p>&copy; 2024 Vitalize Centro Estético.</p>
    </body>
    </html>
  """
