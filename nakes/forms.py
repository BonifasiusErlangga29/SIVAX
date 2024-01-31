from django import forms

STATUS_TIKET_CHOICES = [
    ('terdaftar','terdaftar'),
    ('siap vaksin','siap vaksin'),
    ('tidak lolos screening','tidak lolos screening'),
    ('selesai vaksin','selesai vaksin'),
]

class UpdateTiketForm(forms.Form):
    statusTiket = forms.CharField(label='Role', widget=forms.Select(choices=STATUS_TIKET_CHOICES))
