from unittest import skip

import rx
from rx import operators as ops


@skip
def test_interval():
    print('rx.interval(1)')
    obs = rx.interval(1)

    input('Press Enter to subscribe...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to dispose...\n')
    unsub.dispose()

    input('Press Enter to subscribe again...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to finish...\n')
    unsub.dispose()


@skip
def test_publish():
    print('rx.interval(1).pipe(ops.publish())')
    obs = rx.interval(1).pipe(ops.publish())

    input('Press Enter to connect...\n')
    obs.connect()

    input('Press Enter to subscribe...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to dispose...\n')
    unsub.dispose()

    input('Press Enter to subscribe again...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to finish...\n')
    unsub.dispose()


@skip
def test_ref_count():
    print('rx.interval(1).pipe(ops.publish(), ops.ref_count())')
    obs = rx.interval(1).pipe(
        ops.publish(), 
        ops.ref_count()
    )

    input('Press Enter to subscribe...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to dispose...\n')
    unsub.dispose()

    input('Press Enter to subscribe again...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to finish...\n')
    unsub.dispose()


@skip
def test_tuple_with_previous_using_scan():
    rx.from_iterable(range(10)).pipe(
        ops.start_with((-1, -1)),
        ops.scan(lambda tup, y: (y, tup[0])),
        ops.skip(2)
    ).subscribe(lambda x: print(x))


@skip
def test_tuple_with_previous_using_zip():
    from_range = rx.from_iterable(range(10))
    from_range.pipe(
        ops.skip(1),
        ops.zip(from_range),
    ).subscribe(lambda x: print(x))


@skip
def test_flat_map():
    rx.from_iterable(range(10)).pipe(
        ops.flat_map(lambda x: rx.from_iterable(range(x + 1)))
    ).subscribe(lambda x: print(x))
