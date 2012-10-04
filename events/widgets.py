from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static


class JQueryUIMixin(object):

    @property
    def media(self):
        return forms.Media(
            css={
                'all': (settings.JQUERY_UI_CSS,)
            },
            js=(
                settings.JQUERY_URL,
                settings.JQUERY_UI_URL,
                static("js/jquery-widgets.js")
            )
        )


class JQueryDateInput(JQueryUIMixin, forms.DateInput):

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'datepicker', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(JQueryDateInput, self).__init__(attrs=final_attrs, format=format)


class JQueryTimeInput(JQueryUIMixin, forms.TimeInput):

    class Media:
        css = {
            'all': (static('css/jquery.ui.timepicker.css'),)
        }
        js = (
            static('js/jquery.ui.timepicker.js'),
        )

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'timepicker', 'size': '8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(JQueryTimeInput, self).__init__(attrs=final_attrs, format=format)


class JQuerySplitDateTime(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (JQueryDateInput(attrs=attrs, format=date_format),
                   JQueryTimeInput(attrs=attrs, format=time_format))
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

#    def format_output(self, rendered_widgets):
#        return mark_safe(u'<p class="datetime">%s %s<br />%s %s</p>' % \
#            ('Date:', rendered_widgets[0], 'Time:', rendered_widgets[1]))
