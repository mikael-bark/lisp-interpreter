
(defun create-bintree (d n)
        (if (eqv? d 0)
            NIL
            (list n (create-bintree (- d 1)    (ash n 1))
                    (create-bintree (- d 1) (+ (ash n 1) 1)))))

(defun pre-order-dfs (node travlist)
    (if (null? node)
        NIL
        (begin (print (cons (car node) travlist))
               (pre-order-dfs (cadr node) (cons (car node) travlist))
               (pre-order-dfs (caddr node) (cons (car node) travlist)))))

(defun in-order-dfs (node travlist)
    (if (null? node)
        NIL 
        (begin (in-order-dfs (cadr node) (cons (car node) travlist))
               (print (cons (car node) travlist))
               (in-order-dfs (caddr node) (cons (car node) travlist)))))

(defun post-order-dfs (node travlist)
    (if (null? node)
        NIL
        (begin (post-order-dfs (cadr node) (cons (car node) travlist))
               (post-order-dfs (caddr node) (cons (car node) travlist))
               (print (cons (car node) travlist)))))

(pre-order-dfs (create-bintree 4 1) NIL)
(print)
(in-order-dfs (create-bintree 4 1) NIL)
(print)
(post-order-dfs (create-bintree 4 1) NIL)
(print)

