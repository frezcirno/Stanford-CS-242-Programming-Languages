#lang racket
(print-as-expression #f)
(provide (all-defined-out))

;========;
; Import ;
;========;
; import `throw` and `try_except`.
(require "prob1.rkt")

;===========;
; Problem 2 ;
;===========;
; Task: Implement `eval` using `throw` and `try_except`.
; Note: You can define any other helper functions.

(define (eval1 e)
  (if (number? e)
    e
    (let ([op (car e)]
          [a (eval1 (cadr e))]
          [b (eval1 (caddr e))])
      (cond
        [(equal? op "+") (+ a b)]
        [(equal? op "-") (- a b)]
        [(equal? op "*") (* a b)]
        [(equal? op "/") (if (zero? b) (throw 'DivError) (/ a b))]
        [else (throw 'OpError)]
      )
    )
  )
)

(define (eval e)
  (try_except
    (lambda () (eval1 e))
    (lambda (msg) (printf "~a\n" msg))
  )
)