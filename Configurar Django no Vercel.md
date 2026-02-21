<!-- # Configurar Django no Vercel

No arquivo `settings.py`:
```python
ALLOWED_HOSTS = [".vercel.app"]
```

e também:
```python
DEBUG = False
```

---

No arquivo `wsgi.py`:

```python
application = get_wsgi_application()

app = application
```
---

No arquivo `vercel.json`:

```json
{
    // "builds": [
    //     {
    //     "src": "project_name/wsgi.py",
    //     "use": "@vercel/python"
    //     }
    // ],
    "routes": [
        {
        "src": "/(.*)",
        "dest": "project_name/wsgi.py"
        }
    ]
}
```

> ATENÇÃO: Quando você usa "builds" manualmente:<br>
> > A Vercel IGNORA completamente os campos:
> - Install Command
> - Build Command
> - Output Directory
> do painel da Vercel.

---

Na Vercel:
- Comando de `install`:
    ```bash
    pip install -r requirements.txt
    ```

- Comandos de `build`:
    ```bash
    python manage.py collectstatic --noinput
    ```

- Variáveis de ambiente, caso tenha -->
