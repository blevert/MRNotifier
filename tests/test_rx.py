from unittest import skip

import rx


@skip
def test_publish():
    print('rx.Observable.interval(1000).publish()')
    obs = rx.Observable.interval(1000).publish()

    input('Press Enter to connect...\n')
    obs.connect()

    input('Press Enter to subscribe...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to dispose...\n')
    unsub.dispose()

    input('Press Enter to subscribe again...\n')
    obs.subscribe(lambda x: print(x))

    input('Press Enter to finish...\n')


@skip
def test_ref_count():
    print('rx.Observable.interval(1000).publish().ref_count()')
    obs = rx.Observable.interval(1000).publish().ref_count()

    input('Press Enter to subscribe...\n')
    unsub = obs.subscribe(lambda x: print(x))

    input('Press Enter to dispose...\n')
    unsub.dispose()

    input('Press Enter to subscribe again...\n')
    obs.subscribe(lambda x: print(x))

    input('Press Enter to finish...\n')
