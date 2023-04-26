from django.forms import ModelForm
from autos.models import Make


# It will just make a form according to a specific model you gave it
# can only make form for one model at a time, You don't have to manually design a form
# fields -> take fields/ column names to take, and __all__ means take all
class MakeForm(ModelForm):
    class Meta:
        model = Make
        fields = '__all__'