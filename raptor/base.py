import unicodecsv
from collections import namedtuple
from django.core.exceptions import ValidationError

LineSuccess = namedtuple('LineSuccess',
                         field_names=['line_number', 'line', 'instance'])
LineError = namedtuple('LineError',
                       field_names=['line_number', 'line', 'error'])


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class Adaptor(object):
    SKIP_ON_ERROR = False
    HAS_HEADERS = True

    def __init__(self, input_csv, on_success=None, on_error=None):
        """
        Iniatilize the Adaptor instance, with a CSV input.
        could be a filename or a filehandler.

        on_success and on_error are optional callbacks invoked
        after the process of each line.

        They receive the LineSuccess / LineError object respectively
        """
        if not hasattr(self, 'HEADERS'):
            raise ValueError('You should define the HEADERS of the CSV')
        if not hasattr(self, 'MODEL'):
            raise ValueError('Define the Model!')

        if not hasattr(input_csv, 'read'):
            input_csv = open(input_csv, 'rb')
        self._on_success = on_success if callable(on_success) else lambda l: None
        self._on_error = on_error if callable(on_error) else lambda l: None
        self._csv_fh = input_csv

    def process(self, input_csv=None):
        """
        process each line in the input file.
        return a tuple (succesess, errors)
        """
        successes = []
        errors = []
        reader = unicodecsv.DictReader(self._csv_fh,
                                       fieldnames=self.HEADERS)
        if self.HAS_HEADERS:
            reader.next()
        for i, line in enumerate(reader):
            line_number = i + 1 if self.HAS_HEADERS else i
            try:
                data = self.process_line(line)
                instance = self.create_instance(**data)
            except ValidationError as e:
                le = LineError(line_number, line, unicode(e))
                errors.append(le)
                self._on_error(le)
                if self.SKIP_ON_ERROR:
                    continue
                raise
            ls = LineSuccess(line_number, line, instance)
            successes.append(ls)
            self._on_success(ls)
        return successes, errors

    @ClassProperty
    @classmethod
    def name(cls):
        return getattr(cls, 'NAME', cls.__name__).lower()

    @classmethod
    def import_data(cls, data):
        """drop-in compatibility with django-adaptors
        useful to work with django-devour
        """
        return cls(data).process()

    def process_line(self, line):
        """override in your subclass"""
        return line

    def create_instance(self, **data):
        instance = self.MODEL(**data)
        instance.full_clean()
        instance.save()
        return instance
