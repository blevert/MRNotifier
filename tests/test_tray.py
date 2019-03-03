from mrnotifier.tray import TrayOption, convert_to_tuple, do_nothing

from nose.tools import assert_equal


def test_to_tuple():
    assert_equal(TrayOption('x').to_tuple(), ('x', None, do_nothing))
    assert_equal(TrayOption('x', icon='icon').to_tuple(), ('x', 'icon', do_nothing))
    assert_equal(TrayOption('x', onclick=assert_equal).to_tuple(), ('x', None, assert_equal))
    assert_equal(TrayOption('x', icon='icon', onclick=assert_equal).to_tuple(), ('x', 'icon', assert_equal))


def test_convert_to_tuples():
    options = [TrayOption('x', do_nothing)]
    assert_equal(convert_to_tuple(options), (('x', None, do_nothing),))

    options.append(TrayOption('y', do_nothing))
    assert_equal(convert_to_tuple(options), (('x', None, do_nothing), ('y', None, do_nothing)))

