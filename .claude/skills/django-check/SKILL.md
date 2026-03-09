---
name: django-check
description: Validates Django model and view changes. Use EVERY TIME after editing models.py, views.py, or serializers.py files in the Backend.
context: fork
agent: Explore
allowed-tools: Read, Grep, Glop, Bash
---
Find recently modified Django files in Backend/src/ by running `git diff --name-only` and filtering for models.py, views.py, and serializers.py. 

Then validate each changed file:

  1. **Models**: Any new fields should have appropriate defaults or null=True
  2. **Views**: All ViewSets must have a permission_classes attribute
  3. **Serializers**: Fields listed in Meta.fields must exist on the model
  4. **Imports**: All imported classes must exist in the installed version of DRF

  Report any issues found. If everything looks good, confirm with a brief message.