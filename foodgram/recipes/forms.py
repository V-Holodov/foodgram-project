from django import forms
from recipes import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = [
            'name', 'tag', 'ingredient', 'cooking_time', 'description', 'image'
            ]
        exclude = ['author']

    def clean_text(self):
        data = self.cleaned_data['name']
        if not data:
            raise forms.ValidationError('Поле обязательно для заполнения')
        return data
