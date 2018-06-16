from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def file_size_limit(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('File too large. Size should not exceed 2 MiB.'))