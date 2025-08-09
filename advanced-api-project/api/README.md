

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
