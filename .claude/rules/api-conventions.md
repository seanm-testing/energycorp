# API Design Conventions

- All ViewSets must set `permission_classes` explicitly
- Permission types: AllowAdmin (type 1), AllowManager (type 2), AllowOperator (type 3)
- Serializers must use explicit `fields` lists, never `fields = '__all__'`
- All list endpoints should support filtering where practical
- URL pattern: /api/<app-name>/<resource>/ (plural nouns)
- Response format for errors: `{"message": "...", "code": <http_code>, "data": {}}`