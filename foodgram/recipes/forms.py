from django import forms
from . import models


class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].required = False

    class Meta:
        model = models.Recipe
        fields = [
            'name', 'tag_brekfast', 'tag_lanch', 'tag_dinner',
            'ingredient', 'cooking_time', 'description', 'image'
            ]
        exclude = ['author']
        required = {
                    'ingredient': False,
                }

    def clean_text(self):
        # print(self.data)
        # print(self.cleaned_data)
        data = self.cleaned_data['name']
        if not data:
            raise forms.ValidationError('Поле обязательно для заполнения')
        return data

    # def clean_ingredient(self):
    #     return {'ingredientName_1': 'яблоки'}
