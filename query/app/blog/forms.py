from django import forms

from blog.models import Flavor, IceCreamStore
from blog.validators import validate_tasty


class FlavorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty)
        self.fields['slug'].validators.append(validate_tasty)

    class Meta:
        model = Flavor
        fields = ['title', 'slug', 'scoops_remaining']


class IceCreamOrderForm(forms.Form):
    slug = forms.ChoiceField(label=Flavor)
    topping = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].choices = [(x.slug, x.title) for x in Flavor.objects.all()]

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg = u"Sorry, we are out of that flavor"
            raise forms.ValidationError(msg)
        return slug

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug', '')
        toppings = cleaned_data.get('topping', '')

        if u'chocolate' in slug.lower() and u'chocolate' in toppings.lower():
            msg = u"Your order has too much chocolate."
            raise forms.ValidationError(msg)
        return cleaned_data


class IceCreamStoreCreateForm(forms.ModelForm):
    class Meta:
        model = IceCreamStore
        fields = ['title', 'block_address']


class IceCreamStoreUpdateForm(IceCreamStoreCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['description'].required = True

    class Meta(IceCreamStoreCreateForm.Meta):
        fields = ['title', 'block_address', 'phone', 'description']
