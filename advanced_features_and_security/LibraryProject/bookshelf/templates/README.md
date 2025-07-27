

## Permissions and Groups Setup

This application uses Django's groups and custom permissions to restrict access.

### Permissions:
- can_view: View book list and details
- can_create: Create new books
- can_edit: Update existing books
- can_delete: Delete books

### Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: All permissions

### Setup:
1. Run `python manage.py migrate`
2. Run `python manage.py setup_groups` to auto-create groups and assign permissions
3. Assign users to groups via the Django admin
