window.addEventListener("load", function () {
    let carousel, next, prev, seats;

    carousel = document.querySelectorAll('.muses-carousel');

    seats = document.querySelectorAll('.muses-carousel-seat');

    next = function (el) {
        if (el.next().length > 0) {
            return el.next();
        } else {
            return seats.first();
        }
    };

    prev = function (el) {
        if (el.prev().length > 0) {
            return el.prev();
        } else {
            return seats.last();
        }
    };//

    let toggles = document.querySelectorAll('.toggle')

    toggles.forEach(
        t => t.addEventListener('click', function (e) {
            let el, i, new_seat, _i, _ref;
            el = document.querySelectorAll('.is-ref').forEach(el2 => {
                el2.classList.remove('is-ref')
            });
            document.querySelectorAll(e.currentTarget).forEach(sel1 => {
                if (sel1.toggle === 'next') {
                    new_seat = next(el);
                    carousel.classList.remove('is-reversing');
                } else {
                    new_seat = prev(el);
                    carousel.classList.add('is-reversing');
                }
                new_seat.classList.add('is-ref').css('order', 1);
                for (i = _i = 2, _ref = seats.length; 2 <= _ref ? _i <= _ref : _i >= _ref; i = 2 <= _ref ? ++_i : --_i) {
                    new_seat = next(new_seat).css('order', i);
                }
                carousel.classList.remove('is-set');
                return setTimeout((function () {
                    return carousel.classList.add('is-set');
                }), 50);
            })
        }))

});