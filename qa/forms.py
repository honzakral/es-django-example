from django import forms

class TagsField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', ())
        super(TagsField, self).__init__(*args, **kwargs)

    def valid_value(self, value):
        return True

class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    months = forms.DateField(required=False, input_formats=["%Y-%m"])
    tags = TagsField(required=False)