from django import forms
from .models import Profile, Market, Product

class PictureUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {'image':forms.FileInput(attrs={'hidden':'hidden'})}

class CreateMarket(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    class Meta:
        model = Market
        fields = '__all__'
        exclude = ('user',)
        labels = {
            'name':'Market Name',
            'image':'Market Image',
            'mobile_phone':'Mobile Phone',
            'address':'Address',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'mobile_phone':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
        }


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('seller',)
        labels = {
            'image' : 'Product Image',
            'name' : 'Product Name',
            'description' : 'Description',
            'price':'Price',
            'category':'Category',
        }

        widgets = {
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.TextInput(attrs={'class':'form-control'}),
        }