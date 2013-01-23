from django import forms
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class RadioFieldWithOtherRenderer(forms.widgets.RadioFieldRenderer):
    
    def render(self):
        radio_list = []
        for i, choice in enumerate(self.choices):
            radio = forms.widgets.RadioInput(self.name, self.value, self.attrs.copy(), choice, i)
            if radio.choice_label.lower() == 'other':
                if self.value and self.value not in [c[0] for c in self.choices]:
                    radio = forms.widgets.RadioInput(self.name, radio.choice_value, self.attrs.copy(), choice, i)
                    radio = u'<li>%s <input type="text" name="other_%s" value="%s" /></li>'% (force_unicode(radio), radio.name, self.value)
                else:
                    radio = u'<li>%s <input type="text" name="other_%s" /></li>'% (force_unicode(radio), radio.name)
            else:
                radio = u'<li>%s</li>'% force_unicode(radio)
            radio_list.append(radio)
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join(radio_list))

class RadioSelectWithOtherWidget(forms.RadioSelect):
    renderer = RadioFieldWithOtherRenderer
    
    def value_from_datadict(self, data, files, name):
        if data.get(name, '').lower() == 'other':
            return data.get('other_'+name, None)
        return data.get(name, None)

class ChoiceWithOtherField(forms.ChoiceField):
    widget = RadioSelectWithOtherWidget
    
    def valid_value(self, value):
        return True
