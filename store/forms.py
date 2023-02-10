from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(label="Usuario:", min_length=8, max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: gvillacis'}))
    first_name = forms.CharField(label="Nombre:", max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Gabriel'}))
    last_name = forms.CharField(label="Apellido:", max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Villacis'}))
    email = forms.CharField(label="Email:", max_length=75, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Ej.: gvillacis@hotmail.com'}))
    country = forms.CharField(label="País:", max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Ecuador', 'value': 'Ecuador'}))
    city = forms.CharField(label="Ciudad:", max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Guayaquil'}))
    address = forms.CharField(label="Dirección:", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: Av. Quito 392 y Vélez'}))
    cellphone = forms.CharField(label="Celular:", min_length=10, max_length=13, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej.: 0995851023'}))
    password1 = forms.CharField(label="Contraseña:", min_length=8, max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Ej.: de*738Hoewiux!$'}))
    password2 = forms.CharField(label="Confirme la contraseña:", min_length=8, max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Ej.: de*738Hoewiux!$'}))
    
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            self.add_error('password2', "Las contraseñas no coinciden.")

        return cleaned_data