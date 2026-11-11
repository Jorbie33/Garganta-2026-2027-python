# Six String Shop: Backend (Django + DRF)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed             # sample guitars
python manage.py createsuperuser  # optional, for /admin
python manage.py runserver        # http://localhost:8000
```

Requires Python 3.9 or newer. The migration for the custom user model (`shop.BaseUser`) is already included, so just run `migrate`.
Start from a fresh folder (no old `db.sqlite3`).

## API (all under `/api/`)

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `auth/register/` | no | Create an account |
| POST | `auth/login/` | no | Get `access` and `refresh` JWT tokens |
| POST | `auth/refresh/` | no | Refresh the access token |
| GET/PATCH | `auth/me/` | yes | Current user |
| GET | `products/?search=&ordering=` | no | List guitars |
| GET | `products/<id>/` | no | One guitar |
| GET | `cart/` | yes | Current cart |
| POST | `cart/items/` | yes | `{product_id, quantity}` |
| PATCH/DELETE | `cart/items/<id>/` | yes | Change quantity or remove |
| POST | `checkout/` | yes | Turn the cart into a transaction |
| GET | `transactions/` | yes | Order history |

Add product photos in `/admin` (Products, then Thumbnail). The frontend draws a guitar when there is no photo.
