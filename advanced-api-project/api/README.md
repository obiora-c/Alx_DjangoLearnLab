

## Book API Endpoints

All endpoints are located under `/api/`.

### Endpoints

- `GET /books/`  
  Retrieves a list of all books. Open to all users.

- `GET /books/<int:pk>/`  
  Retrieves a single book by its ID. Open to all users.

- `POST /books/create/`  
  Creates a new book. Requires authentication.

- `PUT /books/<int:pk>/update/`  
  Updates an existing book. Requires authentication.

- `DELETE /books/<int:pk>/delete/`  
  Deletes a book. Requires authentication.

### Permissions

- **Authenticated users**: Full access (create, update, delete)
- **Unauthenticated users**: Read-only access (list, detail)

### Customizations

- Custom validation on `publication_year` ensures books cannot be set in the future.
- Generic class-based views (`ListAPIView`, `CreateAPIView`, etc.) are used for clean, DRY code.





# ✅ API Testing Overview

### Test File:
- Location: `api/tests/test_views.py`
- Framework: Django REST Framework's APITestCase (based on `unittest`)

---

### 🔍 Covered Test Cases:

- `GET /books/` – List all books
- `GET /books/<id>/` – Retrieve single book
- `POST /books/create/` – Create a book (authenticated only)
- `PUT /books/<id>/update/` – Update a book (authenticated only)
- `DELETE /books/<id>/delete/` – Delete a book (authenticated only)
- Filtering by `publication_year`
- Searching by `title`
- Ordering by `title`
- Validation: Rejecting books with future publication years
- Permission enforcement: Blocking unauthenticated POST/PUT/DELETE

---

### 🚀 Running the Tests

```bash
python manage.py test api

























## 📚 Book API - Advanced Querying

### ✅ Filtering

You can filter books using:

- `?title=<string>`
- `?publication_year=<int>`
- `?author=<author_id>`

**Example**: `/api/books/?publication_year=2020`

---

### 🔍 Search

You can search by:

- Book title
- Author's name

**Example**: `/api/books/?search=Orwell`

---

### ↕️ Ordering

You can order by:

- `title`
- `publication_year`
- `author`

**Usage**:
- Ascending: `/api/books/?ordering=title`
- Descending: `/api/books/?ordering=-publication_year`
