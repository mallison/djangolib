from django import forms


class ModelFormWithUserForeignKey(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ModelFormWithUserForeignKey, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ModelFormWithUserForeignKey, self).save(commit=False)
        user_fk_name = self._meta.exclude[0]  # FIXME
        setattr(instance, user_fk_name, self.user)
        if commit:
            instance.save()
        return instance
