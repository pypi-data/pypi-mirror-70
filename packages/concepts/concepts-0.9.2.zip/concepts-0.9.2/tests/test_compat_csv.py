# test_compat_csv.py

import sys

import pytest


@pytest.mark.skipif(sys.version_info.major != 2, reason='Python 2 only')
def test_UnicodeCsvReader():  # noqa: N802
    from concepts._compat_csv import UnicodeCsvReader

    reader = UnicodeCsvReader([u',majestic,bites\r\n',
                               u'M\xf8\xf8se,X,X\r\n',
                               u'Llama,,\r\n'])

    assert reader.dialect.delimiter == ','
    assert reader.line_num == 0

    assert next(reader) == [u'', u'majestic', u'bites']
    assert reader.line_num == 1

    assert list(reader) == [[u'M\xf8\xf8se', u'X', u'X'],
                            [u'Llama', u'', u'']]
