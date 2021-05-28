from django import forms

from . import models


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].required = False

    class Meta:
        model = models.Recipe
        fields = [
            'name', 'tag_breakfast', 'tag_lunch', 'tag_dinner',
            'ingredient', 'cooking_time', 'description', 'image'
            ]
        exclude = ['author']
        required = {
                    'ingredient': False,
                }

    def clean_text(self):
        data = self.cleaned_data['name']
        if not data:
            raise forms.ValidationError('Поле обязательно для заполнения')
        tag_breakfast = self.cleaned_data['tag_breakfast']
        tag_lunch = self.cleaned_data['tag_lunch']
        tag_dinner = self.cleaned_data['tag_dinner']
        if tag_breakfast == tag_lunch == tag_dinner is False:
            raise forms.ValidationError('Необходимо выбрать тег')
        return data
