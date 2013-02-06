"""
Generic views that let you specify the model in the url (admin-stylee)
and automatically restrict objects to those owned by request.user.

Provides a base set of views for fleshing out an app.

Note: THIS IS PROBABLY ALL GASH AND DONE PROPERLY BY SOMEONE CLEVER ON
THE INTERNET BUT I JUST WANTED TO HAVE A GO AT HACKING GENERIC
VIEWS. SO THERE.

"""
from django.contrib.auth.models import User
from django.db.models.loading import cache
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from ..forms.models import ModelFormWithUserForeignKey


class ModelNameInUrlMixin(object):
    def dispatch(self, *args, **kwargs):
        self.model_name = kwargs['model']
        # TODO remove hard-coded 'main' app name here
        self.model = cache.get_model('main', self.model_name)
        if self.model is None:
            raise ValueError("No such model: %s" % self.model_name)
        return super(ModelNameInUrlMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelNameInUrlMixin, self).get_context_data(**kwargs)
        context['model_name'] = self.model_name
        return context


class CurrentUserMixin(object):
    # can be provided explicitly or introspected for direct fk
    user_fk_relation = None
    def dispatch(self, *args, **kwargs):
        model = self.model or self.queryset.model
        if not self.user_fk_relation:
            self.user_fk_relation = get_user_fk_for_model(model).name
        return super(CurrentUserMixin, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(CurrentUserMixin, self).get_queryset()
        return queryset.filter(**{self.user_fk_relation: self.request.user})
    

    def get_form_class(self):
        return modelform_factory(self.model,
                                 exclude=(self.user_fk_relation,),
                                 form=ModelFormWithUserForeignKey)

    def get_form_kwargs(self):
        kwargs = super(CurrentUserMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ListViewForCurrentUser(ModelNameInUrlMixin, CurrentUserMixin, ListView):
    pass

        
class DetailViewForCurrentUser(ModelNameInUrlMixin, CurrentUserMixin, DetailView):
    pass


class CreateForCurrentUserView(CurrentUserMixin, CreateView):
    pass


def get_user_fk_for_model(model):
    for field in model._meta.fields:
        if field.rel and field.rel.to == User:
            break
    else:
        raise ValueError("Model %r has no user foreign key" % model)
    # TODO check for more than one fk
    return field


class DefaultTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = request.path[1:]
        return super(DefaultTemplateView, self).dispatch(request, *args, **kwargs)
